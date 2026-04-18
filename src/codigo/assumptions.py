"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: assumptions.py
Propósito: FASE 3 (Waterfall) - Verificación de supuestos.
           Antes de realizar el ANOVA, se deben verificar los 3 supuestos
           fundamentales: Normalidad, Homogeneidad de varianzas e Independencia.
           Esta fase es obligatoria en Waterfall: sin validar supuestos,
           los resultados del ANOVA podrían ser inválidos.
=============================================================================
"""

import numpy as np
from scipy import stats
from config import GRUPOS, ETIQUETAS_GRUPOS, ALPHA


class AssumptionsTester:
    """
    Clase responsable de verificar los supuestos del ANOVA de una vía.

    Los 3 supuestos del ANOVA (modelo: Yᵢⱼ = μ + τᵢ + εᵢⱼ):
    ─────────────────────────────────────────────────────────
    1. NORMALIDAD: Los errores (εᵢⱼ) siguen distribución normal.
       Prueba: Shapiro-Wilk (preferida para n < 50)
       H₀: Los datos provienen de una distribución normal
       Consecuencia si se viola: usar Kruskal-Wallis (no paramétrico)

    2. HOMOGENEIDAD DE VARIANZAS (Homocedasticidad): σ₁² = σ₂² = σ₃²
       Prueba: Levene (más robusta que Bartlett cuando hay no-normalidad)
       H₀: Las varianzas de todos los grupos son iguales
       Consecuencia si se viola: usar Welch's ANOVA

    3. INDEPENDENCIA: Las observaciones son independientes entre sí.
       No existe prueba formal; se verifica por diseño experimental.
       En PlantGrowth: plantas distintas → independencia garantizada por diseño.

    Atributos:
        grupos_data (dict): Arrays de datos por grupo
        resultados_normalidad (dict): Resultados Shapiro-Wilk por grupo
        resultado_levene (dict): Resultado prueba de Levene
        supuestos_ok (bool): True si TODOS los supuestos se cumplen
    """

    def __init__(self, grupos_data: dict):
        """
        Args:
            grupos_data (dict): {'ctrl': array, 'trt1': array, 'trt2': array}
        """
        self.grupos_data = grupos_data
        self.resultados_normalidad = {}
        self.resultado_levene = {}
        self.supuestos_ok = False
        self._verificar_todos()  # Ejecuta todas las pruebas al instanciar

    def _verificar_todos(self):
        """
        Ejecuta secuencialmente todas las pruebas de supuestos.
        El orden importa: primero normalidad, luego homocedasticidad.
        """
        print("=" * 60)
        print("VERIFICACIÓN DE SUPUESTOS DEL ANOVA")
        print("=" * 60)
        self._prueba_normalidad()
        self._prueba_levene()
        self._evaluar_independencia()
        self._conclusion_supuestos()

    def _prueba_normalidad(self):
        """
        SUPUESTO 1: Normalidad mediante prueba de Shapiro-Wilk.

        Shapiro-Wilk es la prueba de normalidad más potente para muestras
        pequeñas (n < 50). PlantGrowth tiene n=10 por grupo → ideal.

        Hipótesis:
          H₀: Los datos del grupo siguen distribución normal (no rechazar es bueno)
          H₁: Los datos NO siguen distribución normal
          Regla: Si p > α → no se rechaza H₀ → normalidad aceptada
        """
        print("\n[ SUPUESTO 1: NORMALIDAD ]")
        print("  Prueba: Shapiro-Wilk  |  H₀: distribución normal")
        print(f"  Nivel α = {ALPHA}  →  p > {ALPHA} indica normalidad\n")

        todos_normales = True  # Flag: se vuelve False si algún grupo falla

        for grupo in GRUPOS:
            datos = self.grupos_data[grupo]

            # scipy.stats.shapiro retorna (estadístico W, valor p)
            # W cercano a 1 → muy normal; W << 1 → no normal
            w_stat, p_valor = stats.shapiro(datos)

            cumple = p_valor > ALPHA  # True si NO se rechaza H₀
            if not cumple:
                todos_normales = False

            simbolo = "✓" if cumple else "✗"
            decision = "Normal" if cumple else "No normal"

            self.resultados_normalidad[grupo] = {
                "estadistico_W": w_stat,
                "p_valor": p_valor,
                "cumple": cumple
            }

            print(f"  {simbolo} {ETIQUETAS_GRUPOS[grupo]:15s} → "
                  f"W = {w_stat:.4f}, p = {p_valor:.4f}  [{decision}]")

        self._normalidad_ok = todos_normales

        if todos_normales:
            print("\n  → CONCLUSIÓN: Supuesto de normalidad CUMPLIDO para todos los grupos.")
        else:
            print("\n  → CONCLUSIÓN: Supuesto de normalidad VIOLADO en algún grupo.")
            print("     Alternativa: Prueba de Kruskal-Wallis (no paramétrica).")

    def _prueba_levene(self):
        """
        SUPUESTO 2: Homogeneidad de varianzas mediante prueba de Levene.

        Levene es más robusta que Bartlett cuando los datos pueden desviarse
        levemente de la normalidad. Compara la dispersión entre grupos.

        Hipótesis:
          H₀: σ₁² = σ₂² = σ₃² (varianzas iguales → homocedasticidad)
          H₁: Al menos una varianza difiere
          Regla: Si p > α → no se rechaza H₀ → varianzas homogéneas
        """
        print("\n[ SUPUESTO 2: HOMOGENEIDAD DE VARIANZAS ]")
        print("  Prueba: Levene  |  H₀: varianzas iguales entre grupos")
        print(f"  Nivel α = {ALPHA}  →  p > {ALPHA} indica homocedasticidad\n")

        # Extraer los arrays de cada grupo como argumentos posicionales
        # scipy.stats.levene acepta *args (un array por grupo)
        grupos_arrays = [self.grupos_data[g] for g in GRUPOS]
        levene_stat, p_valor = stats.levene(*grupos_arrays)

        cumple = p_valor > ALPHA
        simbolo = "✓" if cumple else "✗"
        decision = "Homogéneas" if cumple else "Heterogéneas"

        self.resultado_levene = {
            "estadistico_F": levene_stat,
            "p_valor": p_valor,
            "cumple": cumple
        }

        print(f"  {simbolo} Levene: F = {levene_stat:.4f}, p = {p_valor:.4f}  [{decision}]")
        self._homocedasticidad_ok = cumple

        if cumple:
            print("\n  → CONCLUSIÓN: Supuesto de homocedasticidad CUMPLIDO.")
            print("     Las varianzas de los grupos son estadísticamente iguales.")
        else:
            print("\n  → CONCLUSIÓN: Supuesto de homocedasticidad VIOLADO.")
            print("     Alternativa: Welch's ANOVA (no asume varianzas iguales).")

    def _evaluar_independencia(self):
        """
        SUPUESTO 3: Independencia de las observaciones.

        La independencia NO se puede probar estadísticamente de la misma
        manera; se verifica por el DISEÑO EXPERIMENTAL.

        En PlantGrowth:
          • Cada planta es una unidad experimental distinta
          • La asignación de tratamientos fue aleatoria
          • No hay medidas repetidas ni observaciones anidadas
          → Por diseño: independencia GARANTIZADA
        """
        print("\n[ SUPUESTO 3: INDEPENDENCIA ]")
        print("  Evaluación: Por diseño experimental (no hay prueba formal)\n")
        print("  ✓ PlantGrowth: cada planta = unidad experimental independiente.")
        print("    Asignación aleatoria → independencia garantizada por diseño.")
        self._independencia_ok = True

    def _conclusion_supuestos(self):
        """
        Emite la conclusión global sobre si es válido proceder con ANOVA.
        Si todos los supuestos se cumplen → ANOVA paramétrico es apropiado.
        Si alguno falla → recomendar alternativas.
        """
        print("\n" + "─" * 60)
        print("CONCLUSIÓN GLOBAL DE SUPUESTOS")
        print("─" * 60)

        # El ANOVA es válido solo si los 3 supuestos se cumplen
        self.supuestos_ok = (
            self._normalidad_ok and
            self._homocedasticidad_ok and
            self._independencia_ok
        )

        estado_n = "✓" if self._normalidad_ok else "✗"
        estado_h = "✓" if self._homocedasticidad_ok else "✗"

        print(f"  {estado_n} Normalidad       : {'Cumplido' if self._normalidad_ok else 'VIOLADO'}")
        print(f"  {estado_h} Homocedasticidad : {'Cumplido' if self._homocedasticidad_ok else 'VIOLADO'}")
        print(f"  ✓ Independencia  : Cumplido (por diseño)")

        if self.supuestos_ok:
            print("\n  ✅ TODOS LOS SUPUESTOS CUMPLIDOS.")
            print("     El ANOVA paramétrico de una vía es apropiado.")
        else:
            print("\n  ⚠️  ALGÚN SUPUESTO VIOLADO.")
            print("     Considerar Kruskal-Wallis o Welch's ANOVA.")
        print()

    def imprimir_alternativas(self):
        """
        Explica qué hacer si cada supuesto se viola.
        Responde directamente a la Parte B.4 de la tarea.
        """
        print("=" * 60)
        print("¿QUÉ HACER SI SE VIOLA UN SUPUESTO?")
        print("=" * 60)

        alternativas = [
            ("Normalidad violada",
             "Usar Kruskal-Wallis (equivalente no paramétrico del ANOVA).\n"
             "     No asume distribución; compara medianas en vez de medias.\n"
             "     Función: scipy.stats.kruskal(*grupos)"),
            ("Homocedasticidad violada",
             "Usar Welch's ANOVA (robusto a varianzas desiguales).\n"
             "     Ajusta los grados de libertad (corrección de Welch).\n"
             "     Función: scipy.stats.alexandergovern(*grupos) o\n"
             "               pingouin.welch_anova(data, dv, between)"),
            ("Independencia violada",
             "El diseño experimental es incorrecto desde su base.\n"
             "     Usar ANOVA de medidas repetidas (si las mismas unidades\n"
             "     experimentales reciben múltiples tratamientos).\n"
             "     Función: pingouin.rm_anova(data, dv, within, subject)"),
        ]

        for supuesto, alternativa in alternativas:
            print(f"\n  ⚠️  {supuesto}:")
            print(f"     → {alternativa}")
        print()

    def get_resultados(self):
        """Retorna diccionario completo con todos los resultados de supuestos."""
        return {
            "normalidad": self.resultados_normalidad,
            "levene": self.resultado_levene,
            "independencia": {"cumple": True, "metodo": "Por diseño experimental"},
            "supuestos_ok": self.supuestos_ok
        }