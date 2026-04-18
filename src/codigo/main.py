"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: main.py
Propósito: Punto de entrada principal del proyecto.
           Orquesta el flujo COMPLETO en orden Waterfall:

  FASE 1: Carga y validación de datos          (DataLoader)
  FASE 2: Estadísticas descriptivas            (DescriptiveStats)
  FASE 3: Verificación de supuestos            (AssumptionsTester)
  FASE 4: Análisis de varianza (ANOVA)         (AnovaAnalysis)
  FASE 5: Generación de gráficos               (Visualizer)
  FASE 6: Reporte final en consola

En Waterfall: cada fase depende de las anteriores y no puede comenzar
hasta que la fase previa esté completada y validada.

USO:
  Asegúrate de tener el venv activo:
    Windows: .\venv\Scripts\Activate.ps1
    Mac/Linux: source venv/bin/activate

  Ejecutar:
    python main.py

DEPENDENCIAS (instalar con pip):
    pip install numpy pandas scipy matplotlib seaborn statsmodels pingouin
=============================================================================
"""

# ---------------------------------------------------------------------------
# IMPORTACIONES DEL PROYECTO (módulos propios)
# ---------------------------------------------------------------------------
from data_loader import DataLoader
from descriptive_stats import DescriptiveStats
from assumptions import AssumptionsTester
from anova_analysis import AnovaAnalysis
from visualizer import Visualizer


def encabezado():
    """Imprime el encabezado del proyecto al inicio de la ejecución."""
    print("\n" + "█" * 65)
    print("█  TAREA 2: DISEÑO COMPLETAMENTE ALEATORIO (DCA) Y ANOVA  █")
    print("█  Dataset: PlantGrowth  |  Metodología: Waterfall         █")
    print("█" * 65 + "\n")


def separador(titulo: str):
    """Imprime un separador visual entre fases del análisis."""
    print("\n" + "▓" * 65)
    print(f"▓  {titulo}")
    print("▓" * 65 + "\n")


def main():
    """
    Función principal que ejecuta el análisis completo en orden Waterfall.
    Cada bloque representa una fase distinta del ciclo de vida del proyecto.
    """
    encabezado()

    # =========================================================================
    # FASE 1 — CARGA Y VALIDACIÓN DE DATOS
    # Requerimiento Waterfall: antes de analizar, necesitamos datos limpios
    # =========================================================================
    separador("FASE 1: CARGA Y VALIDACIÓN DE DATOS")
    loader = DataLoader()
    loader.resumen_basico()

    # Obtener estructuras de datos para las fases siguientes
    df = loader.get_dataframe()         # DataFrame completo
    grupos_data = loader.get_grupos()   # Diccionario {grupo: array}

    # =========================================================================
    # FASE 2 — ESTADÍSTICAS DESCRIPTIVAS
    # Requerimiento Waterfall: explorar datos antes del análisis formal
    # =========================================================================
    separador("FASE 2: ESTADÍSTICAS DESCRIPTIVAS")
    desc = DescriptiveStats(grupos_data)
    desc.imprimir_tabla()
    desc.imprimir_interpretacion()

    # Guardar resultados para pasarlos al Visualizer
    desc_resultados = desc.get_resultados()

    # =========================================================================
    # FASE 3 — VERIFICACIÓN DE SUPUESTOS
    # Requerimiento Waterfall: validar supuestos ANTES de ejecutar el ANOVA
    # Si los supuestos fallan, el ANOVA paramétrico no es apropiado
    # =========================================================================
    separador("FASE 3: VERIFICACIÓN DE SUPUESTOS DEL ANOVA")
    supuestos = AssumptionsTester(grupos_data)
    supuestos.imprimir_alternativas()

    # Obtener resultados de supuestos (para el reporte final)
    resultados_supuestos = supuestos.get_resultados()

    # =========================================================================
    # FASE 4 — ANÁLISIS DE VARIANZA (ANOVA)
    # Requerimiento Waterfall: análisis principal, ejecutado solo si los
    # datos pasaron validación y los supuestos fueron verificados
    # =========================================================================
    separador("FASE 4: ANÁLISIS DE VARIANZA (ANOVA DE UNA VÍA)")
    anova = AnovaAnalysis(grupos_data)
    anova.imprimir_tabla()
    anova.imprimir_interpretacion()
    anova.imprimir_reporte_apa()

    # Guardar resultados para pasarlos al Visualizer
    anova_resultados = anova.get_resultados()

    # =========================================================================
    # FASE 5 — GENERACIÓN DE GRÁFICOS
    # Requerimiento Waterfall: las visualizaciones usan los resultados
    # de las fases anteriores, no pueden generarse antes
    # =========================================================================
    separador("FASE 5: GENERACIÓN DE GRÁFICOS")
    viz = Visualizer(
        grupos_data=grupos_data,
        desc_resultados=desc_resultados,
        anova_resultados=anova_resultados
    )
    # mostrar=False: solo guarda en disco. Cambiar a True para ver en pantalla.
    viz.generar_todos(mostrar=False)

    # =========================================================================
    # FASE 6 — RESUMEN FINAL
    # =========================================================================
    separador("FASE 6: RESUMEN FINAL DEL ANÁLISIS")

    F = anova_resultados["F"]
    p = anova_resultados["p_valor"]
    η2 = anova_resultados["eta_cuadrado"]
    GL_t = anova_resultados["GL_trat"]
    GL_e = anova_resultados["GL_error"]
    supuestos_ok = resultados_supuestos["supuestos_ok"]

    print("  RESULTADOS CLAVE:")
    print(f"  • Supuestos del ANOVA: {'✓ Todos cumplidos' if supuestos_ok else '⚠ Revisar supuestos'}")
    print(f"  • F({GL_t}, {GL_e}) = {F:.4f}")
    print(f"  • p-valor = {p:.4f}  {'→ SIGNIFICATIVO (p < 0.05)' if p < 0.05 else '→ No significativo'}")
    print(f"  • η² = {η2:.4f}  (tamaño del efecto)")
    print(f"\n  GRÁFICOS GENERADOS:")
    graficos = [
        "01_boxplot_comparativo.png",
        "02_histogramas_densidad.png",
        "03_qqplots_normalidad.png",
        "04_distribucion_F_fisher.png",
        "05_intervalos_confianza.png"
    ]
    for g in graficos:
        print(f"  • outputs/{g}")

    print("\n" + "█" * 65)
    print("█  ANÁLISIS COMPLETADO EXITOSAMENTE                        █")
    print("█" * 65 + "\n")


# ---------------------------------------------------------------------------
# Punto de entrada: solo se ejecuta si se llama directamente este script,
# no si es importado por otro módulo (buena práctica en Python)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()