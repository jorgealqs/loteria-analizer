"""
Lottery Analysis API Endpoints
This module provides REST API endpoints for lottery number
analysis and Odoo integration.
"""

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
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Odoo connection configuration
ODOO_URL = os.getenv("ODOO_URL")
DB_NAME = os.getenv("DB_NAME")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

router = APIRouter(
    prefix="/api",
    tags=["Lottery Analysis"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)


def load_lottery_data():
    """
    Helper function to load lottery data with error handling.

    Returns:
        tuple: DataFrame and dates of lottery draws

    Raises:
        HTTPException: If there's an error loading the data
    """
    try:
        df, dates = cargar_datos()
        return df, dates
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal error while loading data"
        )


@router.get(
    "/frequency",
    summary="Get frequency of all numbers",
    response_description=(
        "Returns frequency distribution of all lottery numbers"
    )
)
async def get_number_frequency() -> Dict[str, Any]:
    """
    Get the frequency distribution of all numbers in lottery draws.

    Returns:
        dict: Frequency data for all numbers
    """
    df, dates = load_lottery_data()
    return {"frequency": calcular_frecuencia(df, dates)}


@router.get(
    "/frequency/number",
    summary="Get frequency of a specific number",
    response_description="Returns frequency data for a specific number"
)
async def get_specific_number_frequency(
    num: int = Query(
        ge=1,
        le=39,
        description="Lottery number between 1 and 39"
    )
) -> Dict[str, Any]:
    """
    Get frequency data for a specific lottery number.

    Args:
        num: The lottery number to analyze (1-39)

    Returns:
        dict: Frequency data for the specified number
    """
    df, dates = load_lottery_data()
    frequency = calcular_frecuencia(df, dates)

    if str(num) not in frequency:
        return {"message": f"Number {num} has not appeared in any draw"}

    return {"number": num, "data": frequency[str(num)]}


@router.get(
    "/common-combinations",
    summary="Get most common number combinations",
    response_description="Returns most frequent number combinations"
)
async def get_common_combinations() -> Dict[str, Any]:
    """
    Get the most common combinations of numbers in lottery draws.

    Returns:
        dict: Most common number combinations
    """
    df, _ = load_lottery_data()
    return {"common_combinations": obtener_combinaciones_comunes(df)}


@router.get(
    "/probabilities",
    summary="Calculate number probabilities",
    response_description="Returns probability calculations for numbers"
)
async def get_probabilities() -> Dict[str, Any]:
    """
    Calculate probabilities for numbers based on historical data.

    Returns:
        dict: Probability calculations for each number
    """
    df, _ = load_lottery_data()
    return {"probabilities": calcular_probabilidades(df)}


@router.get(
    "/frequent-combinations",
    summary="Get frequent number combinations",
    response_description="Returns most frequent combinations of specified size"
)
async def get_frequent_combinations(
    n: int = Query(ge=2, le=5, description="Size of number combinations (2-5)")
) -> Dict[str, Any]:
    """
    Get the most frequent combinations of numbers of specified size.

    Args:
        n: Number of elements in each combination (2-5)

    Returns:
        dict: Most frequent combinations of the specified size
    """
    df, _ = load_lottery_data()
    return {
        "frequent_combinations": obtener_combinaciones_frecuentes(df, n)
    }


@router.get(
    "/bar-chart",
    summary="Generate bar chart for number frequency",
    response_description="Returns PNG image of frequency bar chart"
)
async def generate_bar_chart(
    num: int = Query(ge=1, le=39, description="Lottery number to analyze")
) -> Response:
    """
    Generate a bar chart showing monthly frequency for a specific number.

    Args:
        num: The lottery number to analyze (1-39)

    Returns:
        Response: PNG image of the bar chart

    Raises:
        HTTPException: If no data is available for the number
    """
    df, dates = load_lottery_data()
    frequency = calcular_frecuencia(df, dates)
    number_dates = frequency.get(str(num))

    if not number_dates:
        raise HTTPException(
            status_code=404,
            detail=f"No data available for number {num}"
        )

    dates_list = number_dates.get("fechas", [])
    if not dates_list:
        raise HTTPException(
            status_code=404,
            detail="No dates available for this number"
        )

    buf = graficBarras(dates_list, str(num))
    return Response(content=buf.getvalue(), media_type="image/png")


@router.get(
    "/odoo/connect",
    summary="Connect to Odoo and retrieve lottery data",
    response_description="Returns lottery data from Odoo"
)
async def connect_to_odoo() -> Dict[str, Any]:
    """
    Connect to Odoo server and retrieve lottery-related data.

    Returns:
        dict: Lottery data from Odoo

    Note:
        Requires valid Odoo credentials in environment variables
    """
    # Connect to Odoo
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    user_id = common.authenticate(DB_NAME, ODOO_USER, ODOO_PASSWORD, {})

    if not user_id:
        logging.error("Authentication failed")
        raise HTTPException(
            status_code=401,
            detail="Failed to authenticate with Odoo"
        )

    logging.info(f"User authenticated with ID: {user_id}")

    # Connect to Odoo model
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

    # Get all fields from lottery.baloto model
    fields_lottery = models.execute_kw(
        DB_NAME,
        user_id,
        ODOO_PASSWORD,
        "lottery.baloto",
        "fields_get",
        [],
        {"attributes": ["string", "type"]}
    )

    all_fields = list(fields_lottery.keys())

    # Get lottery types
    lottery_types = models.execute_kw(
        DB_NAME,
        user_id,
        ODOO_PASSWORD,
        "lottery.baloto.type",
        "search_read",
        [[["name", "=", "MiLoto"]]],
        {"fields": ["id"]}
    )

    if not lottery_types:
        raise HTTPException(
            status_code=404,
            detail="Lottery type 'MiLoto' not found"
        )

    # Search lottery data
    lottery_data = models.execute_kw(
        DB_NAME,
        user_id,
        ODOO_PASSWORD,
        "lottery.baloto",
        "search_read",
        [[["lottery_type_id", "=", lottery_types[0]["id"]]]],
        {"fields": all_fields}
    )

    if not lottery_data:
        raise HTTPException(
            status_code=404,
            detail="No lottery data found"
        )

    logging.info(f"Retrieved lottery data: {lottery_data}")
    return {"result": lottery_data}
