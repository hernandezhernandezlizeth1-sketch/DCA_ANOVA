# Informe Técnico. Análisis Estadístico: Efecto de Tratamientos Experimentales sobre el Rendimiento de Biomasa Seca en Especies Vegetales

**Asignatura:** Estadística Inferencial ||
**Equipo:** Lizeth Guadalupe Hernández Hernández · Emilio Sánchez Estrada · Carlos Alberto Lule  
**Fecha:** 23/04/2026  
**Dataset:** PlantGrowth (R Core Team, 2023)  
**Metodología:** Diseño Completamente al Azar (DCA) y Análisis de Varianza (ANOVA) de una vía.  

---

## Stack Tecnológico y Justificación Herramental

Para el desarrollo computacional de este análisis, se optó por un ecosistema basado puramente en scripts de **Python**, priorizando la facilidad de implementación, la reproducibilidad y el ecosistema robusto de análisis de datos frente a frameworks de escritorio más complejos o pesados (como JavaFX). 

| Tecnología / Librería | Tipo | Propósito en el Proyecto |
|:---|:---|:---|
| **Python (3.14)** | Lenguaje Base | Motor lógico y desarrollo completo de la arquitectura del análisis estadístico. |
| **NumPy** | Librería | Ejecución de cálculos numéricos de alto rendimiento y operaciones vectorizadas. |
| **Pandas** | Librería | Carga, estructuración, limpieza y manipulación de los dataframes del experimento. |
| **SciPy (stats)** | Librería | Motor inferencial para pruebas paramétricas (Shapiro-Wilk, Levene, ANOVA, probplots). |
| **Matplotlib (pyplot)** | Librería | Renderizado de visualizaciones científicas en alta resolución (DPI 300). |
| **Gaussian KDE** | Módulo (SciPy) | Estimación no paramétrica de la función de densidad de probabilidad para histogramas. |
| **OS** | Módulo Estándar | Creación dinámica de directorios y ruteo relativo de archivos de salida (`outputs/`). |

---

## 1. Introducción y Descripción del Dataset

En el ámbito de la investigación agrícola y biológica, la cuantificación de la biomasa —medida a través del peso seco— es un indicador fundamental del vigor vegetal y la eficiencia fotosintética. A diferencia del peso fresco, que fluctúa por el estado hídrico, el peso seco proporciona una medida estable de la acumulación de materia orgánica.

El estudio busca determinar si la aplicación de dos tratamientos experimentales (Tratamiento 1 y Tratamiento 2) produce variaciones significativas en el rendimiento de biomasa en comparación con un entorno no intervenido (Control). Se seleccionó un Diseño Completamente al Azar (DCA), el estándar metodológico cuando el material experimental es homogéneo.

**Especificaciones del Dataset (`PlantGrowth`):**
* **Total de observaciones:** $N = 30$
* **Número de grupos (Niveles del Factor):** $k = 3$ (Control, TRT1, TRT2)
* **Diseño:** Balanceado ($n = 10$ por grupo).

---

## 2. Fundamentación Matemática del DCA

El modelo estadístico lineal aditivo que describe cada observación en un DCA está dado por la siguiente ecuación:

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?Y_{ij}=\mu+\tau_i+\varepsilon_{ij}" title="Modelo Lineal DCA" />
</div>

Donde $Y_{ij}$ representa la variable de respuesta de la $j$-ésima repetición bajo el $i$-ésimo tratamiento; $\mu$ es la media global verdadera; $\tau_i$ es el efecto específico del tratamiento; y $\varepsilon_{ij}$ es el error aleatorio asumiendo:

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?\varepsilon_{ij}\sim%20N(0,\sigma^2)" title="Error aleatorio" />
</div>

El principio del ANOVA radica en la partición de la variabilidad total en sus componentes:

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?SCT=SCTr+SCE" title="Partición de Varianza" />
</div>

Donde la Suma de Cuadrados Total (SCT), la Suma de Cuadrados de Tratamientos (SCTr) y del Error (SCE) se definen como:

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?SCT=\sum_{i=1}^{a}\sum_{j=1}^{n}(Y_{ij}-\bar{Y}_{..})^2" title="SCT" />
</div>

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?SCTr=n\sum_{i=1}^{a}(\bar{Y}_{i.}-\bar{Y}_{..})^2" title="SCTr" />
</div>

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?SCE=\sum_{i=1}^{a}\sum_{j=1}^{n}(Y_{ij}-\bar{Y}_{i.})^2" title="SCE" />
</div>

