# Ilhas de Calor de Superfície no Município do Rio de Janeiro (2020–2025)

**Dashboard científico interativo desenvolvido como produto computacional da pesquisa sobre identificação e predição de ilhas de calor urbanas no município do Rio de Janeiro.**

## 1. Apresentação do projeto

Este repositório apresenta o desenvolvimento de um dashboard científico interativo para análise exploratória das Ilhas de Calor de Superfície (*Surface Urban Heat Islands — SUHI*) no município do Rio de Janeiro, utilizando imagens dos satélites Landsat 8 e Landsat 9, referentes ao período de 2020 a 2025.

O projeto integra técnicas de sensoriamento remoto, Ciência de Dados, Geoprocessamento e visualização geoespacial, permitindo analisar a distribuição espacial da Temperatura da Superfície Terrestre (*Land Surface Temperature — LST*) e indicadores relacionados à vegetação e às áreas construídas.

## Produto Computacional da Pesquisa — Dashboard SUHI

Como resultado do processamento de imagens Landsat 8/9 e das análises geoespaciais realizadas para o município do Rio de Janeiro, foi desenvolvido e publicado um dashboard científico interativo para exploração da Temperatura da Superfície Terrestre (LST) e de indicadores espectrais no período de 2020 a 2025.

O dashboard constitui a implementação do produto computacional de visualização geoespacial previsto na proposta de pesquisa, permitindo a apresentação e a exploração dos resultados obtidos.

**Acesso público ao dashboard:**

https://rio-suhi-dashboard.streamlit.app/

**Código-fonte e documentação científica:**

https://github.com/Simone-Ingrid/rio-suhi-dashboard

### Funcionalidades implementadas

- Visualização de indicadores anuais de temperatura de superfície e NDVI.
- Gráficos de evolução das estatísticas anuais.
- Consulta às estatísticas descritivas dos seis anos analisados.
- Visualização cartográfica interativa dos rasters LST.
- Comparação espacial entre imagens de diferentes anos.
- Seleção dinâmica dos períodos de análise.

### Tecnologias utilizadas

Python, Streamlit, Pandas, NumPy, Plotly, Rasterio, Folium, QGIS e imagens Landsat Collection 2 Level-2.

### Situação do produto

**Dashboard desenvolvido, publicado e acessível publicamente.**

A ferramenta representa uma entrega computacional verificável da pesquisa. As análises apresentadas possuem caráter exploratório e estão sujeitas às limitações metodológicas documentadas no repositório, especialmente quanto à comparabilidade temporal das cenas e à validação dos índices espectrais.


## 2. Vinculação à proposta de pesquisa

O presente trabalho está vinculado à proposta de pesquisa intitulada:

**“Modelo Computacional para Identificação e Predição de Ilhas de Calor Urbanas no Município do Rio de Janeiro utilizando Ciência de Dados e Geoprocessamento”**

- **Autoria da proposta:** Simone Gama
- **Data da proposta:** Abril de 2026
- **Área de aplicação:** Ciência de Dados, Geoprocessamento e Sustentabilidade Urbana
- **Área de estudo:** Município do Rio de Janeiro, Brasil

A proposta estabelece como objetivo geral o desenvolvimento de um modelo computacional para identificação, modelagem e predição de áreas de maior vulnerabilidade às ilhas de calor urbanas.

Entre seus objetivos específicos, destaca-se a construção de visualizações geoespaciais interativas, por meio de dashboard ou protótipo de sistema web, destinadas a apoiar a análise de informações ambientais e a tomada de decisão.

Nesse contexto, o dashboard disponibilizado neste repositório representa a **materialização do produto computacional de visualização interativa previsto na proposta original**, consolidando os resultados do processamento geoespacial em uma ferramenta acessível e organizada.

## 3. Produto computacional resultante da pesquisa

### Dashboard de Análise de Ilhas de Calor de Superfície — Rio de Janeiro

O principal produto tecnológico implementado nesta etapa da pesquisa é um dashboard científico desenvolvido em Python, utilizando o framework Streamlit.

Sua implementação constitui o resultado da integração das atividades de aquisição, processamento, tratamento, análise estatística e visualização de dados geoespaciais.

O dashboard permite:

- Selecionar o ano de análise entre 2020 e 2025.
- Visualizar indicadores estatísticos de temperatura de superfície.
- Consultar valores médios de NDVI.
- Examinar estatísticas anuais dos dados processados.
- Explorar mapas interativos de temperatura de superfície.
- Comparar espacialmente dois anos selecionados.
- Identificar visualmente padrões de distribuição térmica no território municipal.

A ferramenta foi desenvolvida para facilitar a interpretação dos resultados e demonstrar a aplicação prática de técnicas computacionais ao estudo das ilhas de calor de superfície.

**Assim, o dashboard constitui uma entrega concreta da pesquisa, atendendo ao objetivo específico de implementação de um protótipo de visualização geoespacial interativa e à etapa correspondente prevista no cronograma original.**

### 3.1. Relação entre os objetivos propostos e os resultados implementados

