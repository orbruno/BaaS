from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class ColorPalette(BaseModel):
    """Brand color palette definition."""

    primary_colors: List[str] = Field(
        ..., description="Primary brand colors (hex codes)"
    )
    secondary_colors: List[str] = Field(
        ..., description="Secondary supporting colors (hex codes)"
    )
    neutral_colors: List[str] = Field(
        ..., description="Neutral colors for backgrounds and text (hex codes)"
    )
    accent_colors: List[str] = Field(
        ..., description="Accent colors for highlights and emphasis (hex codes)"
    )


class Typography(BaseModel):
    """Typography guidelines and font selections."""

    primary_font: str = Field(
        ..., description="Primary brand font for headings and important text"
    )
    secondary_font: str = Field(
        ..., description="Secondary font for body text and supporting content"
    )
    display_font: Optional[str] = Field(
        None, description="Optional display font for special occasions"
    )
    font_weights: List[str] = Field(
        ..., description="Available font weights (e.g., light, regular, bold)"
    )
    font_characteristics: List[str] = Field(
        ...,
        description="Characteristics of the chosen fonts (e.g., modern, serif, geometric)",
    )


class LogoGuidelines(BaseModel):
    """Logo usage and guidelines."""

    logo_style: str = Field(
        ...,
        description="Overall style of the logo (e.g., wordmark, symbol, combination)",
    )
    logo_concept: str = Field(
        ..., description="Conceptual description of what the logo represents"
    )
    usage_guidelines: List[str] = Field(
        ..., description="Key guidelines for logo usage and placement"
    )
    minimum_size: str = Field(
        ..., description="Minimum size requirements for logo visibility"
    )
    clear_space: str = Field(..., description="Required clear space around the logo")


class VisualStyleEnum(str, Enum):
    """Visual style categories."""

    MINIMALIST = "minimalist"
    MODERN = "modern"
    CLASSIC = "classic"
    PLAYFUL = "playful"
    SOPHISTICATED = "sophisticated"
    BOLD = "bold"
    ORGANIC = "organic"
    INDUSTRIAL = "industrial"
    LUXURY = "luxury"
    VINTAGE = "vintage"


class DesignElements(BaseModel):
    """Visual design elements and patterns."""

    visual_style: VisualStyleEnum = Field(
        ..., description="Primary visual style category"
    )
    design_principles: List[str] = Field(
        ..., description="Key design principles that guide visual decisions"
    )
    graphic_elements: List[str] = Field(
        ...,
        description="Characteristic graphic elements (e.g., geometric shapes, organic forms)",
    )
    image_style: str = Field(
        ..., description="Preferred style for photography and imagery"
    )
    layout_approach: str = Field(..., description="Approach to layout and composition")


class BrandVisual(BaseModel):
    """Complete visual brand framework."""

    color_palette: ColorPalette
    typography: Typography
    logo_guidelines: LogoGuidelines
    design_elements: DesignElements


class BrandVisualResponse(BaseModel):
    """Response model for brand visual analysis."""

    brand_name: str = Field(..., description="Name of the brand")
    visual: BrandVisual

    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "TechCorp Solutions",
                "visual": {
                    "color_palette": {
                        "primary_colors": ["#2E3440", "#5E81AC"],
                        "secondary_colors": ["#88C0D0", "#81A1C1"],
                        "neutral_colors": ["#ECEFF4", "#E5E9F0", "#D8DEE9"],
                        "accent_colors": ["#BF616A", "#EBCB8B"],
                    },
                    "typography": {
                        "primary_font": "Inter",
                        "secondary_font": "Source Sans Pro",
                        "display_font": "Poppins",
                        "font_weights": ["300", "400", "500", "600", "700"],
                        "font_characteristics": [
                            "Modern",
                            "Clean",
                            "Geometric",
                            "Highly legible",
                        ],
                    },
                    "logo_guidelines": {
                        "logo_style": "Combination mark with wordmark",
                        "logo_concept": "A modern geometric symbol representing connection and growth, paired with clean typography",
                        "usage_guidelines": [
                            "Always maintain proper clear space",
                            "Use approved color variations only",
                            "Never distort or rotate",
                        ],
                        "minimum_size": "24px height for digital, 0.5 inch height for print",
                        "clear_space": "Minimum distance equal to the height of the 'T' in the wordmark",
                    },
                    "design_elements": {
                        "visual_style": "modern",
                        "design_principles": [
                            "Simplicity",
                            "Clarity",
                            "Consistency",
                            "Purpose",
                        ],
                        "graphic_elements": [
                            "Clean geometric shapes",
                            "Subtle gradients",
                            "Generous white space",
                        ],
                        "image_style": "Clean, professional photography with good lighting and minimal distractions",
                        "layout_approach": "Grid-based layouts with clear hierarchy and generous spacing",
                    },
                },
            }
        }
