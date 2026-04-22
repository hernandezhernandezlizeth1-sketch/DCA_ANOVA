"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: visualizer.py
Propósito: FASE 5 (Waterfall) - Implementación de visualizaciones.
           Genera TODOS los gráficos requeridos por la tarea:
             1. Boxplot comparativo
             2. Histogramas con curva de densidad
             3. Q-Q plots de normalidad
             4. Distribución F con zonas de rechazo
           Todos los gráficos se guardan en la carpeta outputs/.
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats
from scipy.stats import gaussian_kde
import os

from config import (GRUPOS, ETIQUETAS_GRUPOS, COLORES, ALPHA,
                    OUTPUT_DIR, FIGSIZE_SIMPLE, FIGSIZE_MULTIPLE, DPI)


class Visualizer:
    """
    Clase responsable de generar todos los gráficos del análisis.

    Centralizar los gráficos en una clase permite:
      - Estilo visual consistente (misma paleta, fuentes, tamaños)
      - Fácil modificación del estilo sin tocar el análisis
      - Generación selectiva o completa de figuras

    Cada método genera UN gráfico, lo guarda en disco y opcionalmente
    lo muestra en pantalla. El método generar_todos() los ejecuta en orden.

    Atributos:
        grupos_data (dict): Arrays de datos por grupo
        desc_resultados (dict): Estadísticos descriptivos
        anova_resultados (dict): Resultados del ANOVA (para F plot)
    """

    def __init__(self, grupos_data: dict,
                 desc_resultados: dict = None,
                 anova_resultados: dict = None):
        """
        Args:
            grupos_data (dict): Datos por grupo
            desc_resultados (dict): Output de DescriptiveStats.get_resultados()
            anova_resultados (dict): Output de AnovaAnalysis.get_resultados()
        """
        self.grupos_data = grupos_data
        self.desc_resultados = desc_resultados or {}
        self.anova_resultados = anova_resultados or {}

        # Configurar estilo global de matplotlib
        # (afecta a todos los gráficos generados después de esta línea)
        self._configurar_estilo()

    def _configurar_estilo(self):
        """
        Configura el estilo visual global de todos los gráficos.
        Usar un estilo consistente es esencial para reportes académicos.
        """
        plt.rcParams.update({
            "figure.facecolor": "white",      # Fondo blanco para impresión
            "axes.facecolor": "#F8F9FA",       # Gris muy claro en el panel
            "axes.grid": True,                 # Cuadrícula activada
            "grid.alpha": 0.4,                 # Cuadrícula semi-transparente
            "grid.linestyle": "--",
            "axes.spines.top": False,          # Sin borde superior
            "axes.spines.right": False,        # Sin borde derecho
            "font.family": "DejaVu Sans",
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        })

    def _guardar(self, fig, nombre_archivo: str):
        """
        Guarda la figura en disco en formato PNG de alta resolución.
        Centralizar el guardado evita olvidar parámetros de calidad.
        """
        ruta = os.path.join(OUTPUT_DIR, nombre_archivo)
        fig.savefig(ruta, dpi=DPI, bbox_inches="tight",
                    facecolor="white", edgecolor="none")
        plt.close(fig)  # Liberar memoria (importante si se generan muchas figuras)
        print(f"  ✓ Guardado: {ruta}")

    # =========================================================================
    # GRÁFICO 1: BOXPLOT COMPARATIVO
    # =========================================================================
    def boxplot_comparativo(self, mostrar=False):
        """
        Genera el boxplot comparativo de los 3 grupos.

        El boxplot muestra simultáneamente:
          - Mediana (línea central): tendencia central robusta
          - Caja (Q1-Q3): rango intercuartílico, 50% central de los datos
          - Bigotes: extensión hasta 1.5×IQR (valores usuales)
          - Puntos individuales (fliers): valores atípicos potenciales
          - Muesca (notch): intervalo de confianza de la mediana
            → si las muescas NO se solapan, medianas significativamente diferentes

        Interpretación para el reporte:
          Observar si las cajas/medianas se solapan entre grupos
        """
        fig, ax = plt.subplots(figsize=FIGSIZE_SIMPLE)

        # Preparar datos como lista de arrays en el orden definido
        datos_lista = [self.grupos_data[g] for g in GRUPOS]
        etiquetas = [ETIQUETAS_GRUPOS[g] for g in GRUPOS]
        colores_lista = [COLORES[g] for g in GRUPOS]

        # Crear boxplot con notches (muescas para IC de la mediana)
        bp = ax.boxplot(
            datos_lista,
            notch=True,           # Muescas = IC 95% de la mediana
            patch_artist=True,    # Relleno de color en las cajas
            widths=0.5,
            medianprops={"color": "black", "linewidth": 2.5},
            whiskerprops={"linewidth": 1.5},
            capprops={"linewidth": 1.5},
            flierprops={"marker": "o", "markersize": 6, "alpha": 0.7}
        )

        # Aplicar colores a cada caja individualmente
        for patch, color in zip(bp["boxes"], colores_lista):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)

        # Superponer puntos individuales para ver la distribución real
        # Jitter (variación horizontal aleatoria) evita que se apilen
        np.random.seed(42)  # Reproducibilidad del jitter
        for i, (grupo, datos) in enumerate(zip(GRUPOS, datos_lista)):
            jitter = np.random.uniform(-0.12, 0.12, len(datos))
            ax.scatter(
                np.full(len(datos), i + 1) + jitter,
                datos,
                color=COLORES[grupo], s=40, alpha=0.85,
                zorder=5, edgecolors="white", linewidths=0.5
            )

        ax.set_xticklabels(etiquetas)
        ax.set_ylabel("Peso seco de la planta (g)")
        ax.set_xlabel("Grupo de tratamiento")
        ax.set_title("Comparación de Peso Seco por Tratamiento\n"
                     "(PlantGrowth dataset)", fontweight="bold", pad=15)

        # Leyenda con colores de cada grupo
        handles = [mpatches.Patch(color=COLORES[g], alpha=0.75,
                                  label=ETIQUETAS_GRUPOS[g]) for g in GRUPOS]
        ax.legend(handles=handles, loc="upper right", framealpha=0.9)

        plt.tight_layout()
        self._guardar(fig, "01_boxplot_comparativo.png")

        if mostrar:
            plt.show()

    # =========================================================================
    # GRÁFICO 2: HISTOGRAMAS CON CURVA DE DENSIDAD
    # =========================================================================
    def histogramas_densidad(self, mostrar=False):
        """
        Genera histogramas con curva de densidad KDE para cada grupo.

        La curva KDE (Kernel Density Estimation) es una versión suavizada
        del histograma que muestra la forma de la distribución sin depender
        del número de bins. Complementa el Q-Q plot para evaluar normalidad.

        Subplots: un panel por grupo, todos con el mismo eje x para comparación.
        """
        fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_MULTIPLE, sharey=False)
        fig.suptitle("Distribución del Peso Seco por Grupo\n"
                     "Histograma + Curva de Densidad KDE",
                     fontsize=14, fontweight="bold", y=1.01)

        for ax, grupo in zip(axes, GRUPOS):
            datos = self.grupos_data[grupo]
            color = COLORES[grupo]

            # Histograma: bins="auto" deja que numpy elija el número óptimo
            ax.hist(datos, bins="auto", color=color, alpha=0.6,
                    edgecolor="white", linewidth=0.8, density=True,
                    label="Histograma")

            # Curva KDE: estimación no paramétrica de la densidad
            # Genera puntos x desde mín-0.5 hasta máx+0.5 para la curva
            x_kde = np.linspace(min(datos) - 0.5, max(datos) + 0.5, 200)
            kde = gaussian_kde(datos, bw_method="scott")  # Ancho de banda automático
            ax.plot(x_kde, kde(x_kde), color=color, linewidth=2.5, label="KDE")

            # Línea vertical en la media del grupo
            media = np.mean(datos)
            ax.axvline(media, color="black", linestyle="--", linewidth=1.5,
                       alpha=0.8, label=f"Media = {media:.2f}")

            ax.set_title(ETIQUETAS_GRUPOS[grupo], fontweight="bold")
            ax.set_xlabel("Peso seco (g)")
            ax.set_ylabel("Densidad")
            ax.legend(fontsize=8, loc="upper right")

        plt.tight_layout()
        self._guardar(fig, "02_histogramas_densidad.png")

        if mostrar:
            plt.show()

    # =========================================================================
    # GRÁFICO 3: Q-Q PLOTS DE NORMALIDAD
    # =========================================================================
    def qqplots_normalidad(self, mostrar=False):
        """
        Genera Q-Q plots (cuantil-cuantil) para cada grupo.

        Un Q-Q plot compara los cuantiles observados (eje y) contra los
        cuantiles teóricos de una distribución normal (eje x).

        Interpretación:
          - Puntos sobre la línea diagonal → distribución normal
          - Curvatura en cola derecha → asimetría positiva (sesgo a la derecha)
          - Curvatura en cola izquierda → asimetría negativa
          - Puntos alejados en los extremos → colas pesadas (leptocúrtica)

        Complementa la prueba Shapiro-Wilk con evidencia VISUAL.
        """
        fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_MULTIPLE)
        fig.suptitle("Q-Q Plots de Normalidad por Grupo\n"
                     "(Los puntos sobre la línea indican normalidad)",
                     fontsize=14, fontweight="bold", y=1.01)

        for ax, grupo in zip(axes, GRUPOS):
            datos = self.grupos_data[grupo]
            color = COLORES[grupo]

            # stats.probplot retorna: (cuantiles teóricos, cuantiles observados),
            # y los parámetros de la línea de referencia
            (q_teoricos, q_observados), (pendiente, intercepto, r) = \
                stats.probplot(datos, dist="norm")

            # Línea de referencia (distribución perfectamente normal)
            x_linea = np.array([min(q_teoricos), max(q_teoricos)])
            ax.plot(x_linea, pendiente * x_linea + intercepto,
                    color="gray", linewidth=1.5, linestyle="-",
                    label="Referencia normal", zorder=1)

            # Puntos observados
            ax.scatter(q_teoricos, q_observados, color=color,
                       s=55, alpha=0.9, zorder=5, edgecolors="white",
                       linewidths=0.5)

            # R² de la línea (cuanto más cercano a 1 → más normal)
            ax.set_title(f"{ETIQUETAS_GRUPOS[grupo]}\nR² = {r**2:.4f}",
                         fontweight="bold")
            ax.set_xlabel("Cuantiles teóricos (Normal)")
            ax.set_ylabel("Cuantiles observados")
            ax.legend(fontsize=8)

        plt.tight_layout()
        self._guardar(fig, "03_qqplots_normalidad.png")

        if mostrar:
            plt.show()

    # =========================================================================
    # GRÁFICO 4: DISTRIBUCIÓN F CON ZONA DE RECHAZO
    # =========================================================================
    def distribucion_f(self, mostrar=False):
        """
        Genera el gráfico de la distribución F con zonas de aceptación/rechazo.

        Muestra visualmente la REGLA DE DECISIÓN del ANOVA:
          - Zona verde (izquierda del F crítico): región de aceptación de H₀
          - Zona roja (derecha del F crítico): región de rechazo de H₀
          - Línea azul: F calculado con los datos reales
          - Línea roja discontinua: F crítico teórico

        Responde directamente al punto A.3 de la tarea.
        """
        if not self.anova_resultados:
            print("  ⚠ Requiere resultados del ANOVA. Llama primero a AnovaAnalysis.")
            return

        GL_trat = self.anova_resultados.get("GL_trat", 2)
        GL_error = self.anova_resultados.get("GL_error", 27)
        F_calculado = self.anova_resultados.get("F", 4.85)
        f_critico = self.anova_resultados.get("f_critico", 3.35)
        p_valor = self.anova_resultados.get("p_valor", 0.016)

        fig, ax = plt.subplots(figsize=(10, 5))

        # Rango de x: de 0 hasta el máximo entre F_calculado*1.5 y f_crítico*1.5
        x_max = max(F_calculado * 1.6, f_critico * 1.8)
        x = np.linspace(0.001, x_max, 1000)

        # Curva de la distribución F(GL_trat, GL_error)
        y = stats.f.pdf(x, GL_trat, GL_error)

        # Trazar la curva completa
        ax.plot(x, y, color="#333333", linewidth=2.5,
                label=f"Distribución F({GL_trat}, {GL_error})")

        # ── ZONA DE ACEPTACIÓN (izquierda del F crítico) ──────────────────
        x_acept = x[x <= f_critico]
        y_acept = stats.f.pdf(x_acept, GL_trat, GL_error)
        ax.fill_between(x_acept, y_acept, alpha=0.25, color="#27AE60",
                        label=f"Zona aceptación H₀ (1-α = {1-ALPHA:.0%})")

        # ── ZONA DE RECHAZO (derecha del F crítico) ───────────────────────
        x_rechazo = x[x >= f_critico]
        y_rechazo = stats.f.pdf(x_rechazo, GL_trat, GL_error)
        ax.fill_between(x_rechazo, y_rechazo, alpha=0.35, color="#E74C3C",
                        label=f"Zona rechazo H₀ (α = {ALPHA})")

        # ── F CRÍTICO (línea vertical de corte) ───────────────────────────
        ax.axvline(f_critico, color="#E74C3C", linestyle="--",
                   linewidth=2, label=f"F crítico = {f_critico:.4f}")
        ax.text(f_critico + 0.05, ax.get_ylim()[1] * 0.5,
                f"F_c = {f_critico:.2f}", color="#E74C3C",
                fontsize=9, va="center")

        # ── F CALCULADO (con los datos reales) ────────────────────────────
        ax.axvline(F_calculado, color="#2980B9", linestyle="-",
                   linewidth=2.5, label=f"F calculado = {F_calculado:.4f}")
        ax.text(F_calculado + 0.05, ax.get_ylim()[1] * 0.7,
                f"F = {F_calculado:.2f}", color="#2980B9",
                fontsize=9, va="center", fontweight="bold")

        # ── ANOTACIÓN DEL P-VALOR ─────────────────────────────────────────
        ax.annotate(f"p = {p_valor:.4f}",
                    xy=(F_calculado, 0),
                    xytext=(F_calculado + 0.3, 0.15),
                    fontsize=9, color="#2980B9",
                    arrowprops={"arrowstyle": "->", "color": "#2980B9"})

        ax.set_xlabel(f"Estadístico F  (GL₁ = {GL_trat}, GL₂ = {GL_error})")
        ax.set_ylabel("Densidad de probabilidad")
        ax.set_title(
            f"Distribución F de Fisher — Regla de Decisión ANOVA\n"
            f"H₀: μ₁ = μ₂ = μ₃  |  α = {ALPHA}  |  "
            f"{'RECHAZA H₀' if p_valor < ALPHA else 'NO RECHAZA H₀'}",
            fontweight="bold", pad=12
        )
        ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
        ax.set_xlim(0, x_max)
        ax.set_ylim(bottom=0)

        plt.tight_layout()
        self._guardar(fig, "04_distribucion_F_fisher.png")

        if mostrar:
            plt.show()

    # =========================================================================
    # MÉTODO PRINCIPAL: GENERAR TODOS LOS GRÁFICOS
    # =========================================================================
    def generar_todos(self, mostrar=False):
        """
        Genera TODOS los gráficos en el orden correcto del análisis.
        Este es el método principal que debe llamarse desde main.py.

        Args:
            mostrar (bool): Si True, muestra los gráficos en pantalla
                            además de guardarlos. Útil en Jupyter.
        """
        print("\n" + "=" * 55)
        print("GENERANDO GRÁFICOS...")
        print("=" * 55)
        self.boxplot_comparativo(mostrar)
        self.histogramas_densidad(mostrar)
        self.qqplots_normalidad(mostrar)
        self.distribucion_f(mostrar)
        print(f"\n✓ Todos los gráficos guardados en: {OUTPUT_DIR}\n")