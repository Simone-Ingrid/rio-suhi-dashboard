# 02 — Processamento das Imagens Landsat: LST, NDVI e NDBI

## 1. Introdução

Este documento apresenta os procedimentos de processamento das imagens Landsat 8 e Landsat 9 utilizados na construção dos indicadores geoespaciais que fundamentam o dashboard científico de Ilhas de Calor de Superfície no município do Rio de Janeiro.

O processamento foi realizado principalmente no QGIS 3.44.11, abrangendo a conversão radiométrica dos produtos Landsat Collection 2 Level-2, o cálculo de índices espectrais, o tratamento de pixels inválidos e o recorte dos rasters ao limite municipal.

Foram produzidos três indicadores:

- **LST (*Land Surface Temperature*):** temperatura da superfície terrestre, expressa em graus Celsius.
- **NDVI (*Normalized Difference Vegetation Index*):** índice espectral normalizado associado à vegetação.
- **NDBI (*Normalized Difference Built-up Index*):** índice espectral normalizado associado à identificação de superfícies construídas.

## 2. Produtos Landsat utilizados

Foram empregados produtos Landsat Collection 2, Level-2, dos sensores Landsat 8 e Landsat 9.

As bandas de reflectância de superfície utilizadas foram:

| Banda | Região espectral | Indicador |
|---|---|---|
| SR_B4 | Vermelho (Red) | NDVI |
| SR_B5 | Infravermelho próximo (NIR) | NDVI e NDBI |
| SR_B6 | Infravermelho de ondas curtas (SWIR1) | NDBI |
| ST_B10 | Temperatura de superfície | LST |
| QA_PIXEL | Qualidade dos pixels | Mascaramento |

## 3. Cálculo da Temperatura da Superfície Terrestre (LST)

A banda ST_B10 dos produtos Landsat Collection 2 Level-2 contém valores digitais que devem ser convertidos em temperatura física utilizando os fatores de escala e deslocamento disponibilizados pelo USGS.

### 3.1. Conversão para Kelvin

A conversão é realizada por:

\[
T_K = DN_{ST} \times 0.00341802 + 149
\]

Em que:

- \(T_K\): temperatura de superfície em Kelvin.
- \(DN_{ST}\): valor digital da banda ST_B10.
- \(0.00341802\): fator multiplicativo de escala.
- \(149\): deslocamento aditivo.

### 3.2. Conversão para Celsius

\[
LST_{^\circ C} = T_K - 273.15
\]

Substituindo a expressão anterior:

\[
\boxed{LST_{^\circ C} = (DN_{ST}\times0.00341802+149)-273.15}
\]

Essa foi a equação utilizada no processamento da temperatura de superfície no QGIS.

### 3.3. Tratamento dos valores de temperatura

Após a conversão, foi aplicado um filtro operacional para preservar valores de temperatura entre 10 °C e 60 °C.

A expressão utilizada na Calculadora Raster do GDAL foi:

```python
where((A >= 10) & (A <= 60) & (A != -9999), A, -9999)
```

Nessa expressão:

- `A` representa o raster de LST.
- Valores no intervalo de 10 °C a 60 °C são preservados.
- Valores fora do intervalo recebem NoData igual a -9999.

Esse intervalo constitui um critério de filtragem adotado no estudo, e não um limite físico universal da temperatura de superfície.

Consequentemente, os valores mínimos, máximos e médios apresentados no dashboard correspondem aos pixels preservados após a aplicação desse filtro.

## 4. Cálculo do NDVI

O NDVI é calculado a partir da reflectância nas regiões do infravermelho próximo e do vermelho.

\[
\boxed{NDVI=\frac{NIR-RED}{NIR+RED}}
\]

Para Landsat 8 e Landsat 9:

\[
NDVI=\frac{\rho_{B5}-\rho_{B4}}{\rho_{B5}+\rho_{B4}}
\]

Em que:

- \(\rho_{B5}\): reflectância de superfície da banda SR_B5.
- \(\rho_{B4}\): reflectância de superfície da banda SR_B4.

### 4.1. Conversão da reflectância

Os valores digitais das bandas SR dos produtos Landsat Collection 2 Level-2 devem ser convertidos em reflectância utilizando:

\[
\boxed{\rho=DN\times0.0000275-0.2}
\]

Em que:

- \(DN\): valor digital da banda.
- \(0.0000275\): fator multiplicativo.
- \(-0.2\): deslocamento aditivo.

O cálculo do NDVI deve utilizar os valores de reflectância convertidos, e não diretamente os valores digitais originais.

### 4.2. Interpretação

O NDVI geralmente varia entre -1 e 1 para reflectâncias não negativas e denominador positivo.

Valores mais elevados costumam indicar maior presença ou vigor da vegetação, enquanto valores próximos de zero podem representar superfícies com pouca vegetação.

Valores negativos podem estar associados à água e a outras superfícies com comportamento espectral distinto.

A interpretação deve considerar as características locais e as condições de aquisição da imagem.

## 5. Cálculo do NDBI

O NDBI utiliza as bandas SWIR1 e NIR:

\[
\boxed{NDBI=\frac{SWIR1-NIR}{SWIR1+NIR}}
\]

