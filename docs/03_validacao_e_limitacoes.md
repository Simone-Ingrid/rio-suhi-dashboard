# 03 — Validação dos Dados e Limitações Metodológicas

## 1. Introdução

Este documento apresenta os procedimentos de controle de qualidade, as verificações de consistência e as limitações metodológicas associadas aos dados geoespaciais utilizados no desenvolvimento do dashboard científico de Ilhas de Calor de Superfície (*Surface Urban Heat Islands — SUHI*) no município do Rio de Janeiro.

A análise compreende imagens Landsat 8 e Landsat 9, referentes ao período de 2020 a 2025, processadas para obtenção dos indicadores:

- Temperatura da Superfície Terrestre (LST);
- Índice de Vegetação por Diferença Normalizada (NDVI);
- Índice de Áreas Construídas por Diferença Normalizada (NDBI).

O objetivo desta etapa é avaliar a consistência dos produtos geoespaciais, identificar possíveis fontes de incerteza e estabelecer critérios para a interpretação dos resultados apresentados no dashboard.

## 2. Procedimentos de controle de qualidade

O processamento incluiu procedimentos de verificação e filtragem dos valores matriciais, com o objetivo de reduzir a influência de pixels inválidos e de valores incompatíveis com os critérios estabelecidos para a análise.

As principais verificações foram:

1. Identificação e exclusão de pixels classificados como inválidos pelas máscaras de qualidade.
2. Tratamento de valores NoData.
3. Aplicação de filtro operacional para a temperatura de superfície.
4. Verificação dos intervalos numéricos dos índices espectrais.
5. Contabilização dos pixels válidos.
6. Cálculo de estatísticas descritivas anuais.
7. Inspeção visual dos produtos raster no QGIS e no dashboard.

Esses procedimentos constituem verificações de consistência dos dados, não uma validação independente da precisão física das temperaturas estimadas.

## 3. Critérios de validade dos indicadores

### 3.1. Temperatura de superfície (LST)

Após a conversão da banda ST_B10 para graus Celsius, foi aplicado um filtro operacional de 10 °C a 60 °C.

Os pixels fora desse intervalo foram definidos como NoData.

Consequentemente, as estatísticas anuais representam somente os pixels preservados após o mascaramento e a filtragem.

O limite superior de 60 °C não deve ser interpretado como uma temperatura máxima física universal. Trata-se de uma escolha metodológica que pode excluir temperaturas reais superiores a esse valor.

### 3.2. Índice de vegetação (NDVI)

O NDVI foi calculado a partir das bandas de reflectância de superfície SR_B5 e SR_B4.

Para reflectâncias não negativas e denominador positivo, o índice está matematicamente limitado ao intervalo [-1, 1].

Valores fora desse intervalo podem indicar problemas numéricos, denominadores próximos de zero, reflectâncias negativas decorrentes do processamento ou pixels que requerem investigação.

### 3.3. Índice de áreas construídas (NDBI)

O NDBI foi calculado a partir das bandas SR_B6 e SR_B5.

Assim como o NDVI, seu intervalo convencional é [-1, 1], sob condições apropriadas dos valores de reflectância.

Valores negativos podem ser espectralmente válidos e não devem ser eliminados apenas por serem negativos.

Durante o processamento, foram identificadas diferenças relevantes entre as distribuições anuais do NDBI, exigindo uma verificação específica de consistência.

## 4. Estatísticas anuais da LST

A tabela apresenta as estatísticas obtidas a partir dos rasters processados e posteriormente organizadas no arquivo `estatisticas_SUHI_2020_2025.csv`.

| Ano | Pixels válidos | LST média (°C) | LST mínima (°C) | LST máxima (°C) | Desvio-padrão (°C) |
|---|---:|---:|---:|---:|---:|
| 2020 | 1.118.788 | 34,60 | 21,32 | 59,68 | 4,71 |
| 2021 | 1.309.652 | 43,00 | 19,80 | 60,00 | 5,61 |
| 2022 | 355.151 | 35,13 | 23,52 | 58,54 | 4,50 |
| 2023 | 852.087 | 30,78 | 10,23 | 57,34 | 5,83 |
| 2024 | 745.898 | 32,46 | 10,00 | 59,98 | 6,11 |
| 2025 | 1.307.947 | 42,14 | 25,38 | 60,00 | 5,53 |