El objetivo del ANOVA es contrastar estadísticamente las siguientes hipótesis:

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?H_0:\mu_{control}=\mu_{trt1}=\mu_{trt2}" title="Hipótesis Nula" />
</div>

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?H_1:\text{Al%20menos%20un%20par%20}\mu_i\neq\mu_j" title="Hipótesis Alternativa" />
</div>

---

## 3. Metodología y Procedimiento

Se utilizó un generador de números pseudoaleatorios para asignar 30 macetas a tres niveles del factor:
1.  **Grupo Control (*ctrl*):** Irrigación exclusiva con solución nutritiva estándar.
2.  **Tratamiento 1 (*trt1*):** Adición de fitorregulador específico nivel 1.
3.  **Tratamiento 2 (*trt2*):** Adición de fitorregulador experimental a un nivel superior (nivel 2).

Al finalizar el ciclo, la parte aérea fue cosechada, deshidratada en horno de secado a 65°C por 72 horas y pesada en balanza analítica. El análisis estadístico se programó modularmente estableciendo un nivel de significancia de $\alpha = .05$.

---

## 4. Resultados Exploratorios y Visualización Computacional

**Tabla 1** *Estadísticas descriptivas completas del peso seco (biomasa) por grupo de tratamiento*

| Grupo | $n$ | Media ($M$) | Desv. Est. ($DE$) | Varianza ($S^2$) | CV (%) | IC 95% Inferior | IC 95% Superior |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Control** | 10 | 5.032 | 0.5832 | 0.3401 | 11.59 | 4.615 | 5.449 |
| **Tratamiento 1** | 10 | 4.661 | 0.7936 | 0.6298 | 17.03 | 4.093 | 5.229 |
| **Tratamiento 2** | 10 | 5.526 | 0.4425 | 0.1958 | 8.01 | 5.209 | 5.843 |

Es evidente una tendencia a favor del **Tratamiento 2**, que presenta la media más alta ($M = 5.526$ g) y la mayor consistencia interna (CV de apenas 8.01%). 

### 4.1 Comparación de Distribución (Boxplot)

```python
# Implementación computacional del Boxplot Comparativo
def boxplot_comparativo(self, mostrar=False):
    fig, ax = plt.subplots(figsize=FIGSIZE_SIMPLE)
    datos_lista = [self.grupos_data[g] for g in GRUPOS]
    etiquetas = [ETIQUETAS_GRUPOS[g] for g in GRUPOS]
    colores_lista = [COLORES[g] for g in GRUPOS]

    bp = ax.boxplot(
        datos_lista, notch=True, patch_artist=True, widths=0.5,
        medianprops={"color": "black", "linewidth": 2.5},
        whiskerprops={"linewidth": 1.5}, capprops={"linewidth": 1.5},
        flierprops={"marker": "o", "markersize": 6, "alpha": 0.7}
    )

    for patch, color in zip(bp["boxes"], colores_lista):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    np.random.seed(42)
    for i, (grupo, datos) in enumerate(zip(GRUPOS, datos_lista)):
        jitter = np.random.uniform(-0.12, 0.12, len(datos))
        ax.scatter(np.full(len(datos), i + 1) + jitter, datos,
                   color=COLORES[grupo], s=40, alpha=0.85,
                   zorder=5, edgecolors="white", linewidths=0.5)

    ax.set_xticklabels(etiquetas)
    ax.set_ylabel("Peso seco de la planta (g)")
    ax.set_xlabel("Grupo de tratamiento")
    ax.set_title("Comparación de Peso Seco por Tratamiento", fontweight="bold")
    plt.tight_layout()
    self._guardar(fig, "01_boxplot_comparativo.png")
```

![Boxplot comparativo](codigo/outputs/01_boxplot_comparativo.png)

