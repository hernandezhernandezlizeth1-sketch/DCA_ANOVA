"""
=============================================================================
TAREA 2: Diseño Completamente Aleatorio (DCA) y ANOVA
=============================================================================
Archivo: data_loader.py
Propósito: FASE 1 (Waterfall) - Requerimientos y adquisición de datos.
           Responsabilidad única: cargar, validar y preparar el dataset
           PlantGrowth para ser usado por los demás módulos.
=============================================================================
"""

import pandas as pd
import numpy as np
from config import GRUPOS, VAR_RESPUESTA, VAR_GRUPO, ETIQUETAS_GRUPOS


class DataLoader:
    """
    Clase responsable de cargar y validar el dataset PlantGrowth.

    En metodología Waterfall, esta clase representa la FASE DE REQUERIMIENTOS
    y DISEÑO DEL SISTEMA: antes de analizar nada, necesitamos datos limpios
    y validados. Separar esta responsabilidad del análisis permite:
      - Cambiar la fuente de datos sin tocar el análisis
      - Detectar errores de datos antes de que contaminen resultados
      - Reutilizar la carga en múltiples scripts

    Atributos:
        df (pd.DataFrame): Dataset completo cargado y validado
        grupos_data (dict): Diccionario {nombre_grupo: array_de_valores}
    """

    # Dataset PlantGrowth embebido directamente en el código.
    # Estos son los datos originales del dataset de R, transcritos aquí
    # para que el proyecto sea autónomo (no requiere conexión a R).
    _PLANT_GROWTH_DATA = {
        "weight": [
            # Control (10 observaciones): plantas sin tratamiento
            4.17, 5.58, 5.18, 6.11, 4.50, 4.61, 5.17, 4.53, 5.33, 5.14,
            # Tratamiento 1 (10 observaciones): primer fertilizante
            4.81, 4.17, 4.41, 3.59, 5.87, 3.83, 6.03, 4.89, 4.32, 4.69,
            # Tratamiento 2 (10 observaciones): segundo fertilizante
            6.31, 5.12, 5.54, 5.50, 5.37, 5.29, 4.92, 6.15, 5.80, 5.26
        ],
        "group": (
            ["ctrl"] * 10 +   # 10 repeticiones del grupo control
            ["trt1"] * 10 +   # 10 repeticiones del tratamiento 1
            ["trt2"] * 10     # 10 repeticiones del tratamiento 2
        )
    }

    def __init__(self):
        """
        Inicializa el DataLoader y ejecuta automáticamente la carga
        y validación. Si los datos tienen errores, se lanza una excepción
        aquí, antes de que lleguen al análisis.
        """
        self.df = None          # DataFrame principal (todas las observaciones)
        self.grupos_data = {}   # Datos separados por grupo para conveniencia
        self._cargar()          # Carga los datos
        self._validar()         # Verifica integridad
        self._preparar()        # Organiza para uso posterior

    def _cargar(self):
        """
        PASO 1: Crea el DataFrame desde los datos embebidos.
        Convierte 'group' a tipo categórico con orden definido para que
        los gráficos siempre muestren ctrl → trt1 → trt2.
        """
        self.df = pd.DataFrame(self._PLANT_GROWTH_DATA)

        # Convertir a categórico con orden explícito
        # Esto garantiza que ctrl siempre sea la referencia base
        self.df[VAR_GRUPO] = pd.Categorical(
            self.df[VAR_GRUPO],
            categories=GRUPOS,
            ordered=True
        )

        print("✓ Dataset PlantGrowth cargado correctamente.")
        print(f"  → Total de observaciones: {len(self.df)}")
        print(f"  → Grupos encontrados: {list(self.df[VAR_GRUPO].unique())}\n")

    def _validar(self):
        """
        PASO 2: Verifica que los datos sean válidos antes de continuar.
        En Waterfall, la validación temprana evita errores costosos más adelante.
        Verifica:
          - No hay valores nulos (NaN)
          - Los 3 grupos existen
          - Los pesos son valores positivos (biológicamente plausibles)
          - Cada grupo tiene al menos 2 observaciones (necesario para varianza)
        """
        errores = []

        # Verificar ausencia de valores nulos
        nulos = self.df.isnull().sum().sum()
        if nulos > 0:
            errores.append(f"Se encontraron {nulos} valores nulos en el dataset.")

        # Verificar que existan los 3 grupos esperados
        grupos_presentes = set(self.df[VAR_GRUPO].unique())
        grupos_esperados = set(GRUPOS)
        faltantes = grupos_esperados - grupos_presentes
        if faltantes:
            errores.append(f"Grupos faltantes: {faltantes}")

        # Verificar que los pesos sean positivos
        if (self.df[VAR_RESPUESTA] <= 0).any():
            errores.append("Existen pesos negativos o cero, lo cual no es válido.")

        # Verificar mínimo 2 obs por grupo (se necesitan para calcular varianza)
        for grupo in GRUPOS:
            n = len(self.df[self.df[VAR_GRUPO] == grupo])
            if n < 2:
                errores.append(f"El grupo '{grupo}' tiene menos de 2 observaciones ({n}).")

        # Si hay errores, detener ejecución con mensaje descriptivo
        if errores:
            mensaje = "\n".join(f"  ✗ {e}" for e in errores)
            raise ValueError(f"Errores de validación del dataset:\n{mensaje}")

        print("✓ Validación del dataset completada sin errores.\n")

    def _preparar(self):
        """
        PASO 3: Organiza los datos en estructuras convenientes para el análisis.
        Crea un diccionario con arrays numpy por grupo, que es el formato
        que necesitan scipy y statsmodels para las pruebas estadísticas.
        """
        for grupo in GRUPOS:
            # Filtra el DataFrame por grupo y extrae solo la columna de pesos
            # como array numpy (más eficiente para cálculos estadísticos)
            self.grupos_data[grupo] = (
                self.df[self.df[VAR_GRUPO] == grupo][VAR_RESPUESTA].values
            )

        print("✓ Datos organizados por grupo:")
        for grupo, valores in self.grupos_data.items():
            etiqueta = ETIQUETAS_GRUPOS[grupo]
            print(f"  → {etiqueta}: {len(valores)} observaciones")
        print()

    def get_dataframe(self):
        """
        Retorna el DataFrame completo.
        Interfaz pública para que otros módulos accedan a los datos.
        """
        return self.df.copy()  # .copy() evita modificaciones accidentales

    def get_grupos(self):
        """
        Retorna el diccionario de arrays por grupo.
        Formato: {'ctrl': array([...]), 'trt1': array([...]), 'trt2': array([...])}
        """
        return {k: v.copy() for k, v in self.grupos_data.items()}

    def resumen_basico(self):
        """
        Imprime un resumen rápido del dataset para verificación visual.
        Útil para el reporte y para confirmar que los datos se cargaron bien.
        """
        print("=" * 50)
        print("RESUMEN DEL DATASET PlantGrowth")
        print("=" * 50)
        print(self.df.groupby(VAR_GRUPO)[VAR_RESPUESTA].describe().round(4))
        print()