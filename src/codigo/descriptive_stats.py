"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: descriptive_stats.py
Propósito: FASE 2 (Waterfall) - Exploración de datos.
           Calcula todas las estadísticas descriptivas requeridas por la
           tarea: media, desviación estándar, CV, mínimo, máximo, mediana
           e intervalos de confianza. Genera la tabla resumen formateada.
=============================================================================
"""

import numpy as np
import pandas as pd
from scipy import stats
from config import GRUPOS, ETIQUETAS_GRUPOS, VAR_RESPUESTA, VAR_GRUPO, ALPHA


class DescriptiveStats:
    """
    Clase responsable del cálculo de estadísticas descriptivas por grupo.

    En Waterfall, esta clase representa la FASE DE DISEÑO DETALLADO para
    la exploración de datos. Se ejecuta después de DataLoader y antes
    del análisis formal (ANOVA), siguiendo el flujo secuencial:
      Datos → Descripción → Supuestos → ANOVA → Reporte

    Atributos:
        grupos_data (dict): Arrays de datos por grupo
        tabla (pd.DataFrame): Tabla completa de estadísticos calculados
    """

    def __init__(self, grupos_data: dict):
        """
        Recibe el diccionario de datos por grupo (output de DataLoader).

        Args:
            grupos_data (dict): {'ctrl': array, 'trt1': array, 'trt2': array}
        """
        self.grupos_data = grupos_data
        self.tabla = None       # Se llenará en calcular()
        self._resultados = {}   # Almacena resultados crudos por grupo
        self.calcular()         # Calcula todo al instanciar

    def calcular(self):
        """
        Calcula todas las estadísticas para cada grupo y construye la tabla.

        Estadísticos calculados:
          - n: número de observaciones
          - media: promedio aritmético (Ȳᵢ)
          - mediana: valor central
          - desv_std: desviación estándar muestral (divide entre n-1)
          - varianza: cuadrado de la desviación estándar
          - cv_pct: coeficiente de variación en % (desv_std/media × 100)
                    Interpreta dispersión relativa; <15% = baja variabilidad
          - minimo, maximo: rango de los datos
          - rango: maximo - minimo
          - ic_inferior, ic_superior: intervalo de confianza 95% para la media
                    Fórmula: Ȳ ± t(α/2, n-1) × (s/√n)
                    Usa distribución t porque n=10 es pequeño (no normal z)
          - error_std: error estándar de la media = s/√n
        """
        filas = []  # Acumula una fila por grupo

        for grupo in GRUPOS:
            datos = self.grupos_data[grupo]
            n = len(datos)
            media = np.mean(datos)
            mediana = np.median(datos)
            desv_std = np.std(datos, ddof=1)    # ddof=1 → divisor n-1 (muestral)
            varianza = np.var(datos, ddof=1)
            cv = (desv_std / media) * 100        # CV en porcentaje
            minimo = np.min(datos)
            maximo = np.max(datos)
            rango = maximo - minimo
            error_std = desv_std / np.sqrt(n)   # Error estándar de la media

            # Intervalo de confianza 95% usando distribución t de Student
            # t_critico: valor t para α/2=0.025 con n-1 grados de libertad
            t_critico = stats.t.ppf(1 - ALPHA / 2, df=n - 1)
            ic_inferior = media - t_critico * error_std
            ic_superior = media + t_critico * error_std

            # Guardar resultados crudos para acceso programático posterior
            self._resultados[grupo] = {
                "n": n, "media": media, "mediana": mediana,
                "desv_std": desv_std, "varianza": varianza,
                "cv_pct": cv, "minimo": minimo, "maximo": maximo,
                "rango": rango, "error_std": error_std,
                "ic_inferior": ic_inferior, "ic_superior": ic_superior,
                "t_critico": t_critico
            }

            # Agregar fila con etiqueta legible para la tabla
            filas.append({
                "Grupo": ETIQUETAS_GRUPOS[grupo],
                "n": n,
                "Media": round(media, 4),
                "Mediana": round(mediana, 4),
                "Desv. Std": round(desv_std, 4),
                "Varianza": round(varianza, 4),
                "CV (%)": round(cv, 2),
                "Mínimo": round(minimo, 2),
                "Máximo": round(maximo, 2),
                "Rango": round(rango, 2),
                "Error Std": round(error_std, 4),
                "IC 95% Inf": round(ic_inferior, 4),
                "IC 95% Sup": round(ic_superior, 4),
            })

        # Convertir lista de diccionarios a DataFrame para fácil manipulación
        self.tabla = pd.DataFrame(filas).set_index("Grupo")

    def imprimir_tabla(self):
        """
        Imprime la tabla de estadísticos descriptivos en consola
        con formato legible. Útil para verificación y para el reporte.
        """
        print("=" * 70)
        print("ESTADÍSTICAS DESCRIPTIVAS POR GRUPO")
        print(f"Nivel de confianza: {int((1-ALPHA)*100)}%  |  α = {ALPHA}")
        print("=" * 70)
        # Transponer para mejor legibilidad: grupos como columnas
        print(self.tabla.T.to_string())
        print()

    def imprimir_interpretacion(self):
        """
        Imprime una interpretación automática de los estadísticos clave.
        Identifica el grupo con mayor/menor media y evalúa los CVs.
        """
        print("─" * 50)
        print("INTERPRETACIÓN DE ESTADÍSTICAS DESCRIPTIVAS")
        print("─" * 50)

        medias = {g: self._resultados[g]["media"] for g in GRUPOS}
        grupo_max = max(medias, key=medias.get)
        grupo_min = min(medias, key=medias.get)

        print(f"• Grupo con mayor media: {ETIQUETAS_GRUPOS[grupo_max]} "
              f"(Ȳ = {medias[grupo_max]:.4f} g)")
        print(f"• Grupo con menor media: {ETIQUETAS_GRUPOS[grupo_min]} "
              f"(Ȳ = {medias[grupo_min]:.4f} g)")
        print(f"• Diferencia entre extremos: "
              f"{medias[grupo_max] - medias[grupo_min]:.4f} g\n")

        print("Coeficientes de Variación (CV):")
        for grupo in GRUPOS:
            cv = self._resultados[grupo]["cv_pct"]
            # Clasificación estándar del CV en ciencias agrícolas
            nivel = "Baja" if cv < 15 else ("Moderada" if cv < 30 else "Alta")
            print(f"  • {ETIQUETAS_GRUPOS[grupo]}: CV = {cv:.2f}% → "
                  f"Variabilidad {nivel}")

        print()
        print("Intervalos de Confianza al 95%:")
        for grupo in GRUPOS:
            r = self._resultados[grupo]
            print(f"  • {ETIQUETAS_GRUPOS[grupo]}: "
                  f"[{r['ic_inferior']:.4f}, {r['ic_superior']:.4f}]")
        print()

    def get_resultados(self):
        """
        Retorna el diccionario completo de resultados crudos.
        Usado por otros módulos (ej: Visualizer necesita las medias para IC).
        """
        return self._resultados

    def get_tabla(self):
        """Retorna el DataFrame de la tabla de estadísticos."""
        return self.tabla.copy()