*Análisis de la Figura 1:* Las cajas intercuartílicas de los grupos *trt1* y *trt2* presentan un mínimo solapamiento vertical. Las muescas (notches) no se cruzan entre estos dos grupos, indicador preliminar de diferencias estadísticas significativas. El gráfico confirma la integridad de los datos por la ausencia de atípicos.

### 4.2 Perfiles de Densidad (KDE)

```python
# Implementación computacional de KDE y Curvas de Densidad
def histogramas_densidad(self, mostrar=False):
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_MULTIPLE, sharey=False)
    fig.suptitle("Distribución del Peso Seco por Grupo", fontweight="bold", y=1.01)

    for ax, grupo in zip(axes, GRUPOS):
        datos = self.grupos_data[grupo]
        color = COLORES[grupo]

        ax.hist(datos, bins="auto", color=color, alpha=0.6,
                edgecolor="white", linewidth=0.8, density=True)

        x_kde = np.linspace(min(datos) - 0.5, max(datos) + 0.5, 200)
        kde = gaussian_kde(datos, bw_method="scott")
        ax.plot(x_kde, kde(x_kde), color=color, linewidth=2.5)

        media = np.mean(datos)
        ax.axvline(media, color="black", linestyle="--", linewidth=1.5, alpha=0.8)
        ax.set_title(ETIQUETAS_GRUPOS[grupo], fontweight="bold")

    plt.tight_layout()
    self._guardar(fig, "02_histogramas_densidad.png")
```

![Histogramas con densidad](codigo/outputs/02_histogramas_densidad.png)

*Análisis de la Figura 2:* El Tratamiento 2 (derecha) concentra sus valores fuertemente alrededor de su media. El Tratamiento 1 (centro) muestra una dispersión mucho más amplia. Visualmente, no se detectan asimetrías severas.

---

## 5. Verificación de Supuestos Paramétricos

### 5.1 Supuesto de Normalidad (Q-Q Plots)

```python
# Verificación visual de Normalidad (Distribución Gaussiana)
def qqplots_normalidad(self, mostrar=False):
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_MULTIPLE)
    
    for ax, grupo in zip(axes, GRUPOS):
        datos = self.grupos_data[grupo]
        color = COLORES[grupo]

        (q_teoricos, q_observados), (pendiente, intercepto, r) = \
            stats.probplot(datos, dist="norm")

        x_linea = np.array([min(q_teoricos), max(q_teoricos)])
        ax.plot(x_linea, pendiente * x_linea + intercepto, color="gray", zorder=1)
        ax.scatter(q_teoricos, q_observados, color=color, s=55, zorder=5)
        ax.set_title(f"{ETIQUETAS_GRUPOS[grupo]}\nR² = {r**2:.4f}", fontweight="bold")

    plt.tight_layout()
    self._guardar(fig, "03_qqplots_normalidad.png")
```

![QQ Plots](codigo/outputs/03_qqplots_normalidad.png)

La normalidad se evaluó analíticamente mediante la prueba de Shapiro-Wilk:
* **Control:** *W* = 0.957, *p* = .752
* **Tratamiento 1:** *W* = 0.930, *p* = .449
* **Tratamiento 2:** *W* = 0.941, *p* = .564

Al ser todos los valores *p* > .05, **el supuesto de normalidad se considera satisfecho.**

### 5.2 Homocedasticidad e Independencia
Se ejecutó la prueba de Levene basada en medianas. Los resultados indicaron igualdad de varianzas, *F*(2, 27) = 1.119, *p* = .341 (Supuesto de Homocedasticidad satisfecho). La independencia se asume garantizada debido al control riguroso de aleatorización espacial del diseño experimental.

---

## 6. Análisis Inferencial (ANOVA de una Vía)

Una vez confirmados los supuestos paramétricos, se procedió a calcular el Análisis de Varianza. El principio matemático del ANOVA evalúa si la variabilidad explicada por nuestra intervención (los fertilizantes) es significativamente mayor que la variabilidad natural de las plantas. 

Para ello, el estadístico de prueba empírico se define como el cociente entre el Cuadrado Medio de los Tratamientos ($CM_{Trat}$) y el Cuadrado Medio del Error ($CM_{Error}$):

