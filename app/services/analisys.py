import pandas as pd
from collections import Counter, defaultdict
from fastapi import HTTPException
from itertools import combinations


def calcular_frecuencia(df, fechas):
    """Calcula la frecuencia y fechas de aparición de cada número."""
    frecuencia = defaultdict(lambda: {"cantidad": 0, "fechas": []})
    total_numeros = 0

    for col in df.columns:
        for index, num in df[col].items():
            if pd.notna(num):
                frecuencia[num]["cantidad"] += 1
                frecuencia[num]["fechas"].append(fechas.iloc[index])
                total_numeros += 1

    for num in frecuencia:
        frecuencia[num]["fechas"].sort(reverse=True)
        frecuencia[num]["porcentaje"] = round(
            (frecuencia[num]["cantidad"] / total_numeros) * 100, 2
        )

    return dict(
        sorted(
            frecuencia.items(), key=lambda x: x[1]["cantidad"], reverse=True
        )
    )


def obtener_combinaciones_comunes(df):
    """Obtiene las combinaciones más comunes de los sorteos."""
    combinaciones = df.apply(
        lambda row: tuple(sorted(map(str, row.dropna()))), axis=1
    )
    conteo = dict(Counter(combinaciones).most_common(1000))

    # Convertir claves de tupla a string para JSON
    return {str(k): v for k, v in conteo.items()}


def calcular_probabilidades(df):
    """Calcula las probabilidades de cada número en la lotería."""
    frecuencia = df.apply(pd.value_counts).sum(axis=1).to_dict()
    total_numeros = sum(frecuencia.values())

    if total_numeros == 0:
        raise HTTPException(
            status_code=400,
            detail="No hay datos suficientes para calcular probabilidades"
        )

    return dict(
        sorted(
            {
                num: round(
                    (freq / total_numeros) * 100, 2
                ) for num, freq in frecuencia.items()
            }.items(), key=lambda x: x[1], reverse=True)
        )


def obtener_combinaciones_frecuentes(df, tamano=5):
    """Obtiene las combinaciones más comunes con el tamaño especificado."""
    todas_combinaciones = []

    # Recorremos cada fila (sorteo) y generamos combinaciones
    for _, row in df.iterrows():
        numeros = row.dropna().tolist()  # Eliminamos valores NaN
        combinaciones_fila = list(combinations(sorted(numeros), tamano))
        todas_combinaciones.extend(combinaciones_fila)

    # Contamos las combinaciones más comunes (convertimos las listas en tuplas)
    conteo = Counter(map(tuple, todas_combinaciones))

    # Contamos las combinaciones más comunes
    return conteo.most_common(10)
