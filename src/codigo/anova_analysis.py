"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: anova_analysis.py
Propósito: FASE 4 (Waterfall) - Análisis principal.
           Realiza el ANOVA de una vía con:
             a) Cálculo manual paso a paso (para entender la matemática)
             b) Verificación con scipy (para confirmar exactitud)
           Genera la tabla ANOVA completa e interpreta resultados.
=============================================================================
"""

import numpy as np
import pandas as pd
from scipy import stats
from config import GRUPOS, ETIQUETAS_GRUPOS, ALPHA


class AnovaAnalysis:
    """
    Clase responsable del Análisis de Varianza (ANOVA) de una vía.

    MODELO ESTADÍSTICO DEL DCA:
    ───────────────────────────
    Yᵢⱼ = μ + τᵢ + εᵢⱼ

    Donde:
      Yᵢⱼ  = j-ésima observación del i-ésimo tratamiento
      μ    = media general poblacional (constante)
      τᵢ   = efecto del i-ésimo tratamiento (τᵢ = μᵢ - μ)
      εᵢⱼ  = error aleatorio (εᵢⱼ ~ N(0, σ²))

    HIPÓTESIS:
    ──────────
      H₀: μ₁ = μ₂ = μ₃ (todos los tratamientos tienen igual efecto)
      H₁: Al menos un μᵢ ≠ μⱼ (al menos un tratamiento difiere)

    TABLA ANOVA:
    ────────────
    Fuente    | GL    | SC       | CM       | F         | p
    ──────────|───────|──────────|──────────|───────────|────
    Trat.     | k-1   | SCTrat   | CMTrat   | CMT/CME   | p
    Error     | N-k   | SCError  | CMError  | -         | -
    Total     | N-1   | SCTotal  | -        | -         | -

    Atributos:
        grupos_data (dict): Arrays de datos por grupo
        tabla_anova (pd.DataFrame): Tabla ANOVA completa
        eta_cuadrado (float): Tamaño del efecto η²
        resultado_scipy (tuple): Verificación con scipy
    """

    def __init__(self, grupos_data: dict):
        """
        Args:
            grupos_data (dict): {'ctrl': array, 'trt1': array, 'trt2': array}
        """
        self.grupos_data = grupos_data
        self.tabla_anova = None
        self.eta_cuadrado = None
        self.f_critico = None
        self._calculo_manual = {}   # Almacena todos los pasos del cálculo
        self._scipy_result = None   # Resultado de verificación con scipy
        self._ejecutar_anova()      # Realiza el análisis completo

    def _ejecutar_anova(self):
        """
        Orquesta el flujo completo del ANOVA en orden lógico:
        1. Cálculo manual (mostrando cada paso)
        2. Verificación con scipy
        3. Construcción de tabla
        4. Tamaño del efecto
        """
        print("=" * 65)
        print("ANÁLISIS DE VARIANZA (ANOVA) DE UNA VÍA - DCA")
        print("=" * 65)
        self._calcular_manualmente()
        self._verificar_con_scipy()
        self._construir_tabla()
        self._calcular_eta_cuadrado()

    def _calcular_manualmente(self):
        """
        CÁLCULO MANUAL DEL ANOVA - paso a paso.

        Muestra cada operación matemática explícitamente, lo que es
        necesario para el reporte académico (tabla calculada manualmente).

        FÓRMULAS UTILIZADAS:
        ──────────────────────────────────────────────────────────────
        Gran Media: Ȳ.. = (ΣΣYᵢⱼ) / N
        SCTrat = Σ nᵢ(Ȳᵢ. - Ȳ..)²    [variación entre grupos]
        SCError = ΣΣ(Yᵢⱼ - Ȳᵢ.)²      [variación dentro de grupos]
        SCTotal = ΣΣ(Yᵢⱼ - Ȳ..)²      [variación total]
        Verificación: SCTotal = SCTrat + SCError
        CMTrat = SCTrat / (k-1)
        CMError = SCError / (N-k)
        F = CMTrat / CMError
        ──────────────────────────────────────────────────────────────
        """
        print("\n[ CÁLCULO MANUAL PASO A PASO ]\n")

        # ── Datos básicos ─────────────────────────────────────────────────
        k = len(GRUPOS)                    # Número de tratamientos (3)
        nᵢ = {g: len(self.grupos_data[g]) for g in GRUPOS}  # n por grupo
        N = sum(nᵢ.values())               # Total de observaciones (30)
        medias_grupo = {g: np.mean(self.grupos_data[g]) for g in GRUPOS}
        gran_media = np.mean(              # Media de TODAS las obs. juntas
            np.concatenate([self.grupos_data[g] for g in GRUPOS])
        )

        print(f"  Parámetros del diseño:")
        print(f"  k (tratamientos) = {k}")
        print(f"  N (total obs.)   = {N}")
        print(f"  nᵢ por grupo     = {nᵢ}")
        print(f"  Gran Media (Ȳ..) = {gran_media:.4f}\n")

        print(f"  Medias por grupo:")
        for g in GRUPOS:
            print(f"    Ȳ({ETIQUETAS_GRUPOS[g]}) = {medias_grupo[g]:.4f}")

        # ── SUMAS DE CUADRADOS ─────────────────────────────────────────────

        # SCTratamientos: variación ENTRE grupos
        # Cuánto se alejan las medias de grupo de la gran media
        # Fórmula: Σ nᵢ × (Ȳᵢ - Ȳ..)²
        SC_trat = sum(
            nᵢ[g] * (medias_grupo[g] - gran_media) ** 2
            for g in GRUPOS
        )

        # SCError: variación DENTRO de los grupos (variabilidad natural)
        # Cuánto se alejan las obs. individuales de su media de grupo
        # Fórmula: ΣΣ (Yᵢⱼ - Ȳᵢ)²
        SC_error = sum(
            np.sum((self.grupos_data[g] - medias_grupo[g]) ** 2)
            for g in GRUPOS
        )

        # SCTotal: variación TOTAL (referencia)
        # Cuánto se alejan todas las obs. de la gran media
        # Fórmula: ΣΣ (Yᵢⱼ - Ȳ..)²
        todas_obs = np.concatenate([self.grupos_data[g] for g in GRUPOS])
        SC_total = np.sum((todas_obs - gran_media) ** 2)

        print(f"\n  Sumas de Cuadrados:")
        print(f"  SCTrat  = Σ nᵢ(Ȳᵢ - Ȳ..)² = {SC_trat:.4f}")
        print(f"  SCError = ΣΣ(Yᵢⱼ - Ȳᵢ)²  = {SC_error:.4f}")
        print(f"  SCTotal = ΣΣ(Yᵢⱼ - Ȳ..)² = {SC_total:.4f}")
        print(f"  Verificación: SCTrat + SCError = {SC_trat + SC_error:.4f} ≈ SCTotal ✓")

        # ── GRADOS DE LIBERTAD ─────────────────────────────────────────────
        # GL son los divisores que "promedian" correctamente cada SC
        GL_trat = k - 1          # Entre grupos: k tratamientos - 1
        GL_error = N - k         # Dentro grupos: N obs - k medias estimadas
        GL_total = N - 1         # Total: N obs - 1 gran media estimada

        print(f"\n  Grados de Libertad:")
        print(f"  GL_Trat  = k - 1   = {k} - 1   = {GL_trat}")
        print(f"  GL_Error = N - k   = {N} - {k}  = {GL_error}")
        print(f"  GL_Total = N - 1   = {N} - 1  = {GL_total}")

        # ── CUADRADOS MEDIOS ───────────────────────────────────────────────
        # CM = SC / GL → "varianza promedio" para cada fuente
        CM_trat = SC_trat / GL_trat
        CM_error = SC_error / GL_error     # Este es el MSE (varianza residual)

        print(f"\n  Cuadrados Medios:")
        print(f"  CMTrat  = SCTrat  / GL_Trat  = {SC_trat:.4f} / {GL_trat} = {CM_trat:.4f}")
        print(f"  CMError = SCError / GL_Error = {SC_error:.4f} / {GL_error} = {CM_error:.4f}")

        # ── ESTADÍSTICO F ──────────────────────────────────────────────────
        # F = variación ENTRE grupos / variación DENTRO de grupos
        # Si H₀ es verdadera → F ≈ 1 (ambas son estimaciones de σ²)
        # Si H₁ es verdadera → F >> 1 (entre-grupos >> dentro-grupos)
        F_calculado = CM_trat / CM_error

        # P-valor: P(F > F_calculado | H₀ verdadera)
        # Probabilidad de observar un F tan extremo si no hay efecto real
        p_valor = 1 - stats.f.cdf(F_calculado, GL_trat, GL_error)

        # Valor crítico F para α dado
        self.f_critico = stats.f.ppf(1 - ALPHA, GL_trat, GL_error)

        print(f"\n  Estadístico F:")
        print(f"  F = CMTrat / CMError = {CM_trat:.4f} / {CM_error:.4f} = {F_calculado:.4f}")
        print(f"  p-valor = P(F > {F_calculado:.4f}) = {p_valor:.4f}")
        print(f"  F crítico (α={ALPHA}, GL={GL_trat},{GL_error}) = {self.f_critico:.4f}")

        # Guardar todos los valores calculados para uso posterior
        self._calculo_manual = {
            "k": k, "N": N, "GL_trat": GL_trat, "GL_error": GL_error,
            "GL_total": GL_total, "SC_trat": SC_trat, "SC_error": SC_error,
            "SC_total": SC_total, "CM_trat": CM_trat, "CM_error": CM_error,
            "F": F_calculado, "p_valor": p_valor, "gran_media": gran_media,
            "medias_grupo": medias_grupo, "ni": nᵢ
        }

    def _verificar_con_scipy(self):
        """
        Verifica el cálculo manual usando scipy.stats.f_oneway.
        Ambos métodos deben dar exactamente el mismo resultado.
        Las diferencias mínimas se deben a precisión de punto flotante.
        """
        print("\n[ VERIFICACIÓN CON SCIPY ]\n")

        # scipy.stats.f_oneway recibe los grupos como argumentos separados
        grupos_arrays = [self.grupos_data[g] for g in GRUPOS]
        F_scipy, p_scipy = stats.f_oneway(*grupos_arrays)

        self._scipy_result = {"F": F_scipy, "p_valor": p_scipy}

        F_manual = self._calculo_manual["F"]
        p_manual = self._calculo_manual["p_valor"]

        print(f"  Manual:  F = {F_manual:.6f}, p = {p_manual:.6f}")
        print(f"  SciPy:   F = {F_scipy:.6f}, p = {p_scipy:.6f}")

        # Verificar que los valores coincidan (tolerancia numérica de 1e-6)
        if abs(F_manual - F_scipy) < 1e-6:
            print("  ✓ Los valores coinciden perfectamente.")
        else:
            print(f"  ⚠ Diferencia: {abs(F_manual - F_scipy):.2e} (revisar cálculo)")

    def _construir_tabla(self):
        """
        Construye la tabla ANOVA en formato DataFrame para presentación.
        Formato estándar usado en publicaciones científicas y reportes APA.
        """
        c = self._calculo_manual  # Alias para brevedad

        filas = [
            {
                "Fuente de Variación": "Tratamientos",
                "GL": c["GL_trat"],
                "SC": round(c["SC_trat"], 4),
                "CM": round(c["CM_trat"], 4),
                "F": round(c["F"], 4),
                "p-valor": round(c["p_valor"], 4)
            },
            {
                "Fuente de Variación": "Error (Residual)",
                "GL": c["GL_error"],
                "SC": round(c["SC_error"], 4),
                "CM": round(c["CM_error"], 4),
                "F": "—",
                "p-valor": "—"
            },
            {
                "Fuente de Variación": "Total",
                "GL": c["GL_total"],
                "SC": round(c["SC_total"], 4),
                "CM": "—",
                "F": "—",
                "p-valor": "—"
            }
        ]

        self.tabla_anova = pd.DataFrame(filas).set_index("Fuente de Variación")

    def _calcular_eta_cuadrado(self):
        """
        Calcula η² (eta cuadrado): tamaño del efecto del ANOVA.

        η² = SCTratamientos / SCTotal

        Interpretación (Cohen, 1988):
          η² < 0.01  → efecto pequeño (ínfimo)
          η² = 0.06  → efecto mediano
          η² ≥ 0.14  → efecto grande

        η² indica qué proporción de la variación total en los pesos
        se explica por los tratamientos.
        """
        c = self._calculo_manual
        self.eta_cuadrado = c["SC_trat"] / c["SC_total"]

    def imprimir_tabla(self):
        """Imprime la tabla ANOVA formateada en consola."""
        print("\n" + "=" * 65)
        print("TABLA ANOVA COMPLETA")
        print("=" * 65)
        print(self.tabla_anova.to_string())
        print()

    def imprimir_interpretacion(self):
        """
        Imprime la interpretación estadística del resultado.
        Incluye la regla de decisión y la conclusión.
        """
        c = self._calculo_manual
        F = c["F"]
        p = c["p_valor"]
        GL_t = c["GL_trat"]
        GL_e = c["GL_error"]

        print("─" * 65)
        print("INTERPRETACIÓN DEL ANOVA")
        print("─" * 65)
        print(f"\n  Estadístico F({GL_t}, {GL_e}) = {F:.4f}")
        print(f"  p-valor = {p:.4f}")
        print(f"  F crítico (α={ALPHA}) = {self.f_critico:.4f}")
        print(f"  η² (eta cuadrado) = {self.eta_cuadrado:.4f}")

        # Clasificación del tamaño del efecto según Cohen (1988)
        if self.eta_cuadrado < 0.01:
            efecto = "ínfimo"
        elif self.eta_cuadrado < 0.06:
            efecto = "pequeño"
        elif self.eta_cuadrado < 0.14:
            efecto = "mediano"
        else:
            efecto = "grande"

        print(f"  Tamaño del efecto: {efecto} (η² = {self.eta_cuadrado:.4f})")

        print("\n  REGLA DE DECISIÓN:")
        if p < ALPHA:
            print(f"  → p ({p:.4f}) < α ({ALPHA}) → SE RECHAZA H₀")
            print(f"  → F calculado ({F:.4f}) > F crítico ({self.f_critico:.4f})")
            print("\n  CONCLUSIÓN: Existe diferencia significativa entre las medias")
            print(f"  de los tratamientos (α = {ALPHA}).")
            print("  Al menos un tratamiento difiere de los demás.")
        else:
            print(f"  → p ({p:.4f}) ≥ α ({ALPHA}) → NO SE RECHAZA H₀")
            print(f"  → F calculado ({F:.4f}) ≤ F crítico ({self.f_critico:.4f})")
            print("\n  CONCLUSIÓN: No existe evidencia suficiente para afirmar")
            print("  que los tratamientos producen efectos diferentes.")

        print()

    def imprimir_reporte_apa(self):
        """
        Genera el reporte en formato APA 7ma edición.
        Responde directamente al punto B.3 de la tarea.
        """
        c = self._calculo_manual
        F = c["F"]
        p = c["p_valor"]
        GL_t = c["GL_trat"]
        GL_e = c["GL_error"]
        η2 = self.eta_cuadrado

        # Determinar si existe o no efecto significativo
        existe = "existe" if p < ALPHA else "no existe"
        sig_text = "significativo" if p < ALPHA else "no significativo"

        # Formato p-valor según APA: si p < .001 → "p < .001"; sino → "p = .xxx"
        if p < 0.001:
            p_str = "p < .001"
        else:
            p_str = f"p = {p:.3f}"

        print("─" * 65)
        print("REPORTE ESTADÍSTICO FORMAL (Formato APA 7ma Edición)")
        print("─" * 65)
        print(f"""
  Se realizó un análisis de varianza de un factor para examinar el
  efecto del tratamiento en el peso seco de las plantas (en gramos).
  Los resultados indicaron que {existe} un efecto {sig_text}
  del tratamiento, F({GL_t}, {GL_e}) = {F:.2f}, {p_str}, η² = {η2:.2f}.

  Las medias y desviaciones estándar de los grupos fueron: control
  (M = {c['medias_grupo']['ctrl']:.2f}), tratamiento 1
  (M = {c['medias_grupo']['trt1']:.2f}) y tratamiento 2
  (M = {c['medias_grupo']['trt2']:.2f}).

  El tamaño del efecto η² = {η2:.2f} indica un efecto {'grande' if η2 >= 0.14
  else 'mediano' if η2 >= 0.06 else 'pequeño'} de los tratamientos
  sobre la variable dependiente.
""")

    def get_resultados(self):
        """Retorna diccionario con todos los resultados del ANOVA."""
        return {
            **self._calculo_manual,
            "eta_cuadrado": self.eta_cuadrado,
            "f_critico": self.f_critico,
            "tabla": self.tabla_anova,
            "scipy": self._scipy_result
        }