Os valores foram arredondados para duas casas decimais. Os valores completos permanecem disponíveis no arquivo CSV.

### 4.1. Variação das médias anuais

As temperaturas médias variaram de aproximadamente 30,78 °C, em 2023, a 43,00 °C, em 2021.

Entretanto, essas diferenças não podem ser interpretadas diretamente como uma tendência de aquecimento ou resfriamento do município.

Cada ano foi representado por uma cena Landsat, adquirida em condições ambientais e atmosféricas específicas.

Além disso, a cobertura espacial de pixels válidos variou consideravelmente entre os anos.

### 4.2. Diferenças na cobertura de pixels válidos

O número de pixels válidos de LST variou entre 355.151, em 2022, e 1.309.652, em 2021.

Essa diferença é relevante porque as estatísticas podem ter sido calculadas sobre conjuntos espaciais distintos.

Uma média anual obtida sobre uma área parcialmente mascarada não é necessariamente comparável à média de outro ano com maior cobertura.

Portanto, comparações quantitativas mais rigorosas devem considerar uma máscara espacial comum ou outro procedimento de harmonização que assegure comparabilidade entre as observações.

## 5. Verificação de consistência do NDVI

A análise preliminar dos produtos NDVI identificou diferenças na quantidade de pixels válidos entre os anos.

| Ano | Pixels NDVI registrados |
|---|---:|
| 2020 | 1.124.148 |
| 2021 | 1.316.915 |
| 2022 | 355.981 |
| 2023 | 855.454 |
| 2024 | 751.177 |
| 2025 | 1.315.090 |

No processamento de 2020, foram identificados 21 valores de NDVI fora do intervalo convencional [-1, 1].

Essa ocorrência deverá ser verificada quanto às condições numéricas do cálculo e aos critérios de exclusão de pixels inválidos.

Os valores médios de NDVI apresentados no dashboard devem ser interpretados considerando os critérios de validade aplicados em sua extração.

## 6. Verificação de consistência do NDBI

A análise preliminar identificou uma diferença importante entre os produtos NDBI dos anos estudados.

| Ano | Pixels NDBI registrados |
|---|---:|
| 2020 | 1.124.169 |
| 2021 | 411.197 |
| 2022 | 60.570 |
| 2023 | 213.957 |
| 2024 | 107.886 |
| 2025 | 393.796 |

Os dados preliminares indicaram presença expressiva de valores negativos no raster de 2020, enquanto os produtos mascarados de 2021 a 2025 não apresentaram valores negativos.

Essa diferença não é suficiente para concluir que houve uma transformação física ou urbana entre os anos.

É necessário investigar se os produtos foram submetidos aos mesmos procedimentos de cálculo, mascaramento e filtragem.

### 6.1. Verificações necessárias

Antes de utilizar o NDBI em análises comparativas ou modelos estatísticos, recomenda-se:

1. Conferir a aplicação dos fatores de escala das bandas SR_B5 e SR_B6.
2. Verificar a ordem das bandas no numerador.
3. Examinar denominadores próximos de zero.
4. Confirmar a aplicação uniforme das máscaras QA_PIXEL.
5. Investigar eventuais filtros que tenham eliminado valores negativos.
6. Comparar histogramas e distribuições anuais.
7. Recalcular os produtos que apresentarem inconsistências confirmadas.

**Situação da verificação:** consistência interanual do NDBI ainda não demonstrada.

Por esse motivo, os produtos NDBI não devem ser utilizados para sustentar conclusões sobre mudanças nas áreas construídas até a conclusão da auditoria.

## 7. Limitações da comparação temporal

A comparação entre imagens Landsat adquiridas em diferentes anos envolve limitações relacionadas à aquisição das cenas, à disponibilidade de pixels e às condições ambientais.

Entre os principais fatores estão:

