"""
Lottery Analyzer API
Main application module that initializes the FastAPI application and includes
all routes.

This module serves as the entry point for the Lottery Analyzer API application.
It configures the FastAPI instance and includes all route modules.
"""

from fastapi import FastAPI, Response
from app.routes.endpoints import router
from app.routes.password_key import router_password_key
from app.routes.amazon.router import router_amazon

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Lottery Analyzer",
    description="API for analyzing lottery draws and statistics",
    version="1.0"
)

# Include routers from different modules
app.include_router(router)
app.include_router(router_password_key)
app.include_router(router_amazon)


@app.get(
    "/",
    summary="Home endpoint",
    description="Returns a welcome message for the Lottery Analyzer API",
    response_description="HTML welcome message"
)
def home() -> Response:
    """
    Root endpoint that displays a welcome message.

    Returns:
        Response: HTML response containing the welcome message
    """
    return Response(
        content="<h1>Welcome to the Lottery Analyzer</h1>",
        media_type="text/html"
    )
