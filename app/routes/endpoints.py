from fastapi import APIRouter, Query
from app.services.data_loader import cargar_datos
from app.services.analisys import calcular_frecuencia
from app.services.analisys import obtener_combinaciones_comunes
from app.services.analisys import calcular_probabilidades
from app.services.analisys import obtener_combinaciones_frecuentes

router = APIRouter()


@router.get("/frecuencia")
def frecuencia():
    df, fechas = cargar_datos()
    return {"frecuencia": calcular_frecuencia(df, fechas)}


@router.get("/frecuencia/{numero}")
def frecuencia_numero(numero: str):
    df, fechas = cargar_datos()
    frecuencia = calcular_frecuencia(df, fechas)

    if numero not in frecuencia:
        return {
            "mensaje": f"El número {numero} no ha salido"
        }

    return {"numero": numero, "datos": frecuencia[numero]}


@router.get("/combinaciones_comunes")
def combinaciones_comunes():
    df, _ = cargar_datos()
    return {"combinaciones_comunes": obtener_combinaciones_comunes(df)}


@router.get("/probabilidades")
def probabilidades():
    df, _ = cargar_datos()
    return {"probabilidades": calcular_probabilidades(df)}


@router.get("/combinaciones_frecuentes")
def combinaciones_frecuentes(
    n: int = Query(
        5,
        ge=2, le=5, description="Número de elementos en la combinación (2-5)"
    )
):
    df, _ = cargar_datos()
    return {
        "combinaciones_frecuentes": obtener_combinaciones_frecuentes(df, n)
    }
