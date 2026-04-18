"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: config.py
Propósito: Configuración centralizada del proyecto (Fase 1 - Waterfall)
           Define todas las constantes, rutas y parámetros globales.
           Modificar aquí afecta a todos los módulos del proyecto.
Autores: [Equipo]
Fecha: 2025
=============================================================================
"""

import os

# ---------------------------------------------------------------------------
# RUTAS DEL PROYECTO
# ---------------------------------------------------------------------------
# Directorio base donde se encuentran todos los scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde se guardarán todas las figuras/gráficos generados
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Carpeta donde se guardará el reporte final
REPORT_DIR = os.path.join(BASE_DIR, "report")

# ---------------------------------------------------------------------------
# PARÁMETROS ESTADÍSTICOS
# ---------------------------------------------------------------------------
# Nivel de significancia para todas las pruebas (α = 0.05 → 95% confianza)
ALPHA = 0.05

# Semilla para reproducibilidad (garantiza resultados iguales en cada ejecución)
RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DEL DATASET PlantGrowth
# ---------------------------------------------------------------------------
# Nombres de los grupos de tratamiento tal como aparecen en el dataset
GRUPOS = ["ctrl", "trt1", "trt2"]

# Etiquetas legibles para los gráficos
ETIQUETAS_GRUPOS = {
    "ctrl": "Control",
    "trt1": "Tratamiento 1",
    "trt2": "Tratamiento 2"
}

# Variable de respuesta (columna que contiene los pesos secos)
VAR_RESPUESTA = "weight"

# Variable de agrupación (columna que contiene el tratamiento)
VAR_GRUPO = "group"

# ---------------------------------------------------------------------------
# ESTILO VISUAL DE GRÁFICOS
# ---------------------------------------------------------------------------
# Paleta de colores para los 3 grupos (ctrl, trt1, trt2)
COLORES = {
    "ctrl": "#2E86AB",   # Azul acero
    "trt1": "#E84855",   # Rojo coral
    "trt2": "#3BB273"    # Verde esmeralda
}

# Tamaño estándar de figura para gráficos individuales (ancho x alto en pulgadas)
FIGSIZE_SIMPLE = (8, 5)

# Tamaño para gráficos múltiples/comparativos
FIGSIZE_MULTIPLE = (14, 5)

# Resolución de exportación en DPI (300 = calidad para impresión)
DPI = 300

# ---------------------------------------------------------------------------
# CREACIÓN AUTOMÁTICA DE CARPETAS DE SALIDA
# ---------------------------------------------------------------------------
# Se crean automáticamente al importar este módulo
for carpeta in [OUTPUT_DIR, REPORT_DIR]:
    os.makedirs(carpeta, exist_ok=True)