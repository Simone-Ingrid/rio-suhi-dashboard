# Ilhas de Calor de Superfície no Município do Rio de Janeiro (2020–2025)

**Dashboard científico interativo para análise geoespacial e modelagem estatística da Temperatura da Superfície Terrestre (LST), utilizando sensoriamento remoto, dados meteorológicos e aprendizado de máquina.**

🌐 **[Acessar o dashboard](https://rio-suhi-dashboard.streamlit.app/)**

💻 **[Repositório GitHub](https://github.com/Simone-Ingrid/rio-suhi-dashboard)**

## 1. Apresentação do projeto

Este repositório apresenta o desenvolvimento de um produto computacional associado à pesquisa **“Modelo Computacional para Identificação e Predição de Ilhas de Calor Urbanas no Município do Rio de Janeiro utilizando Ciência de Dados e Geoprocessamento”**, proposta por Simone Gama em abril de 2026.

O projeto utiliza imagens Landsat 8 e Landsat 9, referentes ao período de 2020 a 2025, para investigar a distribuição espacial da Temperatura da Superfície Terrestre (*Land Surface Temperature — LST*) e sua associação com indicadores ambientais e meteorológicos.

O principal produto implementado é um dashboard científico desenvolvido em Python e Streamlit, disponibilizando análises exploratórias, mapas interativos, comparações espaciais e resultados de modelos de aprendizado de máquina.

## 2. Objetivos

O projeto tem como objetivos:

- Processar e organizar dados de sensoriamento remoto para o município do Rio de Janeiro.
- Investigar padrões espaciais de temperatura superficial e vegetação.
- Desenvolver ferramentas interativas para visualização de dados geoespaciais.
- Avaliar modelos estatísticos e de aprendizado de máquina para estimativa da LST.
- Investigar a capacidade de generalização temporal dos modelos.
- Estabelecer uma base computacional para estudos posteriores de vulnerabilidade climática urbana.

## 3. Dados utilizados

| Característica | Descrição |
|---|---|
| Área de estudo | Município do Rio de Janeiro, Brasil |
| Período | 2020–2025 |
| Satélites | Landsat 8 e Landsat 9 |
| Produto | Landsat Collection 2, Level-2 |
| Resolução espacial | 30 metros |
| Sistema de referência | EPSG:32623 |
| Variável térmica | LST (°C) |
| Índice de vegetação | NDVI |
| Índice de áreas construídas | NDBI — processamento realizado, com validação adicional pendente |
| Variável meteorológica | Temperatura do ar obtida de dados históricos ERA5-Land |

Foram utilizadas seis cenas Landsat, uma por ano, adquiridas entre janeiro e fevereiro.

As aquisições ocorreram aproximadamente às 12h52 UTC (09h52 no horário de Brasília).

## 4. Metodologia computacional

O processamento geoespacial foi realizado principalmente no QGIS, com etapas complementares desenvolvidas em Python e Google Colab.

As principais operações compreenderam:

1. Aquisição e organização das imagens Landsat.
2. Aplicação de máscaras de qualidade para identificação de pixels inválidos.
3. Conversão da banda térmica ST_B10 para temperatura em graus Celsius.
4. Cálculo dos índices espectrais NDVI e NDBI.
5. Tratamento de valores NoData.
6. Recorte espacial ao limite administrativo do município.
7. Extração de estatísticas anuais.
8. Desenvolvimento de mapas interativos e visualizações estatísticas.
9. Construção de bases de dados para aprendizado de máquina.
10. Treinamento e avaliação de modelos com separação espacial e temporal.

A conversão da temperatura de superfície utilizou os fatores de escala e deslocamento do produto Landsat Collection 2 Level-2.

## 5. Dashboard científico

O dashboard está publicado e acessível em:

https://rio-suhi-dashboard.streamlit.app/

### Funcionalidades implementadas

- Seleção interativa dos anos de 2020 a 2025.
- Visualização de estatísticas anuais de LST e NDVI.
- Gráficos comparativos dos indicadores.
- Mapas interativos de temperatura superficial.
- Comparação espacial entre diferentes anos.
- Apresentação dos resultados de modelagem espacial de 2025.
- Estimativa interativa de LST a partir do NDVI, utilizando Random Forest treinado com dados de 2025.
- Comparação de modelos de generalização temporal para 2020–2025.
- Visualização de métricas de desempenho e limitações metodológicas.

A estimativa interativa de 2025 constitui uma aproximação estatística baseada nos dados utilizados no treinamento, não uma previsão meteorológica para datas futuras.

## 6. Modelagem espacial — 2025

Foram avaliados dois algoritmos para estimar a LST a partir do NDVI:

- Regressão Linear.
- Random Forest Regressor.

A base de modelagem utilizou 100.000 pixels amostrados da cena de 2025.

A avaliação foi realizada com separação espacial de blocos de pixels, reduzindo a sobreposição espacial direta entre treinamento e teste.

### Resultados

| Modelo | MAE (°C) | RMSE (°C) | R² |
|---|---:|---:|---:|
| Regressão Linear | 2,4326 | 3,1454 | 0,6843 |
| Random Forest | **2,2152** | **2,8937** | **0,7328** |

O Random Forest apresentou melhor desempenho no experimento espacial de 2025.

Entretanto, esses resultados não demonstram capacidade de previsão para outros anos.

## 7. Modelagem multianual — 2020 a 2025

Foi construída uma base experimental contendo 600.000 observações, correspondentes a 100.000 pixels amostrados por ano.

Foram investigadas duas variáveis explicativas:

- NDVI, associado às características espectrais da vegetação.
- Temperatura do ar, utilizada para representar parte das condições meteorológicas da cena.

### 7.1. Integração meteorológica

Os horários de aquisição foram recuperados dos metadados Landsat.

A temperatura do ar no horário aproximado de passagem dos satélites foi estimada por interpolação temporal entre os registros meteorológicos horários.

Essa variável foi utilizada para investigar se a inclusão de informações meteorológicas melhora a generalização temporal dos modelos.

### 7.2. Estratégia de validação

Foi utilizada a estratégia *Leave-One-Year-Out* (LOYO).

Em cada experimento, cinco anos foram utilizados no treinamento e o ano restante foi reservado para teste.

O procedimento foi repetido seis vezes, permitindo avaliar o comportamento dos modelos em cenas não utilizadas no respectivo treinamento.

### 7.3. Resultados comparativos

| Algoritmo | Variáveis | MAE médio (°C) | RMSE médio (°C) | R² médio |
|---|---|---:|---:|---:|
| Regressão Linear | NDVI | 5,3281 | 6,4099 | −0,4507 |
| Regressão Linear | NDVI + temperatura às 11h | 4,7220 | 5,6955 | −0,2394 |
| Regressão Linear | NDVI + temperatura na aquisição | 4,8479 | 5,8392 | −0,2603 |
| Random Forest | NDVI | 5,3573 | 6,4231 | −0,4558 |
| **Random Forest** | **NDVI + temperatura na aquisição** | **3,2949** | **4,1389** | **0,3887** |

Os valores correspondem às médias aritméticas das métricas obtidas nos seis anos de teste.

O Random Forest com NDVI e temperatura do ar apresentou o melhor desempenho médio, reduzindo aproximadamente 38,5% do MAE em relação ao Random Forest que utiliza somente NDVI.

A melhoria ocorreu em cinco dos seis anos avaliados. Em 2024, o modelo com temperatura do ar apresentou erro superior ao modelo baseado somente em NDVI.

### 7.4. Visualização dos resultados

![Comparação dos modelos multianuais](assets/comparacao_modelos_multianuais.png)

*Figura 1 — Comparação de MAE e RMSE médios na validação temporal LOYO.*

![Desempenho anual do Random Forest](assets/random_forest_mae_por_ano.png)

*Figura 2 — Comparação do MAE anual do Random Forest com e sem integração meteorológica.*

## 8. Principais resultados científicos

Os experimentos permitiram identificar os seguintes comportamentos:

- Associação negativa entre NDVI e LST nas seis cenas analisadas.
- Desempenho favorável do Random Forest na modelagem espacial de 2025.
- Limitações de generalização temporal dos modelos que utilizam exclusivamente NDVI.
- Melhoria média da generalização temporal com a inclusão da temperatura do ar no Random Forest.
- Sensibilidade dos modelos às condições específicas de determinados anos.
- Importância da avaliação temporal independente da avaliação espacial.

Esses resultados indicam que a modelagem da LST pode se beneficiar da integração de variáveis espectrais e meteorológicas, mas a robustez temporal ainda exige investigação adicional.

## 9. Limitações metodológicas

Os resultados devem ser interpretados considerando as seguintes limitações:

1. **Quantidade de cenas:** foram utilizadas apenas seis imagens Landsat, uma por ano.
2. **Independência meteorológica:** embora a base contenha 600.000 observações de pixels, existem somente seis condições meteorológicas de aquisição.
3. **Comparabilidade temporal:** as cenas foram obtidas em datas e condições ambientais diferentes.
4. **Cobertura espacial:** a quantidade e a distribuição dos pixels válidos variam entre os anos.
5. **Generalização:** a validação LOYO oferece uma avaliação exploratória, mas não comprova desempenho confiável para anos futuros.
6. **Índices espectrais:** o processamento multianual do NDBI ainda necessita de validação adicional.
7. **Interpretação estatística:** associações entre NDVI, temperatura do ar e LST não demonstram causalidade.

Os resultados não devem ser interpretados isoladamente como evidência de tendência climática, aquecimento urbano de longo prazo ou efeito causal de transformações no uso do solo.

## 10. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Processamento, análise e modelagem |
| QGIS | Geoprocessamento e tratamento dos rasters |
| Rasterio | Leitura e processamento de dados matriciais |
| NumPy | Operações numéricas |
| Pandas | Manipulação e organização de dados |
| Scikit-learn | Modelagem estatística e aprendizado de máquina |
| Joblib | Serialização de modelos |
| Matplotlib | Gráficos científicos |
| Plotly | Visualizações interativas |
| Folium | Mapas interativos |
| Streamlit | Dashboard científico |
| Google Colab | Desenvolvimento e experimentação |
| GitHub | Versionamento e disponibilização do projeto |

## 11. Organização do repositório

```text
rio-suhi-dashboard/
├── app/
│   └── app.py
├── assets/
│   ├── comparacao_modelos_multianuais.png
│   └── random_forest_mae_por_ano.png
├── data/
│   ├── rasters/
│   ├── estatisticas_SUHI_2020_2025.csv
│   ├── comparacao_modelos_multianuais.csv
│   ├── resultados_rf_multianual_loyo.csv
│   ├── resumo_meteorologico_2020_2025.csv
│   ├── temperatura_ar_aquisicao_2020_2025.csv
│   └── datas_cenas_landsat.csv
├── docs/
├── models/
│   └── random_forest_lst_2025_compactado.joblib
├── notebooks/
├── requirements.txt
└── README.md
```

## 12. Situação em relação à proposta de pesquisa

| Objetivo | Situação |
|---|---|
| Aquisição e processamento Landsat | Implementado |
| Análise exploratória de LST e NDVI | Implementado |
| Mapas geoespaciais interativos | Implementado |
| Dashboard científico público | Implementado |
| Modelagem espacial de LST | Implementado para 2025 |
| Modelagem temporal multianual | Experimentos exploratórios concluídos |
| Integração de temperatura do ar | Implementada experimentalmente |
| Integração socioeconômica | Pendente |
| Indicador composto de vulnerabilidade climática | Pendente |
| Validação ampliada com novas cenas e condições ambientais | Pendente |

O projeto apresenta um produto computacional funcional e resultados experimentais documentados, mas ainda não contempla integralmente todos os objetivos da proposta original.

## 13. Continuidade da pesquisa

Como possibilidades de desenvolvimento futuro, destacam-se:

- Ampliação da base de cenas Landsat.
- Inclusão de outras variáveis meteorológicas e ambientais.
- Validação adicional do NDBI.
- Investigação de estratégias mais robustas de generalização temporal.
- Integração de indicadores socioeconômicos.
- Desenvolvimento e validação de um indicador composto de vulnerabilidade climática urbana.

## 14. Considerações finais

O projeto resultou na implementação de um dashboard científico público que integra sensoriamento remoto, geoprocessamento, análise estatística e aprendizado de máquina.

Além das funcionalidades de visualização, foram desenvolvidos experimentos de modelagem espacial e temporal, com avaliação por métricas quantitativas e documentação de suas limitações.

O produto constitui uma entrega computacional verificável da pesquisa e uma base para o desenvolvimento de métodos mais abrangentes de análise e modelagem das ilhas de calor urbanas.

---

**Projeto de pesquisa:** Modelo Computacional para Identificação e Predição de Ilhas de Calor Urbanas no Município do Rio de Janeiro utilizando Ciência de Dados e Geoprocessamento.

**Autoria:** Simone Gama.

**Proposta original:** Abril de 2026.

**Período analisado:** 2020–2025.

**Produto computacional:** Dashboard científico interativo de Ilhas de Calor de Superfície.

**Estado atual:** Dashboard funcional e publicado; modelagem espacial e experimentos de validação temporal implementados; extensões científicas em desenvolvimento.
