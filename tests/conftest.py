"""
Test configuration and fixtures for the Branding API tests.
"""
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.branding import router


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_data_dir():
    """Path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_pdf_file(test_data_dir):
    """Path to the sample PDF file."""
    pdf_files = list(test_data_dir.glob("*.pdf"))
    if not pdf_files:
        pytest.skip("No PDF files found in test data directory")
    return pdf_files[0]


@pytest.fixture
def sample_text_content():
    """Sample interview content for testing."""
    return """
Brand Interview - Test Company

Q: What is your company's mission?
A: We exist to solve problems and create value for our customers through innovative solutions.

Q: What are your core values?
A: Innovation, integrity, and customer success drive everything we do.

Q: How do you want customers to feel?
A: Confident, empowered, and supported in achieving their goals.
""".strip()
