import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard SUHI — Rio de Janeiro",
    page_icon="🌡️",
    layout="wide", initial_sidebar_state="collapsed"
)

st.title("🌡️ Ilhas de Calor de Superfície — Rio de Janeiro")
st.caption("Análise exploratória de imagens Landsat | 2020–2025")


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "data" / "estatisticas_SUHI_2020_2025.csv"
)


ano = st.sidebar.selectbox(
    "Selecione o ano",
    sorted(df["Ano"].unique(), reverse=True)
)

dados = df[df["Ano"] == ano].iloc[0]

st.subheader(f"Indicadores de {ano}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("LST média", f"{dados['LST_media']:.2f} °C")
c2.metric("LST mínima", f"{dados['LST_min']:.2f} °C")
c3.metric("LST máxima", f"{dados['LST_max']:.2f} °C")
c4.metric("NDVI médio", f"{dados['NDVI_media']:.3f}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        df,
        x="Ano",
        y="LST_media",
        markers=True,
        title="Temperatura média de superfície",
        labels={
            "Ano": "Ano",
            "LST_media": "LST média (°C)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(
        df,
        x="Ano",
        y="NDVI_media",
        markers=True,
        title="Índice de vegetação médio",
        labels={
            "Ano": "Ano",
            "NDVI_media": "NDVI médio"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Estatísticas anuais")

colunas = [
    "Ano",
    "LST_media",
    "LST_min",
    "LST_max",
    "LST_desvio",
    "NDVI_media",
    "LST_pixels_validos",
    "NDVI_pixels_validos"
]

st.dataframe(
    df[colunas].round(3),
    use_container_width=True,
    hide_index=True
)

st.info(
    "Resultados exploratórios. As cenas possuem datas e "
    "coberturas válidas diferentes. A LST recebeu um filtro "
    "provisório de 10 a 60 °C. O NDBI está em revisão."
)



# === MAPA INTERATIVO SUHI ===
import numpy as np
import rasterio
import folium
import branca.colormap as cm
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
from streamlit_folium import st_folium
from pathlib import Path

st.divider()
st.subheader(f"Mapa de temperatura de superfície — {ano}")

@st.cache_data(show_spinner="Preparando mapa térmico...")
def preparar_mapa(ano_selecionado):
    caminho = (Path(__file__).resolve().parent.parent / "data" / "rasters" / f"LST_{ano_selecionado}_RIO.tif")
    
    with rasterio.open(caminho) as src:
        fator = max(1, int(np.ceil(max(src.width, src.height) / 1000)))
        largura = max(1, src.width // fator)
        altura = max(1, src.height // fator)

        transformacao = src.transform * src.transform.scale(
            src.width / largura, src.height / altura
        )

        origem = src.read(
            1,
            out_shape=(altura, largura),
            resampling=Resampling.nearest
        )

        destino_transform, destino_largura, destino_altura = (
            calculate_default_transform(
                src.crs, "EPSG:4326",
                largura, altura,
                *rasterio.transform.array_bounds(
                    altura, largura, transformacao
                )
            )
        )

        destino = np.full(
            (destino_altura, destino_largura),
            -9999, dtype=np.float32
        )

        reproject(
            source=origem,
            destination=destino,
            src_transform=transformacao,
            src_crs=src.crs,
            src_nodata=-9999,
            dst_transform=destino_transform,
            dst_crs="EPSG:4326",
            dst_nodata=-9999,
            resampling=Resampling.nearest
        )

    valido = (
        np.isfinite(destino)
        & (destino >= 10)
        & (destino <= 60)
    )

    paleta = np.array([
        [33, 102, 172],
        [103, 169, 207],
        [255, 255, 191],
        [253, 174, 97],
        [178, 24, 43]
    ], dtype=float)

    posicao = np.clip((destino - 10) / 50, 0, 1) * 4
    indice = np.minimum(posicao.astype(int), 3)
    fracao = (posicao - indice)[..., None]

    rgb = (
        paleta[indice] * (1 - fracao)
        + paleta[indice + 1] * fracao
    ).astype(np.uint8)

    rgba = np.zeros(
        (destino_altura, destino_largura, 4),
        dtype=np.uint8
    )
    rgba[:, :, :3] = rgb
    rgba[:, :, 3] = np.where(valido, 230, 0)

    oeste, sul, leste, norte = rasterio.transform.array_bounds(
        destino_altura, destino_largura, destino_transform
    )

    return rgba, [[sul, oeste], [norte, leste]]

try:
    imagem, limites_mapa = preparar_mapa(ano)

    centro_mapa = [
        (limites_mapa[0][0] + limites_mapa[1][0]) / 2,
        (limites_mapa[0][1] + limites_mapa[1][1]) / 2
    ]

    mapa_suhi = folium.Map(
        location=centro_mapa,
        tiles=None,
        zoom_control=True,
        control_scale=True
    )

    folium.raster_layers.ImageOverlay(
        image=imagem,
        bounds=limites_mapa,
        opacity=1,
        name=f"LST {ano}"
    ).add_to(mapa_suhi)

    escala = cm.LinearColormap(
        ["#2166ac", "#67a9cf", "#ffffbf",
         "#fdae61", "#b2182b"],
        vmin=10,
        vmax=60,
        caption="Temperatura de superfície (°C)"
    )
    escala.add_to(mapa_suhi)

    # Ajusta automaticamente a visualização à extensão do raster
    mapa_suhi.fit_bounds(
        limites_mapa,
        padding=(45, 45),
        max_zoom=10
    )

    # Exibe o mapa em uma área mais ampla
    st_folium(
        mapa_suhi,
        width=None,
        height=700,
        returned_objects=[],
        key=f"mapa_{ano}"
    )

    st.caption(
        "LST Landsat 8/9 em °C. Pixels transparentes representam "
        "ausência de dados válidos. Escala fixa: 10–60 °C."
    )

except FileNotFoundError:
    st.warning(
        f"Arquivo LST_{ano}_RIO.tif não encontrado em /content."
    )



# === COMPARACAO ESPACIAL SUHI ===

st.divider()
st.subheader("Comparação espacial entre dois anos")

st.caption(
    "Compare a distribuição espacial da temperatura de superfície "
    "em duas cenas Landsat. Os mapas utilizam a mesma escala "
    "de cores, de 10 °C a 60 °C."
)

anos_disponiveis = list(range(2020, 2026))

seletor_esquerdo, seletor_direito = st.columns(2)

with seletor_esquerdo:
    ano_esquerdo = st.selectbox(
        "Ano do primeiro mapa",
        anos_disponiveis,
        index=0,
        key="comparacao_ano_1"
    )

with seletor_direito:
    ano_direito = st.selectbox(
        "Ano do segundo mapa",
        anos_disponiveis,
        index=5,
        key="comparacao_ano_2"
    )


def construir_mapa_comparativo(ano_mapa):
    imagem, limites = preparar_mapa(ano_mapa)

    centro = [
        (limites[0][0] + limites[1][0]) / 2,
        (limites[0][1] + limites[1][1]) / 2
    ]

    mapa = folium.Map(
        location=centro,
        tiles=None,
        zoom_control=True,
        control_scale=True
    )

    folium.raster_layers.ImageOverlay(
        image=imagem,
        bounds=limites,
        opacity=1,
        name=f"LST {ano_mapa}"
    ).add_to(mapa)

    mapa.fit_bounds(
        limites,
        padding=(15, 15)
    )

    return mapa


coluna_mapa_1, coluna_mapa_2 = st.columns(2)

with coluna_mapa_1:
    st.markdown(f"**LST — {ano_esquerdo}**")

    try:
        mapa_1 = construir_mapa_comparativo(ano_esquerdo)

        st_folium(
            mapa_1,
            width=None,
            height=450,
            returned_objects=[],
            key=f"comparacao_mapa_1_{ano_esquerdo}"
        )

    except FileNotFoundError:
        st.warning(
            f"Raster LST_{ano_esquerdo}_RIO.tif não encontrado."
        )

with coluna_mapa_2:
    st.markdown(f"**LST — {ano_direito}**")

    try:
        mapa_2 = construir_mapa_comparativo(ano_direito)

        st_folium(
            mapa_2,
            width=None,
            height=450,
            returned_objects=[],
            key=f"comparacao_mapa_2_{ano_direito}"
        )

    except FileNotFoundError:
        st.warning(
            f"Raster LST_{ano_direito}_RIO.tif não encontrado."
        )


# Escala térmica compartilhada
escala_comparacao = cm.LinearColormap(
    [
        "#2166ac",
        "#67a9cf",
        "#ffffbf",
        "#fdae61",
        "#b2182b"
    ],
    vmin=10,
    vmax=60
)

st.markdown("**Escala térmica compartilhada (°C)**")

st.image(
    "data:image/svg+xml;base64," +
    __import__("base64").b64encode(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="700" height="55">'
            '<defs><linearGradient id="g">'
            '<stop offset="0%" stop-color="#2166ac"/>'
            '<stop offset="25%" stop-color="#67a9cf"/>'
            '<stop offset="50%" stop-color="#ffffbf"/>'
            '<stop offset="75%" stop-color="#fdae61"/>'
            '<stop offset="100%" stop-color="#b2182b"/>'
            '</linearGradient></defs>'
            '<rect x="20" y="5" width="660" height="20" '
            'fill="url(#g)"/>'
            '<g font-size="14" fill="#333">'
            '<text x="20" y="45">10</text>'
            '<text x="180" y="45">23</text>'
            '<text x="345" y="45">35</text>'
            '<text x="510" y="45">48</text>'
            '<text x="655" y="45">60 °C</text>'
            '</g></svg>'
        ).encode("utf-8")
    ).decode("ascii"),
    use_container_width=True
)

st.info(
    "Comparação visual exploratória: as cenas Landsat "
    "foram adquiridas em datas diferentes e apresentam "
    "coberturas distintas de pixels válidos. "
    "Diferenças de cor não representam, isoladamente, "
    "mudanças comprovadas na intensidade das ilhas de calor."
)

# === MODELAGEM PREDITIVA DA LST (2025) ===
st.divider()
st.subheader("Modelagem preditiva da temperatura de superfície — 2025")
st.caption(
    "Estimativa estatística da LST (°C) a partir do NDVI, com modelos "
    "treinados em pixels Landsat de 2025. Não constitui previsão meteorológica futura."
)

PASTA_RESULTADOS = BASE_DIR / "results"
CAMINHO_MODELO = BASE_DIR / "models" / "random_forest_lst_2025_compactado.joblib"

arquivo_metricas = PASTA_RESULTADOS / "metricas_modelos_2025.csv"
if arquivo_metricas.is_file():
    try:
        metricas = pd.read_csv(arquivo_metricas)
        st.markdown("**Desempenho dos modelos no conjunto de teste espacial**")
        st.dataframe(metricas, use_container_width=True, hide_index=True)
    except Exception as erro:
        st.warning(f"Não foi possível ler as métricas: {erro}")
else:
    st.warning("Arquivo de métricas não encontrado na pasta results/.")

col_fig_1, col_fig_2 = st.columns(2)
with col_fig_1:
    figura = PASTA_RESULTADOS / "comparacao_modelos_2025.png"
    if figura.is_file():
        st.image(str(figura), caption="Comparação de MAE e RMSE", use_container_width=True)
    else:
        st.warning("Gráfico de comparação dos modelos não encontrado.")
with col_fig_2:
    figura = PASTA_RESULTADOS / "lst_observada_prevista_2025.png"
    if figura.is_file():
        st.image(str(figura), caption="LST observada versus estimada — Random Forest", use_container_width=True)
    else:
        st.warning("Gráfico de LST observada versus estimada não encontrado.")

st.markdown("**Estimativa interativa com Random Forest**")
st.write("Informe um valor de NDVI para estimar a LST correspondente no modelo de 2025.")
ndvi_entrada = st.number_input(
    "NDVI do pixel",
    min_value=-1.0,
    max_value=1.0,
    value=0.30,
    step=0.05,
    format="%.2f",
    help="O NDVI varia teoricamente entre -1 e 1. Valores fora da faixa "
         "observada no treinamento podem gerar estimativas pouco confiáveis."
)

@st.cache_resource(show_spinner="Carregando modelo Random Forest...")
def carregar_modelo_lst(caminho):
    import joblib
    return joblib.load(caminho)

if CAMINHO_MODELO.is_file():
    try:
        modelo_lst = carregar_modelo_lst(str(CAMINHO_MODELO))
        entrada_modelo = pd.DataFrame({"NDVI": [float(ndvi_entrada)]})
        estimativa_lst = float(modelo_lst.predict(entrada_modelo)[0])
        st.metric("LST estimada pelo Random Forest", f"{estimativa_lst:.2f} °C")
    except Exception as erro:
        st.error(f"Não foi possível carregar ou executar o modelo: {erro}")
else:
    st.warning("Modelo compactado não encontrado na pasta models/.")

st.info(
    "Limitações metodológicas: modelo treinado somente com NDVI e LST de 2025; "
    "avaliação realizada por separação espacial de blocos de pixels. "
    "A estimativa não demonstra causalidade, não representa previsão para anos futuros "
    "e deve ser interpretada com cautela para valores de NDVI não observados no treinamento."
)



# ============================================================
# MODELAGEM MULTIANUAL — VALIDAÇÃO TEMPORAL LOYO
# ============================================================

st.divider()

st.header("Modelagem multianual da temperatura de superfície")

st.caption(
    "Avaliação exploratória da generalização temporal dos "
    "modelos entre 2020 e 2025, utilizando validação "
    "Leave-One-Year-Out (LOYO)."
)

# Caminhos relativos à raiz do repositório
raiz_projeto = Path(__file__).resolve().parent.parent

arquivo_metricas = (
    raiz_projeto / "data" /
    "comparacao_modelos_multianuais.csv"
)

arquivo_grafico_modelos = (
    raiz_projeto / "assets" /
    "comparacao_modelos_multianuais.png"
)

arquivo_grafico_rf = (
    raiz_projeto / "assets" /
    "random_forest_mae_por_ano.png"
)

# Tabela comparativa
st.subheader("Comparação dos modelos")

if arquivo_metricas.exists():
    metricas_multi = pd.read_csv(arquivo_metricas)

    st.dataframe(
        metricas_multi,
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Arquivo de métricas multianuais não encontrado.")

# Gráfico de comparação geral
if arquivo_grafico_modelos.exists():
    st.image(
        str(arquivo_grafico_modelos),
        caption="Comparação de MAE e RMSE médios — LOYO",
        use_container_width=True
    )

# Gráfico de desempenho anual
st.subheader("Desempenho temporal do Random Forest")

if arquivo_grafico_rf.exists():
    st.image(
        str(arquivo_grafico_rf),
        caption="MAE por ano de teste — Random Forest",
        use_container_width=True
    )

# Interpretação científica
st.subheader("Interpretação dos resultados")

st.markdown("""
A inclusão da temperatura do ar no horário de aquisição
das cenas Landsat reduziu aproximadamente **38,5% do MAE
médio** do Random Forest em comparação ao modelo que
utiliza somente NDVI.

O modelo com NDVI e temperatura do ar apresentou:

- **MAE médio:** 3,2949 °C
- **RMSE médio:** 4,1389 °C
- **R² médio:** 0,3887

Os resultados indicam melhoria do desempenho médio
na validação temporal, embora existam diferenças
importantes entre os anos avaliados.
""")

st.info(
    "Limitações metodológicas: foram utilizadas apenas "
    "seis cenas Landsat, uma por ano. A temperatura do ar "
    "é uma variável compartilhada pelos pixels de cada "
    "cena. O R² apresentado corresponde à média dos "
    "R² anuais. Os resultados são exploratórios e não "
    "constituem uma previsão validada para anos futuros."
)



# ============================================================
# INTEGRAÇÃO SOCIOAMBIENTAL — RIO DE JANEIRO
# ============================================================

st.divider()

st.header("Análise socioambiental do calor superficial")

st.markdown(
    "Integração exploratória da temperatura superficial "
    "Landsat 2025 com indicadores de rendimento dos "
    "responsáveis pelos domicílios do Censo 2022 (IBGE)."
)

# Indicadores da classificação
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Setores analisados",
        "12.760"
    )

with col2:
    st.metric(
        "Setores prioritários",
        "770"
    )

with col3:
    st.metric(
        "Percentual prioritário",
        "6,03%"
    )

st.subheader("Distribuição espacial")

# Caminho da imagem
mapa_socioambiental = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "mapa_socioambiental_rio_2025.png"
)

if mapa_socioambiental.exists():
    st.image(
        str(mapa_socioambiental),
        caption=(
            "Setores censitários com calor superficial "
            "elevado e baixo rendimento mediano."
        ),
        use_container_width=True
    )
else:
    st.warning("Mapa socioambiental não encontrado.")

st.subheader("Critérios da classificação")

st.markdown("""
Foram considerados elegíveis os setores censitários
com rendimento mediano válido e pelo menos cinco
pixels válidos de LST.

**Critérios utilizados:**

- **Calor elevado:** LST média ≥ 48,27 °C.
- **Baixo rendimento:** rendimento mediano ≤ R$ 1.290,75.
- **Classe prioritária:** ocorrência simultânea
  das duas condições.

Dos 13.782 setores censitários do município,
12.760 atenderam aos critérios de elegibilidade.

Entre os setores elegíveis, 770 (6,03%) foram
classificados com calor elevado e baixo rendimento.
""")

st.subheader("Associação entre rendimento e temperatura")

col1, col2 = st.columns(2)

with col1:
    st.metric("Correlação de Pearson", "−0,4915")

with col2:
    st.metric("Correlação de Spearman", "−0,2817")

st.markdown("""
As correlações negativas indicam uma associação
entre menores rendimentos medianos e temperaturas
superficiais mais elevadas nos setores analisados.

As correlações foram calculadas com os 13.359
setores que apresentaram ambas as variáveis válidas,
sem aplicação do filtro mínimo de cinco pixels.
""")

st.info(
    "Esta análise é exploratória. A LST corresponde "
    "a uma cena Landsat de 2025, enquanto os dados "
    "econômicos são do Censo 2022. A classificação "
    "utiliza limiares relativos à distribuição dos "
    "setores elegíveis e não representa um índice "
    "validado de risco climático ou uma relação causal."
)

