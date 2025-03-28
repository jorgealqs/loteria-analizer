from pydantic import BaseModel
from typing import Optional


class AmazonProductResponse(BaseModel):
    title: str
    price: Optional[str] = None
    availability: Optional[str] = None
    reviews: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
