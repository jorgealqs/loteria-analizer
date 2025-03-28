from fastapi import APIRouter, HTTPException
from app.routes.amazon.schemas import AmazonProductResponse
from app.routes.amazon.service import AmazonScraperService
from app.utils.logger import get_logger

logger = get_logger("amazon_router")

router_amazon = APIRouter(
    prefix="/amazon",
    tags=["Amazon Data"],
    responses={404: {"description": "Product not found"}}
)


@router_amazon.get("/product2/{asin}", response_model=AmazonProductResponse)
async def get_product_info(asin: str) -> AmazonProductResponse:
    """
    Get Amazon product information by ASIN.

    Args:
        asin: Amazon Standard Identification Number

    Returns:
        AmazonProductResponse: Product information
    """
    try:
        scraper = AmazonScraperService()
        return await scraper.get_product_info(asin)
    except Exception as e:
        logger.error(f"Error fetching product {asin}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
