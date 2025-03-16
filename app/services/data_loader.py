import pandas as pd
import os
from fastapi import HTTPException
from app.config import FILE_PATH, COLUMNAS_EXCLUIR


def cargar_datos():
    """Carga y limpia los datos del archivo CSV."""
    if not os.path.exists(FILE_PATH):
        raise HTTPException(
            status_code=404, detail="Archivo Miloto.csv no encontrado"
        )

    df = pd.read_csv(FILE_PATH, dtype=str)

    if "Draw Date" not in df.columns:
        raise HTTPException(
            status_code=400, detail="No se encontró la columna 'Draw Date'"
        )

    df["Draw Date"] = pd.to_datetime(
        df["Draw Date"], errors="coerce"
    ).dt.strftime('%Y-%m-%d')

    return df.drop(
        columns=[col for col in COLUMNAS_EXCLUIR if col in df.columns],
        errors="ignore"
    ), df["Draw Date"]
