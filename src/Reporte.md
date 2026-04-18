# Reporte Estadístico: Efecto del Tratamiento sobre el Peso Seco de Plantas

**Asignatura:** Estadística Inferencial ||  
**Equipo:** Lizeth Hernandez Hernandez - Emilio Sanchez Estrada - Carlos Alberto Lule 
**Fecha:** 23/04/2026
**Dataset:** PlantGrowth (R Core Team, 2023)

---

## 1. Introducción

Se realizó un análisis de varianza de un factor (ANOVA de una vía) para examinar el efecto de diferentes tratamientos sobre el peso seco de plantas (en gramos). El estudio empleó el diseño completamente aleatorio (DCA), en el que las unidades experimentales fueron asignadas de forma aleatoria a uno de tres grupos: control (*ctrl*), tratamiento 1 (*trt1*) y tratamiento 2 (*trt2*). El conjunto de datos corresponde al dataset `PlantGrowth`, disponible en el entorno base de R (R Core Team, 2023).

---

## 2. Método

### 2.1 Participantes y diseño

El estudio incluyó *N* = 30 observaciones distribuidas equitativamente en tres grupos (*n* = 10 por grupo). El factor independiente fue el tipo de tratamiento (control, tratamiento 1 y tratamiento 2), y la variable dependiente fue el peso seco de las plantas medido en gramos.

### 2.2 Modelo estadístico

El modelo lineal del DCA es:

$$Y_{ij} = \mu + \tau_i + \varepsilon_{ij}$$

donde $Y_{ij}$ es la *j*-ésima observación del *i*-ésimo tratamiento, $\mu$ es la media general, $\tau_i$ es el efecto del *i*-ésimo tratamiento, y $\varepsilon_{ij} \sim N(0, \sigma^2)$ es el error aleatorio.

### 2.3 Hipótesis

$$H_0: \mu_1 = \mu_2 = \mu_3$$
$$H_1: \text{Al menos un } \mu_i \neq \mu_j$$

### 2.4 Nivel de significancia

Se estableció un nivel de significancia $\alpha = .05$ para todas las pruebas estadísticas.

---

## 3. Resultados

### 3.1 Estadísticas descriptivas

*Tabla 1*

*Estadísticas descriptivas del peso seco de plantas por grupo de tratamiento*

| Grupo        |  *n* | *M* (g) | *DE* (g) | CV (%) | IC 95% inferior | IC 95% superior |
|:-------------|:----:|:-------:|:--------:|:------:|:---------------:|:---------------:|
| Control      |  10  |  5.032  |  0.5832  |  11.59 |     4.615       |     5.449       |
| Tratamiento 1|  10  |  4.661  |  0.7936  |  17.03 |     4.093       |     5.229       |
| Tratamiento 2|  10  |  5.526  |  0.4425  |   8.01 |     5.209       |     5.843       |

*Nota.* M = media aritmética; DE = desviación estándar muestral; CV = coeficiente de variación; IC = intervalo de confianza para la media. Los intervalos de confianza se calcularon con la distribución *t* de Student (*gl* = 9).

Las medias observadas sugieren que el tratamiento 2 produjo plantas con mayor peso seco (*M* = 5.526 g, *DE* = 0.442), seguido por el grupo control (*M* = 5.032 g, *DE* = 0.583) y el tratamiento 1 (*M* = 4.661 g, *DE* = 0.794). El coeficiente de variación indica una variabilidad baja en el grupo control (CV = 11.59%) y en el tratamiento 2 (CV = 8.01%), mientras que el tratamiento 1 presentó una variabilidad moderada (CV = 17.03%).

### 3.2 Verificación de supuestos

Previo al análisis de varianza, se verificaron los supuestos del modelo.

**Normalidad.** Se aplicó la prueba de Shapiro-Wilk a cada grupo por separado. Los resultados indicaron que la distribución del peso seco no difirió significativamente de la normal en ninguno de los tres grupos: control, *W*(10) = 0.9571, *p* = .752; tratamiento 1, *W*(10) = 0.9302, *p* = .449; tratamiento 2, *W*(10) = 0.9411, *p* = .564. Por tanto, el supuesto de normalidad se consideró satisfecho.