| Elemento da proposta | Resultado implementado | Situação |
|---|---|---|
| Aquisição e pré-processamento de dados geoespaciais | Processamento de imagens Landsat 8/9 | Implementado para os dados Landsat |
| Análise exploratória de dados | Estatísticas de LST e NDVI para 2020–2025 | Implementado |
| Construção de mapas temáticos | Mapas de temperatura de superfície | Implementado |
| Visualização geoespacial interativa | Dashboard Streamlit com mapas Folium | Implementado |
| Comparação espacial e temporal exploratória | Seleção e comparação visual entre anos | Implementado |
| Integração de dados climáticos e socioeconômicos | Integração completa das bases propostas | Em processo de finalização |
| Modelagem estatística e aprendizado de máquina | Modelos de predição de risco térmico | Em processo de finalização |
| Avaliação de modelos preditivos | RMSE, MAE, R² e validação cruzada | Em processo de finalização |
| Indicador composto de vulnerabilidade climática | Indicador integrado de risco | Em processo de finalização |

A distinção entre funcionalidades implementadas e etapas pendentes assegura a rastreabilidade dos resultados em relação aos objetivos estabelecidos na proposta.

## 4. Objetivo do dashboard

Disponibilizar uma ferramenta computacional interativa para exploração e visualização de dados de temperatura de superfície e indicadores espectrais, permitindo identificar padrões espaciais associados às características ambientais do município do Rio de Janeiro.

O dashboard também estabelece uma base computacional para futuras extensões voltadas à modelagem preditiva e à análise integrada de vulnerabilidade climática.

## 5. Dados utilizados

- **Satélites:** Landsat 8 e Landsat 9.
- **Produto:** Landsat Collection 2, Level-2.
- **Período de análise:** 2020–2025.
- **Área de estudo:** Município do Rio de Janeiro.
- **Resolução espacial de trabalho:** 30 metros.
- **Indicadores processados:** LST, NDVI e NDBI.
- **Sistema de referência dos rasters recortados:** EPSG:32623.

## 6. Metodologia computacional

O desenvolvimento do produto compreendeu as seguintes etapas:

1. Aquisição e organização das imagens Landsat.
2. Aplicação de máscaras de qualidade para tratamento de nuvens e pixels inválidos.
3. Cálculo da temperatura de superfície em graus Celsius.
4. Cálculo dos índices espectrais NDVI e NDBI.
5. Tratamento de valores inválidos e definição de NoData.
6. Recorte das imagens ao limite administrativo do município.
7. Extração e organização de estatísticas anuais.
8. Implementação de mapas temáticos interativos.
9. Desenvolvimento e integração dos componentes do dashboard.
10. Implementação da comparação espacial entre anos.

Os procedimentos e parâmetros serão detalhados nos documentos metodológicos deste repositório.

## 7. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| QGIS | Processamento e análise geoespacial |
| Python | Implementação das rotinas computacionais |
| Rasterio | Leitura, manipulação e reprojeção de rasters |
| NumPy | Processamento matricial |
| Pandas | Organização de estatísticas |
| Streamlit | Desenvolvimento do dashboard |
| Folium | Visualização cartográfica interativa |
| Google Colab | Ambiente de desenvolvimento e execução |
| GitHub | Versionamento, documentação e disponibilização do produto |

## 8. Resultados e contribuições

O desenvolvimento do dashboard demonstra a viabilidade de integrar produtos de sensoriamento remoto e ferramentas de Ciência de Dados em uma aplicação computacional para análise exploratória de ilhas de calor de superfície.

Entre as principais contribuições desta etapa destacam-se:

- Sistematização de dados geoespaciais de seis anos.
- Construção de indicadores estatísticos de temperatura superficial.
- Produção de visualizações cartográficas interativas.
- Implementação de uma interface para exploração dos resultados.
- Desenvolvimento de um produto computacional associado diretamente à proposta de pesquisa.
- Estabelecimento de uma estrutura inicial para documentação e reprodutibilidade.

## 9. Limitações e continuidade da pesquisa

As imagens analisadas correspondem a cenas Landsat adquiridas em diferentes datas e apresentam variações de cobertura de pixels válidos.

Portanto, a comparação entre os anos possui caráter exploratório e não permite, isoladamente, atribuir mudanças térmicas a transformações urbanas ou climáticas.

O dashboard atual concentra-se na análise descritiva e espacial da temperatura de superfície.

A implementação dos modelos preditivos, a integração de variáveis socioeconômicas e a construção de indicadores compostos de vulnerabilidade climática permanecem como etapas de desenvolvimento necessárias para contemplar integralmente o escopo da proposta original.

## 10. Considerações finais

O dashboard científico desenvolvido constitui o **produto computacional de visualização geoespacial interativa previsto na proposta de pesquisa de abril de 2026**.

Sua implementação demonstra que as atividades de processamento de imagens Landsat, análise exploratória e geoprocessamento resultaram em uma ferramenta funcional, capaz de apresentar e comparar informações sobre a distribuição espacial da temperatura de superfície no município do Rio de Janeiro.

Dessa forma, o produto representa uma entrega efetiva e verificável da pesquisa, especialmente no que se refere à construção do protótipo interativo previsto nos objetivos específicos e no cronograma de execução.

A ferramenta também constitui uma base para a incorporação futura de modelos preditivos e indicadores integrados de vulnerabilidade climática, em continuidade aos demais objetivos estabelecidos na proposta original.

---

**Projeto de pesquisa:** Modelo Computacional para Identificação e Predição de Ilhas de Calor Urbanas no Município do Rio de Janeiro utilizando Ciência de Dados e Geoprocessamento.

**Autoria:** Simone Gama.

**Proposta original:** Abril de 2026.

**Produto computacional:** Dashboard científico interativo para análise exploratória de ilhas de calor de superfície no Rio de Janeiro.

**Período dos dados:** 2020–2025.

**Estado do produto:** Protótipo funcional, com documentação e aprimoramentos em desenvolvimento.
