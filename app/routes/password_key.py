"""
Password Key Router Module
-------------------------
This module provides endpoints for password generation and validation.

The module includes two main functionalities:
1. Password Generation: Creates secure random passwords of specified length
2. Password Validation: Checks if passwords meet security requirements

Security Requirements:
- Minimum length: 8 characters
- Must contain at least one number
- Must contain at least one letter
- Must contain at least one special character

Author: Jorge Alberto Quiroz Sierra
Date: 2024
Version: 1.0
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict
import logging
import random
import string

# Configure logging with UTF-8 encoding for proper character handling
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    encoding='utf-8'
)

logger = logging.getLogger(__name__)

router_password_key = APIRouter(
    prefix="/api/password-key",
    tags=["password-key"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)


def generate_password(length: int = 12) -> str:
    """
    Generates a cryptographically secure password of specified length.

    The generated password includes a mix of:
    - ASCII letters (both uppercase and lowercase)
    - Digits (0-9)
    - Special characters (punctuation)

    Args:
        length (int, optional): Length of the password to generate.
        Defaults to 12.

    Returns:
        str: A randomly generated password string.

    Raises:
        ValueError: If length is less than 6 characters.

    Example:
        >>> generate_password(16)
        'Kj#9mP$2nL&5vX@4'
    """
    if length < 6:
        raise ValueError("Password length must be at least 6 characters.")
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def validate_password(password: str) -> Dict[str, str]:
    """
    Validates a password against security requirements.

    Security checks include:
    1. Minimum length of 8 characters
    2. Presence of at least one number
    3. Presence of at least one letter
    4. Presence of at least one special character

    Args:
        password (str): The password string to validate.

    Returns:
        Dict[str, str]: A dictionary containing:
            - 'valid': "true" or "false"
            - 'reason': Description of validation result or failure reason

    Example:
        >>> validate_password("SecurePass123!")
        {'valid': 'true', 'reason': 'Password is strong.'}
        >>> validate_password("weak")
        {'valid': 'false', 'reason':
        'Password must be at least 8 characters long.'}
    """
    # Check minimum length requirement
    if len(password) < 8:
        return {
            "valid": "false",
            "reason": "Password must be at least 8 characters long."
        }

    # Check for at least one number
    if not any(char.isdigit() for char in password):
        return {
            "valid": "false",
            "reason": "Password must contain at least one number."
        }

    # Check for at least one letter
    if not any(char.isalpha() for char in password):
        return {
            "valid": "false",
            "reason": "Password must contain at least one letter."
        }

    # Check for at least one special character
    if not any(char in string.punctuation for char in password):
        return {
            "valid": "false",
            "reason": "Password must contain at least one special character."
        }

    return {"valid": "true", "reason": "Password is strong."}


@router_password_key.get(
    "/generate",
    response_model=Dict[str, str],
    summary="Generate a secure password",
    description=(
        "Generates a random secure password of specified length "
        "(6-64 characters)."
    ),
    responses={
        200: {
            "description": "Successfully generated password",
            "content": {
                "application/json": {
                    "example": {"password": "Kj#9mP$2nL&5"}
                }
            }
        },
        400: {
            "description": "Invalid length parameter",
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Password length must be at least 6 characters."
                            )
                        }
                }
            }
        }
    }
)
async def api_generate_password(
    length: int = Query(
        12,
        ge=6,
        le=64,
        description=(
            "Length of the password to generate (between 6 and 64 characters)"
        )
    )
) -> Dict[str, str]:
    """
    API endpoint to generate a secure password.

    Args:
        length (int): Desired length of the password (6-64 characters).
                    Defaults to 12.

    Returns:
        Dict[str, str]: Dictionary containing the generated password.

    Raises:
        HTTPException: If the length parameter is invalid.
    """
    try:
        logger.info(f"Generating password of length {length}")
        password = generate_password(length)
        logger.info("Password generated successfully")
        return {"password": password}
    except ValueError as e:
        logger.error(f"Password generation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router_password_key.post(
    "/validate",
    response_model=Dict[str, str],
    summary="Validate password strength",
    description="Validates if a password meets security requirements.",
    responses={
        200: {
            "description": "Password validation result",
            "content": {
                "application/json": {
                    "example": {
                        "valid": "true",
                        "reason": "Password is strong."
                    }
                }
            }
        }
    }
)
async def api_validate_password(password: str) -> Dict[str, str]:
    """
    API endpoint to validate password strength.

    Args:
        password (str): The password to validate.

    Returns:
        Dict[str, str]: Dictionary containing validation result and reason.

    Example:
        Request: POST /api/password-key/validate
        Body: {"password": "SecurePass123!"}
        Response: {"valid": "true", "reason": "Password is strong."}
    """
    logger.info("Processing password validation request")
    result = validate_password(password)
    logger.info(f"Password validation completed: {result['valid']}")
    return result