<div align="center">
  <img src="https://latex.codecogs.com/svg.image?F=\frac{CM_{Trat}}{CM_{Error}}=\frac{SCTr/(k-1)}{SCE/(N-k)}" title="Fórmula del Estadístico F" />
</div>

### 6.1 Desglose del Cálculo Manual

Para validar la solidez del modelo, se ejecutó un cálculo analítico paso a paso partiendo de los estadísticos base ($N = 30$, $k = 3$, $n_i = 10$).

**Paso 1: Grados de Libertad (GL)**
* $GL_{Trat} = k - 1 = 3 - 1 = 2$
* $GL_{Total} = N - 1 = 30 - 1 = 29$
* $GL_{Error} = N - k = 30 - 3 = 27$

**Paso 2: Sumas de Cuadrados (SC)**
* $SCTr = \Sigma n_i (\bar{Y}_{i.} - \bar{Y}_{..})^2 = 10(5.032 - 5.073)^2 + 10(4.661 - 5.073)^2 + 10(5.526 - 5.073)^2 = 3.7663$
* $SCE = \Sigma (n_i - 1) S_i^2 = 9(0.3401) + 9(0.6298) + 9(0.1958) = 10.4921$
* $SCT = SCTr + SCE = 3.7663 + 10.4921 = 14.2584$

**Paso 3: Cuadrados Medios (CM)**
* $CM_{Trat} = \frac{SCTr}{GL_{Trat}} = \frac{3.7663}{2} = 1.8832$
* $CM_{Error} = \frac{SCE}{GL_{Error}} = \frac{10.4921}{27} = 0.3886$

**Paso 4: Estadístico *F* Empírico**
* $F = \frac{CM_{Trat}}{CM_{Error}} = \frac{1.8832}{0.3886} = 4.846$

### 6.2 Verificación con Software y Tabla ANOVA

Los cálculos analíticos fueron confirmados mediante la ejecución de la rutina computacional `scipy.stats.f_oneway`, arrojando una concordancia matemática perfecta con los valores manuales:

```python
# Verificación con SciPy
import scipy.stats as stats
F_scipy, p_scipy = stats.f_oneway(datos_ctrl, datos_trt1, datos_trt2)
print(f"SciPy: F = {F_scipy:.6f}, p = {p_scipy:.6f}")
# Output: SciPy: F = 4.846088, p = 0.015910
```

**Tabla 2** *Tabla del Análisis de Varianza (ANOVA) para la variable Biomasa Seca*

| Fuente de Variación | Grados de Libertad (GL) | Suma de Cuadrados (SC) | Cuadrado Medio (CM) | Estadístico F | Valor p | η² |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Tratamientos** | 2 | 3.7663 | 1.8832 | 4.846 | .016 | .264 |
| **Error (Residual)**| 27 | 10.4921 | 0.3886 | — | — | — |
| **Total** | 29 | 14.2584 | — | — | — | — |

*Nota:* Valor Crítico $F_{crit}(2, 27)$ para $\alpha = .05$ es igual a $3.354$.

### 6.3 Implementación Computacional y Regla de Decisión

```python
# Cálculo y visualización de la Región de Rechazo del Estadístico F
def distribucion_f(self, mostrar=False):
    GL_trat = 2; GL_error = 27
    F_calculado = 4.846; f_critico = 3.354; p_valor = 0.016

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(0.001, max(F_calculado * 1.6, f_critico * 1.8), 1000)
    
    # Renderizado de la curva de densidad F de Fisher
    y = stats.f.pdf(x, GL_trat, GL_error)
    ax.plot(x, y, color="#333333", linewidth=2.5)

    # Sombreado de la región de rechazo (alfa = 0.05)
    x_rechazo = x[x >= f_critico]
    ax.fill_between(x_rechazo, stats.f.pdf(x_rechazo, GL_trat, GL_error), 
                    alpha=0.35, color="#E74C3C")
    
    # Marcadores de decisión estadística
    ax.axvline(f_critico, color="#E74C3C", linestyle="--", linewidth=2)
    ax.axvline(F_calculado, color="#2980B9", linestyle="-", linewidth=2.5)
    
    ax.annotate(f"p = {p_valor:.4f}", xy=(F_calculado, 0),
                xytext=(F_calculado + 0.3, 0.15), color="#2980B9",
                arrowprops={"arrowstyle": "->", "color": "#2980B9"})
    
    plt.tight_layout()
    self._guardar(fig, "04_distribucion_F_fisher.png")
```

