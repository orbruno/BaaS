from typing import Optional
import logging
from fastapi import UploadFile, HTTPException

# Import response models - using TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.pydantic.brand_strategy import (
        GoldenCircleResponse,
        BrandStrategyResponse,
    )

logger = logging.getLogger(__name__)


class BrandingService:
    """Service for handling brand identity creation from interview files."""

    def __init__(self):
        # Initialize any dependencies here (database, AI clients, etc.)
        pass

    async def create_brand_identity_from_interview(
        self, interview_file: UploadFile, brand_name: Optional[str] = None
    ) -> dict:
        """
        Process an interview file and generate brand identity.

        Args:
            interview_file: The uploaded interview file
            brand_name: Optional brand name override

        Returns:
            dict: Generated brand identity data

        Raises:
            HTTPException: If file processing fails
        """
        try:
            # Validate file
            if not interview_file.filename:
                raise HTTPException(status_code=400, detail="No file provided")

            # Check file type (PDF only)
            allowed_types = ["application/pdf"]
            if interview_file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type. Allowed types: {allowed_types}",
                )

            # Read file content (bytes)
            pdf_bytes = await interview_file.read()

            # Reset file position for potential re-reading
            await interview_file.seek(0)

            # Extract text from PDF using Docling
            extracted_text = self._extract_text_from_pdf_bytes(pdf_bytes)

            # Process the interview content
            brand_identity = await self._process_interview_content(
                extracted_text,
                brand_name
                or self._extract_brand_name_from_filename(interview_file.filename),
            )

            logger.info(
                f"Successfully generated brand identity for {brand_identity.get('brand_name')}"
            )
            return brand_identity

        except HTTPException:
            # Re-raise HTTP exceptions (like 400 validation errors) as-is
            raise
        except UnicodeDecodeError:
            # Kept for backward compatibility, though we no longer decode directly
            raise HTTPException(
                status_code=400, detail="File encoding not supported. Please use UTF-8."
            )
        except Exception as e:
            logger.error(f"Error processing interview file: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Internal server error processing file"
            )

    async def _process_interview_content(self, content: str, brand_name: str) -> dict:
        """
        Process the interview content and generate brand identity.
        This is where you'll integrate with BAML or other AI services.
        """
        # TODO: Integrate with BAML client for AI processing
        # For now, returning a mock response

        # Basic content analysis (you'll replace this with AI processing)
        word_count = len(content.split())

        # Mock brand identity generation
        brand_identity = {
            "brand_name": brand_name,
            "interview_summary": {
                "word_count": word_count,
                "content_preview": content[:200] + "..."
                if len(content) > 200
                else content,
            },
            "brand_attributes": {
                "tone": "professional",  # AI-generated
                "values": ["innovation", "quality", "customer-focus"],  # AI-generated
                "target_audience": "business professionals",  # AI-generated
                "brand_personality": "modern and approachable",  # AI-generated
            },
            "visual_guidelines": {
                "primary_colors": ["#2E3440", "#5E81AC"],  # AI-generated
                "font_suggestions": ["Helvetica", "Open Sans"],  # AI-generated
                "style": "minimalist",  # AI-generated
            },
            "messaging": {
                "tagline": "Innovation meets excellence",  # AI-generated
                "value_proposition": "Delivering quality solutions for modern businesses",  # AI-generated
            },
        }

        return brand_identity

    async def _process_interview_for_golden_circle(
        self, content: str, brand_name: str
    ) -> dict:
        """
        Process the interview content and generate Golden Circle analysis.
        This focuses only on Why, How, What.
        """
        # TODO: Integrate with BAML client for AI processing
        # For now, returning a mock Golden Circle response

        # Mock Golden Circle generation based on content analysis
        golden_circle = {
            "brand_name": brand_name,
            "golden_circle": {
                "why": f"We believe that businesses like {brand_name} should create meaningful impact by solving real problems and empowering their customers to achieve their goals.",
                "how": "Our approach focuses on innovative solutions and a clear process: we listen, iterate, and deliver with high quality standards and reliable service. This method builds genuine relationships with customers through transparency.",
                "what": f"{brand_name} provides professional services and solutions that help clients streamline their operations and grow their business effectively.",
            },
        }

        return golden_circle

    async def create_golden_circle_from_interview(
        self, interview_file: UploadFile, brand_name: Optional[str] = None
    ) -> dict:
        """
        Process an interview file and generate Golden Circle (Why, How, What) analysis.

        Args:
            interview_file: The uploaded interview file
            brand_name: Optional brand name override

        Returns:
            dict: Golden Circle data (why, how, what)

        Raises:
            HTTPException: If file processing fails
        """
        try:
            # Validate file
            if not interview_file.filename:
                raise HTTPException(status_code=400, detail="No file provided")

            # Check file type (PDF only)
            allowed_types = ["application/pdf"]
            if interview_file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type. Allowed types: {allowed_types}",
                )

            # Read file content (bytes)
            pdf_bytes = await interview_file.read()

            # Reset file position for potential re-reading
            await interview_file.seek(0)

            # Extract text from PDF using Docling
            extracted_text = self._extract_text_from_pdf_bytes(pdf_bytes)

            # Prefer BAML to extract the Golden Circle directly from markdown
            try:
                from app.models.BAML.baml_client.sync_client import (
                    b as baml_client,
                )

                baml_resp = baml_client.ExtractGoldenCircleFromMarkdown(
                    markdown=extracted_text
                )
                golden_circle = baml_resp.model_dump()

                # If a brand_name was explicitly provided, override the inferred one
                if brand_name:
                    golden_circle["brand_name"] = brand_name

            except Exception as e:
                # Fallback to heuristic/mock processing to keep service resilient (and tests offline)
                logger.warning(
                    f"BAML Golden Circle extraction failed ({type(e).__name__}: {e}). Falling back to heuristic generation."
                )
                golden_circle = await self._process_interview_for_golden_circle(
                    extracted_text,
                    brand_name
                    or self._extract_brand_name_from_filename(interview_file.filename),
                )

            logger.info(
                f"Successfully generated Golden Circle for {golden_circle.get('brand_name')}"
            )
            return golden_circle

        except HTTPException:
            # Re-raise HTTP exceptions (like 400 validation errors) as-is
            raise
        except UnicodeDecodeError:
            # Kept for backward compatibility, though we no longer decode directly
            raise HTTPException(
                status_code=400, detail="File encoding not supported. Please use UTF-8."
            )
        except Exception as e:
            logger.error(f"Error processing interview file for Golden Circle: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Internal server error processing file"
            )

    async def create_golden_circle_response(
        self, interview_file: UploadFile, brand_name: Optional[str] = None
    ) -> "GoldenCircleResponse":
        """
        Complete business logic for creating Golden Circle from interview.
        Returns a validated Pydantic response model.

        Args:
            interview_file: The uploaded interview file
            brand_name: Optional brand name override

        Returns:
            GoldenCircleResponse: Validated Golden Circle response model

        Raises:
            HTTPException: If processing fails
        """
        from app.models.pydantic.brand_strategy import GoldenCircleResponse

        try:
            # Process the interview and generate Golden Circle
            golden_circle_data = await self.create_golden_circle_from_interview(
                interview_file=interview_file, brand_name=brand_name
            )

            # Convert to Pydantic model for response validation
            return GoldenCircleResponse(**golden_circle_data)

        except HTTPException:
            # Re-raise HTTP exceptions from the service
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Golden Circle creation: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while processing the Golden Circle request",
            )

    def _extract_brand_name_from_filename(self, filename: str) -> str:
        """Extract brand name from filename, removing extension and cleaning up."""
        import os

        base_name = os.path.splitext(filename)[0]
        # Clean up common patterns
        return (
            base_name.replace("_interview", "")
            .replace("-interview", "")
            .replace("_", " ")
            .title()
        )

    async def create_brand_identity_response(
        self, interview_file: UploadFile, brand_name: Optional[str] = None
    ) -> "BrandStrategyResponse":
        """
        Complete business logic for creating brand identity from interview.
        Returns a validated Pydantic response model.

        Args:
            interview_file: The uploaded interview file
            brand_name: Optional brand name override

        Returns:
            BrandIdentityResponse: Validated response model

        Raises:
            HTTPException: If processing fails
        """
        from app.models.pydantic.brand_strategy import BrandStrategyResponse

        try:
            # Process the interview and generate brand identity
            brand_identity_data = await self.create_brand_identity_from_interview(
                interview_file=interview_file, brand_name=brand_name
            )

            # Convert to Pydantic model for response validation
            return BrandStrategyResponse(**brand_identity_data)

        except HTTPException:
            # Re-raise HTTP exceptions from the service
            raise
        except Exception as e:
            logger.error(f"Unexpected error in brand identity creation: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while processing the brand identity request",
            )

    def get_health_status(self) -> dict:
        """Get the health status of the branding service."""
        return {"status": "healthy", "service": "branding"}

    def get_supported_file_formats(self) -> dict:
        """Get supported file formats and configuration."""
        return {
            "supported_formats": [
                {
                    "extension": ".pdf",
                    "mime_type": "application/pdf",
                    "description": "PDF documents",
                }
            ],
            "max_file_size": "10MB",
            "encoding": "UTF-8",
        }

    def _extract_text_from_pdf_bytes(self, pdf_bytes: bytes) -> str:
        """Extract text (markdown) from PDF bytes using Docling.

        Args:
            pdf_bytes: Raw PDF bytes

        Returns:
            str: Extracted text content (markdown)

        Raises:
            HTTPException: If extraction fails
        """
        try:
            import tempfile
            from docling.document_converter import DocumentConverter

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
                tmp.write(pdf_bytes)
                tmp.flush()

                converter = DocumentConverter()
                result = converter.convert(tmp.name)
                # Export to markdown for better structure; plain text also possible
                return result.document.export_to_markdown()
        except HTTPException:
            # Bubble up service-specific HTTP errors
            raise
        except Exception as e:
            logger.error(f"Docling PDF extraction failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from PDF. Ensure the PDF is readable.",
            )


def get_branding_service() -> BrandingService:
    """Dependency injection for BrandingService."""
    return BrandingService()