**Homogeneidad de varianzas.** La prueba de Levene no reveló diferencias significativas entre las varianzas de los grupos, *F*(2, 27) = 1.119, *p* = .341, lo que indica que el supuesto de homocedasticidad se cumplió.

**Independencia.** Las observaciones son independientes por diseño experimental: cada planta constituyó una unidad experimental distinta y la asignación de tratamientos fue completamente aleatoria.

### 3.3 Análisis de varianza

*Tabla 2*

*Tabla ANOVA para el efecto del tratamiento sobre el peso seco de las plantas*

| Fuente de variación |  *GL* |    *SC*   |   *CM*   |   *F*  |   *p*  |  *η²*  |
|:--------------------|:-----:|:---------:|:--------:|:------:|:------:|:------:|
| Tratamientos        |   2   |   3.7663  |  1.8832  |  4.846 |  .016  |  .264  |
| Error (Residual)    |  27   |  10.4921  |  0.3886  |   —    |   —    |   —    |
| Total               |  29   |  14.2584  |    —     |   —    |   —    |   —    |

*Nota.* GL = grados de libertad; SC = suma de cuadrados; CM = cuadrado medio; η² = eta cuadrado (tamaño del efecto). El valor crítico de F para α = .05 con GL(2, 27) es F_c = 3.354.

Se realizó un análisis de varianza de un factor para examinar el efecto del tratamiento en el peso seco de las plantas. Los resultados indicaron que **existe un efecto significativo del tratamiento**, *F*(2, 27) = 4.846, *p* = .016, η² = .26.

El tamaño del efecto η² = .26 indica que el 26.4% de la variabilidad total en el peso seco de las plantas es explicado por el tipo de tratamiento, lo que corresponde a un efecto **grande** según los criterios de Cohen (1988), quien establece η² ≥ .14 como umbral para efectos grandes.

### 3.4 Intervalos de confianza al 95% para las medias

Los intervalos de confianza al 95% para las medias de cada grupo fueron: control [4.615, 5.449], tratamiento 1 [4.093, 5.229] y tratamiento 2 [5.209, 5.843]. La ausencia de solapamiento entre los intervalos del tratamiento 1 y el tratamiento 2 proporciona evidencia visual adicional de una diferencia significativa entre estos dos grupos.

---

## 4. Discusión de supuestos y alternativas

### 4.1 Consecuencias de la violación de supuestos

| Supuesto violado       | Consecuencia                                                                 | Alternativa recomendada                              |
|:-----------------------|:-----------------------------------------------------------------------------|:-----------------------------------------------------|
| Normalidad             | El estadístico F pierde robustez; los p-valores se vuelven inexactos         | Prueba de Kruskal-Wallis (no paramétrica)             |
| Homocedasticidad       | Inflación del error Tipo I; el CME subestima o sobreestima la varianza real  | Welch's ANOVA (ajusta los grados de libertad)        |
| Independencia          | Correlación entre residuos; el modelo lineal es estructuralmente inválido    | ANOVA de medidas repetidas o modelos mixtos           |

En el presente estudio, los tres supuestos fueron satisfechos, por lo que el ANOVA paramétrico de una vía es el método apropiado.

---

## 5. Conclusión

Los resultados del análisis de varianza indicaron un efecto estadísticamente significativo del tratamiento sobre el peso seco de las plantas, *F*(2, 27) = 4.846, *p* = .016, η² = .26. El tratamiento 2 produjo el mayor peso seco promedio (*M* = 5.526 g), seguido por el grupo control (*M* = 5.032 g) y el tratamiento 1 (*M* = 4.661 g). Se rechaza la hipótesis nula de igualdad de medias a un nivel de significancia de .05.

---

## Referencias

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

R Core Team. (2023). *R: A language and environment for statistical computing*. R Foundation for Statistical Computing. https://www.R-project.org/

Field, A. (2018). *Discovering statistics using IBM SPSS statistics* (5th ed.). SAGE Publications.

Montgomery, D. C. (2017). *Design and analysis of experiments* (9th ed.). Wiley.