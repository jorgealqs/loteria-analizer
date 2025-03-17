from fastapi import APIRouter, Query, Response, HTTPException
from app.services.data_loader import cargar_datos
from app.services.analisys import (
    calcular_frecuencia,
    obtener_combinaciones_comunes,
    calcular_probabilidades,
    obtener_combinaciones_frecuentes
)
from app.services.grafic import graficBarras
import logging

# 📌 Configurar logging
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

router = APIRouter()


# 📌 Función auxiliar para cargar datos con manejo de errores
def obtener_datos():
    try:
        df, fechas = cargar_datos()
        return df, fechas
    except Exception as e:
        logging.error(f"Error al cargar datos: {e}")
        raise HTTPException(
            status_code=500, detail="Error interno al cargar datos"
        )


@router.get(
    "/frecuencia", summary="Obtener la frecuencia de todos los números"
)
def frecuencia():
    """ Devuelve la frecuencia de aparición de los números en los sorteos. """
    df, fechas = obtener_datos()
    return {"frecuencia": calcular_frecuencia(df, fechas)}


@router.get("/frecuencia/numero", summary="Frecuencia de un número específico")
def frecuencia_numero(num: int = Query(ge=1, le=39)):
    """
    Devuelve la frecuencia de aparición de un número específico en los sorteos.
    Si el número no ha salido, se informa al usuario.
    """
    df, fechas = obtener_datos()
    frecuencia = calcular_frecuencia(df, fechas)

    if str(num) not in frecuencia:
        return {"mensaje": f"El número {num} no ha salido"}

    return {"numero": num, "datos": frecuencia[str(num)]}


@router.get("/combinaciones_comunes", summary="Obtener combinaciones comunes")
def combinaciones_comunes():
    """ Devuelve las combinaciones más comunes de números en los sorteos. """
    df, _ = obtener_datos()
    return {"combinaciones_comunes": obtener_combinaciones_comunes(df)}


@router.get("/probabilidades", summary="Calcular probabilidades de números")
def probabilidades():
    """ Calcula las probabilidades de los números en base a su historial. """
    df, _ = obtener_datos()
    return {"probabilidades": calcular_probabilidades(df)}


@router.get(
    "/combinaciones_frecuentes", summary="Obtener combinaciones frecuentes"
)
def combinaciones_frecuentes(n: int = Query(ge=2, le=5)):
    """
    Devuelve las combinaciones de números más frecuentes.
    Se puede especificar cuántos números incluir en cada combinación
    (entre 2 y 5).
    """
    df, _ = obtener_datos()
    return {
        "combinaciones_frecuentes": obtener_combinaciones_frecuentes(df, n)
    }


@router.get(
    "/grafico-barras", summary="Generar gráfico de barras para un número"
)
def grafico_barras(num: int = Query(ge=1, le=39)):
    """
    Genera un gráfico de barras con la frecuencia mensual
    de un número específico. Devuelve la imagen en formato PNG.
    """
    df, fechas = obtener_datos()
    frecuencia = calcular_frecuencia(df, fechas)

    fechas_numero = frecuencia.get(str(num))  # Obtener datos como diccionario

    if not fechas_numero:
        raise HTTPException(
            status_code=404, detail=f"No hay datos para el número {num}"
        )

    fechas_lista = fechas_numero.get("fechas", [])

    if not fechas_lista:
        raise HTTPException(
            status_code=404,
            detail="No hay fechas disponibles para este número"
        )

    # 📌 Generar gráfico
    buf = graficBarras(fechas_lista, str(num))

    return Response(content=buf.getvalue(), media_type="image/png")
