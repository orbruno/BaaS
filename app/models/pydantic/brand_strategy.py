from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class GoldenCircle(BaseModel):
    """The Golden Circle framework: Why, How, What."""

    why: str = Field(
        ..., description="The purpose, belief, or cause - why the brand exists"
    )
    how: str = Field(
        ..., description="The process or values - how the brand fulfills its purpose"
    )
    what: str = Field(
        ..., description="The products or services - what the brand actually does"
    )


class BrandPositioning(BaseModel):
    """Strategic brand positioning elements."""

    value_proposition: str = Field(
        ..., description="Unique value proposition that differentiates the brand"
    )
    target_audience: str = Field(
        ..., description="Primary target audience and market segment"
    )
    competitive_advantage: str = Field(
        ..., description="Key competitive advantages and differentiators"
    )
    brand_promise: str = Field(
        ..., description="The promise or commitment the brand makes to customers"
    )


class BrandValues(BaseModel):
    """Core brand values and principles."""

    core_values: List[str] = Field(
        ..., description="Fundamental values that guide brand decisions"
    )
    mission_statement: str = Field(
        ..., description="Brand's mission and purpose statement"
    )
    vision_statement: str = Field(
        ..., description="Brand's long-term vision and aspirations"
    )


class BrandStrategy(BaseModel):
    """Complete brand strategy framework."""

    golden_circle: GoldenCircle
    positioning: BrandPositioning
    values: BrandValues


class BrandStrategyResponse(BaseModel):
    """Response model for brand strategy analysis."""

    brand_name: str = Field(..., description="Name of the brand")
    strategy: BrandStrategy

    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "TechCorp Solutions",
                "strategy": {
                    "golden_circle": {
                        "why": "We believe that technology should empower people to achieve their dreams and create meaningful change in the world.",
                        "how": "By creating intuitive, reliable, and innovative solutions that prioritize user experience and genuine problem-solving over flashy features.",
                        "what": "We develop software platforms and digital tools that help businesses streamline operations and connect with their customers.",
                    },
                    "positioning": {
                        "value_proposition": "We deliver technology solutions that are both powerful and intuitive, helping businesses achieve more with less complexity.",
                        "target_audience": "Mid-market businesses seeking to modernize their operations without overwhelming complexity.",
                        "competitive_advantage": "Our unique combination of cutting-edge technology with user-centric design and exceptional customer support.",
                        "brand_promise": "Technology that works as hard as you do, without the headaches.",
                    },
                    "values": {
                        "core_values": [
                            "Innovation",
                            "Simplicity",
                            "Reliability",
                            "Customer Success",
                        ],
                        "mission_statement": "To democratize powerful technology by making it accessible and intuitive for businesses of all sizes.",
                        "vision_statement": "A world where technology amplifies human potential rather than complicating it.",
                    },
                },
            }
        }


class GoldenCircleResponse(BaseModel):
    """Simplified response model for Golden Circle analysis only."""

    brand_name: str = Field(..., description="Name of the brand")
    golden_circle: GoldenCircle

    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "TechCorp Solutions",
                "golden_circle": {
                    "why": "We believe that technology should empower people to achieve their dreams and create meaningful change in the world.",
                    "how": "By creating intuitive, reliable, and innovative solutions that prioritize user experience and genuine problem-solving over flashy features.",
                    "what": "We develop software platforms and digital tools that help businesses streamline operations and connect with their customers.",
                },
            }
        }
