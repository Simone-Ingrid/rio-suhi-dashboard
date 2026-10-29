# 01 — Dados e Aquisição das Imagens Landsat

## 1. Introdução

Esta etapa apresenta as fontes de dados e os critérios gerais de organização das imagens de satélite utilizadas no desenvolvimento do dashboard científico para análise exploratória de Ilhas de Calor de Superfície (SUHI) no município do Rio de Janeiro.

O processamento dos dados geoespaciais integra a pesquisa intitulada *Modelo Computacional para Identificação e Predição de Ilhas de Calor Urbanas no Município do Rio de Janeiro utilizando Ciência de Dados e Geoprocessamento*, proposta em abril de 2026.

## 2. Área de estudo

A área de estudo corresponde ao município do Rio de Janeiro, localizado no estado do Rio de Janeiro, Brasil.

Para a delimitação espacial, foi utilizada uma camada vetorial dos municípios do estado do Rio de Janeiro, da qual foi selecionado o município identificado pelo atributo `NM_MUN = 'Rio de Janeiro'`.

O limite municipal foi armazenado no arquivo `Limite_Municipal_Rio.gpkg`, originalmente no sistema de referência EPSG:4674.

## 3. Dados de sensoriamento remoto

Foram utilizadas imagens dos satélites Landsat 8 e Landsat 9, pertencentes à coleção Landsat Collection 2, Level-2.

Esses produtos disponibilizam bandas de reflectância de superfície e temperatura de superfície, acompanhadas de informações de qualidade dos pixels.

| Característica | Descrição |
|---|---|
| Plataforma | Landsat 8 e Landsat 9 |
| Coleção | Collection 2 |
| Nível de processamento | Level-2 |
| Período | 2020–2025 |
| Área geográfica | Município do Rio de Janeiro |
| Resolução espacial de trabalho | 30 metros |
| Indicadores derivados | LST, NDVI e NDBI |
| Ambiente de geoprocessamento | QGIS 3.44.11 |

Foi utilizada uma cena do período de verão para cada ano analisado.

As datas exatas de aquisição, os identificadores das cenas e os critérios de seleção deverão ser registrados nos metadados para garantir a rastreabilidade dos produtos utilizados.

## 4. Bandas espectrais utilizadas

| Banda | Descrição | Aplicação |
|---|---|---|
| SR_B4 | Vermelho | Cálculo do NDVI |
| SR_B5 | Infravermelho próximo (NIR) | Cálculo do NDVI e NDBI |
| SR_B6 | Infravermelho de ondas curtas (SWIR1) | Cálculo do NDBI |
| ST_B10 | Temperatura de superfície | Cálculo da LST |
| QA_PIXEL | Qualidade dos pixels | Identificação de pixels inválidos e afetados por nuvens |

## 5. Organização temporal

Os dados foram organizados em seis conjuntos anuais, correspondentes a 2020, 2021, 2022, 2023, 2024 e 2025.

Para cada ano foram produzidos três rasters temáticos principais:

- `LST_ANO_RIO.tif`
- `NDVI_ANO_RIO.tif`
- `NDBI_ANO_RIO.tif`

A expressão `ANO` representa o ano de referência do produto.

Ao final do processamento, foram obtidos 18 arquivos raster recortados ao limite municipal.

## 6. Padronização geoespacial

Os produtos raster finais foram organizados utilizando:

- Sistema de referência EPSG:32623 — WGS 84 / UTM zona 23S.
- Resolução espacial de 30 metros.
- Delimitação pelo limite administrativo municipal.
- Valor NoData igual a -9999.

Esses procedimentos permitiram organizar os produtos geoespaciais para posterior análise estatística e visualização no dashboard.

## 7. Relação com o produto computacional

Os rasters processados constituem a base geoespacial do dashboard desenvolvido em Python e Streamlit.

A partir desses produtos foram extraídas estatísticas anuais e implementadas visualizações cartográficas interativas, incluindo a comparação espacial de temperatura de superfície entre diferentes anos.

Dessa forma, a etapa de aquisição e organização dos dados fornece os insumos necessários à implementação do produto computacional de visualização geoespacial previsto na proposta de pesquisa.

## 8. Reprodutibilidade

Para permitir a reprodução integral do estudo, deverão ser disponibilizados ou referenciados:

- Identificadores completos das cenas Landsat utilizadas.
- Datas de aquisição das imagens.
- Fontes oficiais dos dados.
- Parâmetros de processamento.
- Arquivos ou scripts de cálculo dos indicadores.
- Critérios de aplicação das máscaras de qualidade.
- Informações sobre o limite municipal empregado.

A documentação será complementada progressivamente conforme a consolidação dos metadados e dos procedimentos computacionais.