Para Landsat 8 e Landsat 9:

\[
NDBI=\frac{\rho_{B6}-\rho_{B5}}{\rho_{B6}+\rho_{B5}}
\]

Em que:

- \(\rho_{B6}\): reflectância de superfície da banda SR_B6.
- \(\rho_{B5}\): reflectância de superfície da banda SR_B5.

A conversão radiométrica utiliza o mesmo fator de escala e deslocamento descritos para o NDVI.

### 5.1. Interpretação

Valores positivos de NDBI podem estar associados a determinadas superfícies construídas ou expostas.

Entretanto, o índice não identifica exclusivamente áreas urbanizadas: solos expostos e outras coberturas podem apresentar respostas espectrais semelhantes.

Valores negativos não devem ser descartados automaticamente, pois podem representar respostas espectrais válidas.

### 5.2. Tratamento de valores anômalos

Durante o processamento, foram identificados valores anômalos em determinados rasters NDBI, especialmente associados a denominadores muito próximos de zero.

Para o produto de 2024, foi aplicada uma expressão de mascaramento e filtragem:

```python
where(
    (B == 1) &
    (A != -9999) &
    (A >= -1) &
    (A <= 1),
    A,
    -9999
)
```

Em que:

- `A`: raster NDBI.
- `B`: máscara de pixels válidos.
- `-9999`: valor NoData.

Esse procedimento preserva valores no intervalo [-1, 1] que atendam à condição da máscara.

A consistência dos rasters NDBI entre os diferentes anos ainda requer verificação adicional, especialmente quanto à distribuição dos valores negativos e à quantidade de pixels válidos.

## 6. Máscaras de qualidade

Os produtos Landsat Collection 2 Level-2 disponibilizam a banda QA_PIXEL, que codifica informações sobre a qualidade dos pixels.

O processamento incluiu o uso de máscaras para excluir pixels considerados inadequados à análise, incluindo aqueles afetados por nuvens.

A identificação dos pixels depende da interpretação dos bits da banda QA_PIXEL.

Para garantir a reprodução exata do procedimento, ainda será necessário registrar a expressão completa utilizada na geração das máscaras anuais e os bits efetivamente considerados.

## 7. Recorte ao limite municipal

Após o cálculo e o tratamento dos indicadores, os rasters foram recortados ao limite administrativo do município do Rio de Janeiro.

Foi utilizada a ferramenta do QGIS:

**GDAL → Recortar raster pela camada de máscara.**

Os parâmetros principais foram:

| Parâmetro | Configuração |
|---|---|
| Camada de máscara | `Limite_Municipal_Rio.gpkg` |
| Sistema de referência de saída | EPSG:32623 |
| Resolução espacial | 30 metros |
| Valor NoData | -9999 |
| Extensão | Limite municipal |
| Preservação da resolução | Habilitada |

O procedimento produziu 18 rasters, correspondentes aos três indicadores para os seis anos analisados.

## 8. Produtos raster finais

Os arquivos foram organizados segundo o padrão:

```text
LST_2020_RIO.tif
NDVI_2020_RIO.tif
NDBI_2020_RIO.tif

...

LST_2025_RIO.tif
NDVI_2025_RIO.tif
NDBI_2025_RIO.tif
```

Esses produtos constituem a base geoespacial processada da pesquisa.

## 9. Integração com o dashboard

O dashboard foi desenvolvido em Python, utilizando Streamlit e Folium.

Os rasters de temperatura de superfície são utilizados na construção dos mapas interativos, com reprojeção para EPSG:4326 durante a preparação das visualizações.

Foi adotada uma escala térmica fixa de 10 °C a 60 °C para facilitar a comparação visual entre anos.

As estatísticas anuais foram organizadas no arquivo:

`data/estatisticas_SUHI_2020_2025.csv`

Esse arquivo contém indicadores como média, mínimo, máximo, desvio-padrão e quantidade de pixels válidos.

## 10. Limitações metodológicas

A análise deve considerar:

1. As imagens correspondem a diferentes datas de aquisição.
2. A cobertura de pixels válidos varia entre os anos.
3. A filtragem da LST entre 10 °C e 60 °C influencia as estatísticas calculadas.
4. Os rasters NDBI requerem verificação adicional de consistência.
5. A comparação visual não constitui, isoladamente, comprovação de tendências climáticas ou mudanças urbanas.
6. A temperatura de superfície não equivale à temperatura do ar.
7. A identificação de uma ilha de calor de superfície exige critérios explícitos de comparação térmica, como uma referência espacial ou outra metodologia justificável.

## 11. Relação com a proposta de pesquisa

O processamento dos produtos Landsat constitui uma etapa fundamental da implementação computacional prevista na proposta de abril de 2026.

A obtenção dos indicadores LST, NDVI e NDBI permitiu construir uma base de dados geoespaciais utilizada na elaboração do dashboard científico interativo.

Assim, o processamento descrito neste documento contribuiu diretamente para a implementação do protótipo de visualização geoespacial previsto na proposta original, constituindo parte verificável do produto computacional desenvolvido.

## 12. Referência técnica

USGS — United
