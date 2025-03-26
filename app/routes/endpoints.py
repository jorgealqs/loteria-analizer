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
import xmlrpc.client
from dotenv import load_dotenv
import os


# Cargo variables de mentor decide .env
load_dotenv()

# Obtener valores de las variables de entorno
ODOO_URL = os.getenv("ODOO_URL")
DB_NAME = os.getenv("DB_NAME")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


# 📌 Configure logging
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

router = APIRouter(prefix="/api")


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


@router.get("/odoo/conectar")
def conectar_odoo():

    # Conectar con Odoo
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    user_id = common.authenticate(DB_NAME, ODOO_USER, ODOO_PASSWORD, {})

    if not user_id:
        logging.info("\n\nError en la autenticación\n\n")
    else:
        logging.info(f"\n\nUsuario autenticado con ID: {user_id}\n\n")

        # Conectar con el modelo de Odoo
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

        # Obtener todos los campos del modelo lottery.baloto
        fields_lottery = models.execute_kw(
            DB_NAME,
            user_id,
            ODOO_PASSWORD,
            "lottery.baloto",
            "fields_get",
            [],
            {"attributes": ["string", "type"]}
        )

        # Extraer los nombres de los campos
        all_fields = list(fields_lottery.keys())

        tipos_loteria = models.execute_kw(
            DB_NAME,
            user_id,
            ODOO_PASSWORD,
            "lottery.baloto.type",  # Modelo correcto donde está 'MiLoto'
            "search_read",
            [[["name", "=", "MiLoto"]]],
            {"fields": ["id"]}
        )

        # Buscar información del usuario en res. Partner
        partner_data = models.execute_kw(
            DB_NAME,
            user_id,
            ODOO_PASSWORD,
            "lottery.baloto",  # Modelo
            "search_read",  # Método
            [[["lottery_type_id", "=", tipos_loteria[0]["id"]]]],
            # Sin filtros
            {"fields": all_fields}  # Campos que queremos ver
        )

        if partner_data:
            logging.info(f"\n\nDatos del usuario: {partner_data}\n\n")
            return {"result": partner_data}
        else:
            logging.info("\n\nNo se encontró el usuario.\n\n")
