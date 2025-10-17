"""
Tests for the Branding API endpoints.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


class TestBrandingAPI:
    """Test class for branding API endpoints."""

    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/api/v1/branding/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "branding"

    def test_supported_formats(self, client: TestClient):
        """Test the supported formats endpoint."""
        response = client.get("/api/v1/branding/supported-formats")

        assert response.status_code == 200
        data = response.json()
        assert "supported_formats" in data
        assert "max_file_size" in data
        assert "encoding" in data

        formats = data["supported_formats"]
        assert len(formats) > 0
        # Only PDF is supported now
        mime_types = [fmt["mime_type"] for fmt in formats]
        assert "application/pdf" in mime_types
        assert len(mime_types) == 1

    # Removed text/plain test since only PDF is supported now

    @pytest.mark.integration
    def test_create_golden_circle_with_pdf_file(
        self, client: TestClient, sample_pdf_file: Path
    ):
        """Test creating golden circle with PDF file."""
        with open(sample_pdf_file, "rb") as f:
            files = {"interview_file": (sample_pdf_file.name, f, "application/pdf")}
            data = {"brand_name": "Olillac Brand"}

            response = client.post(
                "/api/v1/branding/create-from-interview", files=files, data=data
            )

        assert response.status_code == 200
        result = response.json()

        # Check response structure
        assert "brand_name" in result
        assert "golden_circle" in result
        assert result["brand_name"] == "Olillac Brand"

        golden_circle = result["golden_circle"]
        assert "why" in golden_circle
        assert "how" in golden_circle
        assert "what" in golden_circle

        # Check that values are not empty
        assert len(golden_circle["why"]) > 0
        assert len(golden_circle["how"]) > 0
        assert len(golden_circle["what"]) > 0

    def test_create_golden_circle_without_brand_name(
        self, client: TestClient, sample_pdf_file: Path
    ):
        """Test creating golden circle without providing brand name (should extract from filename)."""
        with open(sample_pdf_file, "rb") as f:
            files = {"interview_file": (sample_pdf_file.name, f, "application/pdf")}

            response = client.post(
                "/api/v1/branding/create-from-interview", files=files
            )

        assert response.status_code == 200
        result = response.json()

        # Should extract brand name from filename
        assert "brand_name" in result
        # The service should clean up the filename and create a brand name
        assert len(result["brand_name"]) > 0

    def test_create_golden_circle_invalid_file_type(self, client: TestClient):
        """Test creating golden circle with invalid file type."""
        files = {"interview_file": ("test.jpg", b"fake image content", "image/jpeg")}
        data = {"brand_name": "Test Company"}

        response = client.post(
            "/api/v1/branding/create-from-interview", files=files, data=data
        )

        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert "Unsupported file type" in error_detail

    def test_create_golden_circle_no_file(self, client: TestClient):
        """Test creating golden circle without providing a file."""
        data = {"brand_name": "Test Company"}

        response = client.post("/api/v1/branding/create-from-interview", data=data)

        # FastAPI should return 422 for missing required file
        assert response.status_code == 422

    def test_create_golden_circle_empty_file(self, client: TestClient):
        """Test creating golden circle with empty file."""
        files = {"interview_file": ("empty.pdf", b"", "application/pdf")}
        data = {"brand_name": "Test Company"}

        response = client.post(
            "/api/v1/branding/create-from-interview", files=files, data=data
        )

        # Empty PDF should trigger extraction error handled as 400
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert "Failed to extract text" in error_detail


class TestGoldenCircleContent:
    """Test class for validating Golden Circle content quality."""

    @pytest.mark.integration
    def test_golden_circle_content_structure(
        self, client: TestClient, sample_pdf_file: Path
    ):
        """Test that Golden Circle content follows expected structure."""
        with open(sample_pdf_file, "rb") as f:
            files = {"interview_file": (sample_pdf_file.name, f, "application/pdf")}
            data = {"brand_name": "Innovation Corp"}

            response = client.post(
                "/api/v1/branding/create-from-interview", files=files, data=data
            )
        result = response.json()
        golden_circle = result["golden_circle"]

        # Accept English and Spanish cues so the test is robust to BAML output language
        why = golden_circle["why"].lower()
        why_tokens_en = ["believe", "purpose", "exist", "mission", "why"]
        why_tokens_es = [
            "creemos",
            "propósito",
            "proposito",
            "misión",
            "mision",
            "por qué",
            "porque",
            "razón",
            "razon",
        ]
        assert any(word in why for word in (why_tokens_en + why_tokens_es))

        # How should be about process/values
        how = golden_circle["how"].lower()
        how_tokens_en = ["how", "process", "approach", "way", "method"]
        how_tokens_es = [
            "cómo",
            "como",
            "proceso",
            "enfoque",
            "manera",
            "método",
            "metodo",
        ]
        assert any(word in how for word in (how_tokens_en + how_tokens_es))

        # What should be about products/services
        what = golden_circle["what"].lower()
        what_tokens_en = [
            "provide",
            "offer",
            "deliver",
            "create",
            "service",
            "product",
            "products",
            "services",
        ]
        what_tokens_es = [
            "ofrecer",
            "ofrece",
            "proveer",
            "entregar",
            "crear",
            "servicio",
            "servicios",
            "producto",
            "productos",
        ]
        assert any(word in what for word in (what_tokens_en + what_tokens_es))

    @pytest.mark.unit
    def test_response_model_validation(self, client: TestClient, sample_pdf_file: Path):
        """Test that response follows the expected Pydantic model."""
        with open(sample_pdf_file, "rb") as f:
            files = {"interview_file": (sample_pdf_file.name, f, "application/pdf")}
            data = {"brand_name": "Test Company"}

            response = client.post(
                "/api/v1/branding/create-from-interview", files=files, data=data
            )
        result = response.json()

        # Validate against expected schema
        required_fields = ["brand_name", "golden_circle"]
        for field in required_fields:
            assert field in result

        golden_circle_fields = ["why", "how", "what"]
        for field in golden_circle_fields:
            assert field in result["golden_circle"]
            assert isinstance(result["golden_circle"][field], str)
            assert len(result["golden_circle"][field]) > 10  # Meaningful content
