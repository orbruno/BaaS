from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional

from app.models.pydantic.brand_strategy import GoldenCircleResponse
from app.services.branding_service import BrandingService, get_branding_service

router = APIRouter(prefix="/branding", tags=["branding"])


@router.post(
    "/create-from-interview",
    response_model=GoldenCircleResponse,
    summary="Create Golden Circle from Interview",
    description="Upload an interview file and generate the Golden Circle (Why, How, What) framework for brand positioning.",
)
async def create_brand_identity_from_interview(
    interview_file: UploadFile = File(
        ..., description="Interview file (text, markdown, or PDF)"
    ),
    brand_name: Optional[str] = Form(None, description="Optional brand name override"),
    branding_service: BrandingService = Depends(get_branding_service),
) -> GoldenCircleResponse:
    """
    Create a Golden Circle analysis from an uploaded interview file.

    This endpoint processes an interview file containing conversations with brand stakeholders
    and generates the Golden Circle framework:
    - Why: The purpose, belief, or cause - why the brand exists
    - How: The process or values - how the brand fulfills its purpose
    - What: The products or services - what the brand actually does

    Args:
        interview_file: The uploaded interview file (supports .txt, .md, .pdf)
        brand_name: Optional brand name (if not provided, will be extracted from filename)
        branding_service: Injected branding service

    Returns:
        GoldenCircleResponse: Golden Circle analysis (Why, How, What)

    Raises:
        HTTPException: If file processing fails or unsupported file type
    """
    return await branding_service.create_golden_circle_response(
        interview_file=interview_file, brand_name=brand_name
    )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the branding service is healthy and operational.",
)
async def health_check(
    branding_service: BrandingService = Depends(get_branding_service),
):
    """Simple health check endpoint for the branding service."""
    return branding_service.get_health_status()


@router.get(
    "/supported-formats",
    summary="Get Supported File Formats",
    description="Get a list of supported file formats for interview uploads.",
)
async def get_supported_formats(
    branding_service: BrandingService = Depends(get_branding_service),
):
    """Get supported file formats for interview uploads."""
    return branding_service.get_supported_file_formats()