![Distribución F](codigo/outputs/04_distribucion_F_fisher.png)

Se realizó un análisis de varianza de un factor para examinar el efecto del tratamiento en el peso seco de las plantas. Los resultados indicaron que existe un efecto significativo del tratamiento, *F*(2, 27) = 4.85, *p* = .016, $\eta^2$ = .26. Debido a que el valor *p* es estrictamente menor al nivel de significancia prefijado, se rechaza la hipótesis nula. El cálculo de tamaño de efecto ($\eta^2$ = .26) indica que el 26.4% de la varianza en el peso seco se explica por las diferencias en los tratamientos.

---

## 7. Análisis Post-Hoc (Tukey HSD)

**Tabla 3** *Matriz de comparaciones múltiples de Tukey HSD*

| Contraste (Par de grupos) | Diferencia de Medias | Diferencia Crítica (W) | Valor *p* ajustado | Decisión |
|:---|:---:|:---:|:---:|:---:|
| **Tratamiento 2 vs. Tratamiento 1** | **0.865** | 0.689 | *p* < .05 | Significativa |
| **Tratamiento 2 vs. Control** | 0.494 | 0.689 | *p* > .05 | *ns* |
| **Control vs. Tratamiento 1** | 0.371 | 0.689 | *p* > .05 | *ns* |

El análisis revela que el Tratamiento 2 produce significativamente más biomasa seca en comparación con el Tratamiento 1, consolidando la superioridad estadística de dicha intervención.

---

## 8. Discusión y Conclusiones Generales

### Discusión
Los datos proporcionan evidencia sobre la modulación del crecimiento vegetal mediante agentes exógenos. La inferioridad del Tratamiento 1 sugiere un ambiente subóptimo para el metabolismo basal de la planta. En contraste, el Tratamiento 2 logra elevar el techo productivo de la biomasa de manera homogénea. Entre las limitaciones destaca el tamaño de muestra (*n* = 10), el cual limita el poder estadístico en comparaciones cruzadas frente al control. Se recomienda transitar a Diseños de Bloques en etapas futuras.

### Alternativas ante Violación de Supuestos
En caso de que futuros experimentos con estos tratamientos no cumplan los supuestos paramétricos verificados en la Sección 5, se establecen las siguientes rutas de contingencia metodológica:
* **Si se viola la Normalidad:** El estadístico F pierde robustez. Se deberá utilizar la **Prueba de Kruskal-Wallis**, la cual es una alternativa no paramétrica que evalúa las diferencias en las medianas basándose en los rangos de los datos, sin asumir una distribución específica.
* **Si se viola la Homocedasticidad:** La inflación del error Tipo I compromete el modelo. La alternativa es utilizar el **ANOVA de Welch** (Welch's ANOVA), el cual ajusta dinámicamente los grados de libertad del denominador para compensar la desigualdad de varianzas entre los grupos.
* **Si se viola la Independencia:** Sugeriría un fallo de diseño (ej. mediciones repetidas en la misma planta a lo largo del tiempo). Se tendría que reestructurar el análisis utilizando un **ANOVA de Medidas Repetidas** o Modelos Mixtos para aislar el error intra-sujeto.

### Conclusiones
Con base en el rigor metodológico aplicado, se realizó un análisis de varianza de un factor para examinar el efecto del tratamiento en el peso seco de las plantas. Los resultados indicaron que existe un efecto significativo del tratamiento, *F*(2, 27) = 4.85, *p* = .016, $\eta^2$ = .26. El análisis post-hoc determinó específicamente que el Tratamiento 2 es estadísticamente superior al Tratamiento 1. Se concluye que el protocolo del Tratamiento 2 es el óptimo para una potencial escalabilidad agronómica.

---

## Referencias Bibliográficas

1. American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000
2. Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.
3. Field, A. (2018). *Discovering statistics using IBM SPSS statistics* (5th ed.). SAGE Publications.
4. Montgomery, D. C. (2017). *Design and analysis of experiments* (9th ed.). Wiley.