- Diferenças nas datas e horários de aquisição.
- Condições meteorológicas específicas de cada cena.
- Presença de nuvens e outros pixels mascarados.
- Variação da cobertura espacial efetivamente observada.
- Diferenças nas condições de umidade do solo e da vegetação.
- Sensibilidade dos indicadores aos critérios de filtragem.

O dashboard permite a comparação visual entre anos, mas essa funcionalidade não equivale, isoladamente, à demonstração de tendências climáticas de longo prazo.

## 8. Limitações da identificação de ilhas de calor de superfície

A temperatura de superfície constitui uma variável relevante para o estudo das ilhas de calor urbanas, mas não representa automaticamente a intensidade de uma ilha de calor.

Uma avaliação quantitativa de SUHI requer a definição de um referencial térmico apropriado, por exemplo, a comparação entre áreas urbanizadas e áreas de referência não urbanizadas, com critérios espaciais explícitos.

O dashboard atual apresenta distribuições de LST e estatísticas exploratórias.

Portanto, a identificação visual de regiões relativamente mais quentes deve ser distinguida de uma estimativa formal da intensidade de SUHI.

Também é necessário distinguir temperatura de superfície e temperatura do ar, pois são grandezas físicas diferentes.

## 9. Validação do dashboard

O dashboard foi desenvolvido em Python e Streamlit, integrando estatísticas anuais e visualizações cartográficas dos rasters processados.

As funcionalidades verificadas durante o desenvolvimento incluem:

| Funcionalidade | Situação |
|---|---|
| Seleção de ano entre 2020 e 2025 | Implementada |
| Exibição de indicadores anuais | Implementada |
| Visualização de estatísticas anuais | Implementada |
| Mapa interativo de LST | Implementada |
| Comparação espacial entre dois anos | Implementada |
| Escala térmica padronizada | Implementada |
| Execução no ambiente Google Colab | Verificada |
| Execução independente do Colab | Ainda não verificada |
| Validação de modelos preditivos | Não documentada nesta etapa |

A verificação funcional do dashboard não substitui testes sistemáticos de software nem validação científica dos dados apresentados.

## 10. Validação dos modelos preditivos

A proposta original de pesquisa prevê o desenvolvimento de modelos estatísticos ou de aprendizado de máquina para estimar áreas de risco térmico.

Também prevê a avaliação desses modelos por métricas como:

- RMSE (*Root Mean Squared Error*);
- MAE (*Mean Absolute Error*);
- R² (*Coefficient of Determination*);
- Validação cruzada.

Essas métricas se referem ao desempenho de modelos preditivos e não devem ser confundidas com os controles de qualidade dos rasters.

A implementação e a avaliação dos modelos deverão ser documentadas separadamente, com descrição das variáveis utilizadas, conjuntos de treinamento e teste, procedimentos de validação e resultados obtidos.

## 11. Relação com a proposta de pesquisa

Os procedimentos de processamento, controle de qualidade e análise exploratória contribuíram diretamente para a implementação do dashboard científico.

Esse dashboard constitui o produto computacional de visualização geoespacial interativa previsto na proposta de pesquisa de abril de 2026.

A ferramenta consolida uma parte dos resultados da investigação em uma interface funcional, permitindo examinar padrões espaciais de temperatura de superfície e comparar visualmente cenas de diferentes anos.

A conclusão das demais etapas da proposta, especialmente a modelagem preditiva e a integração de variáveis socioeconômicas, deverá ser demonstrada por resultados e documentação específicos.

## 12. Considerações finais

Os procedimentos realizados permitiram construir uma base geoespacial organizada e desenvolver um dashboard funcional para análise exploratória da temperatura de superfície no município do Rio de Janeiro.

A análise de consistência identificou limitações importantes relacionadas à cobertura espacial, à comparabilidade temporal e à distribuição dos valores de NDBI.

O registro dessas limitações contribui para a transparência metodológica e para a reprodutibilidade da pesquisa.

O produto computacional desenvolvido representa uma entrega verificável da proposta original, mantendo explícita a distinção entre funcionalidades implementadas, verificações ainda necessárias e objetivos científicos que dependem de validação adicional.
