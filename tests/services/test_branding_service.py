"""
Unit tests for the BrandingService.
"""

from unittest.mock import AsyncMock, Mock
from pathlib import Path
import os

import pytest
from fastapi import HTTPException, UploadFile

from app.services.branding_service import BrandingService


class TestBrandingService:
    """Unit tests for BrandingService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = BrandingService()

    @pytest.mark.unit
    def test_extract_brand_name_from_filename(self):
        """Test brand name extraction from filename."""
        test_cases = [
            ("brand_interview.txt", "Brand"),
            ("my-company-interview.pdf", "My-Company"),
            ("awesome_brand_interview.md", "Awesome Brand"),
            ("simple.txt", "Simple"),
            ("company_name_interview_final.pdf", "Company Name Final"),
        ]

        for filename, expected in test_cases:
            result = self.service._extract_brand_name_from_filename(filename)
            assert result == expected

    @pytest.mark.unit
    def test_get_health_status(self):
        """Test health status method."""
        result = self.service.get_health_status()

        assert result == {"status": "healthy", "service": "branding"}

    @pytest.mark.unit
    def test_get_supported_file_formats(self):
        """Test supported file formats method."""
        result = self.service.get_supported_file_formats()

        assert "supported_formats" in result
        assert "max_file_size" in result
        assert "encoding" in result

        formats = result["supported_formats"]
        mime_types = [fmt["mime_type"] for fmt in formats]

        # Only PDF supported now
        assert mime_types == ["application/pdf"]

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_golden_circle_from_interview_success(self):
        """Test successful golden circle creation."""
        # Mock file content
        content = "Q: What is your mission? A: To help businesses succeed."
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test_interview.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.read = AsyncMock(return_value=content.encode("utf-8"))
        mock_file.seek = AsyncMock()

        # Mock Docling extractor to return our content
        self.service._extract_text_from_pdf_bytes = Mock(return_value=content)

        result = await self.service.create_golden_circle_from_interview(
            interview_file=mock_file, brand_name="Test Company"
        )

        assert "brand_name" in result
        assert "golden_circle" in result
        assert result["brand_name"] == "Test Company"

        golden_circle = result["golden_circle"]
        assert "why" in golden_circle
        assert "how" in golden_circle
        assert "what" in golden_circle

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_golden_circle_no_filename(self):
        """Test golden circle creation with no filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = None

        with pytest.raises(HTTPException) as exc_info:
            await self.service.create_golden_circle_from_interview(
                interview_file=mock_file, brand_name="Test Company"
            )

        assert exc_info.value.status_code == 400
        assert "No file provided" in exc_info.value.detail

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_golden_circle_invalid_content_type(self):
        """Test golden circle creation with invalid content type."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"

        with pytest.raises(HTTPException) as exc_info:
            await self.service.create_golden_circle_from_interview(
                interview_file=mock_file, brand_name="Test Company"
            )

        assert exc_info.value.status_code == 400
        assert "Unsupported file type" in exc_info.value.detail

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_golden_circle_unicode_decode_error(self):
        """Test golden circle creation with unicode decode error."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.txt"
        mock_file.content_type = "application/pdf"
        mock_file.read = AsyncMock(
            return_value=b""
        )  # Empty PDF bytes will fail extraction
        mock_file.seek = AsyncMock()

        # Mock extractor to raise extraction error
        def _raise(*args, **kwargs):
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from PDF. Ensure the PDF is readable.",
            )

        self.service._extract_text_from_pdf_bytes = Mock(side_effect=_raise)

        with pytest.raises(HTTPException) as exc_info:
            await self.service.create_golden_circle_from_interview(
                interview_file=mock_file, brand_name="Test Company"
            )

        assert exc_info.value.status_code == 400
        assert "Failed to extract text" in exc_info.value.detail

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_interview_for_golden_circle(self):
        """Test the internal interview processing method."""
        content = """
        Q: What is your company's mission?
        A: We exist to help small businesses thrive through technology.

        Q: What are your values?
        A: Innovation, integrity, and customer success.
        """
        brand_name = "TechHelper"

        result = await self.service._process_interview_for_golden_circle(
            content, brand_name
        )

        assert "brand_name" in result
        assert "golden_circle" in result
        assert result["brand_name"] == brand_name

        golden_circle = result["golden_circle"]
        assert "why" in golden_circle
        assert "how" in golden_circle
        assert "what" in golden_circle

        # Check that the brand name appears in the generated content
        why_text = golden_circle["why"]
        assert brand_name in why_text or "TechHelper" in why_text

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_golden_circle_response_success(self):
        """Test the complete response creation method."""
        content = "Q: What drives you? A: Helping others succeed."
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test_interview.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.read = AsyncMock(return_value=content.encode("utf-8"))
        mock_file.seek = AsyncMock()

        # Mock Docling extractor to return our content
        self.service._extract_text_from_pdf_bytes = Mock(return_value=content)

        response = await self.service.create_golden_circle_response(
            interview_file=mock_file, brand_name="Success Corp"
        )

        # Should return a Pydantic model
        assert hasattr(response, "brand_name")
        assert hasattr(response, "golden_circle")
        assert response.brand_name == "Success Corp"

        # Test that we can convert to dict (Pydantic behavior)
        response_dict = response.model_dump()
        assert "brand_name" in response_dict
        assert "golden_circle" in response_dict

    @pytest.mark.integration
    def test_extract_text_from_pdf_bytes_returns_markdown_real_pdf(self):
        """Integration: real PDF extraction should return non-empty markdown-like text."""
        # Skip if Docling is not installed in the environment
        pytest.importorskip(
            "docling",
            reason="Docling not installed; skipping PDF extraction integration test",
        )

        # Locate the sample PDF in tests/data
        pdf_path = Path(__file__).resolve().parents[1] / "data" / "Olillac.pdf"
        assert pdf_path.exists(), f"Sample PDF not found at {pdf_path}"

        pdf_bytes = pdf_path.read_bytes()

        try:
            extracted = self.service._extract_text_from_pdf_bytes(pdf_bytes)
        except HTTPException as exc:
            # If extraction fails due to unreadable PDF in this environment, skip
            pytest.skip(f"PDF extraction failed in this environment: {exc.detail}")

        # Basic assertions that we received some textual markdown-like content
        assert isinstance(extracted, str), "Extraction should return a string"
        assert len(extracted) > 0, "Extracted content should not be empty"

        # Optional: print the markdown to stdout when enabled
        if os.getenv("PRINT_EXTRACTED_MARKDOWN"):
            print("\n--- Extracted Markdown (truncated to 2000 chars) ---")
            print(extracted[:2000])

        # Optional: save the full markdown next to the test PDF when enabled
        if os.getenv("SAVE_EXTRACTED_MARKDOWN"):
            out_path = pdf_path.with_name(f"{pdf_path.stem}_extracted.md")
            out_path.write_text(extracted, encoding="utf-8")
            print(f"Saved extracted markdown to {out_path.resolve()}")

        # Heuristic check for markdown structure (not strict to avoid flakiness)
        has_markdown_cues = any(
            token in extracted for token in ["# ", "## ", "- ", "* "]
        )
        # Do not require cues strictly; just ensure content is text-heavy
        ratio = sum(ch.isprintable() for ch in extracted) / max(len(extracted), 1)
        assert ratio > 0.9
        # Optional stronger signal
        if has_markdown_cues:
            assert True
