from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ArchetypeEnum(str, Enum):
    """The 12 brand archetypes based on Carl Jung's psychology."""

    INNOCENT = "innocent"
    EXPLORER = "explorer"
    SAGE = "sage"
    HERO = "hero"
    OUTLAW = "outlaw"
    MAGICIAN = "magician"
    REGULAR_GUY = "regular_guy"
    LOVER = "lover"
    JESTER = "jester"
    CAREGIVER = "caregiver"
    CREATOR = "creator"
    RULER = "ruler"


class BrandPersonality(BaseModel):
    """Brand personality traits and characteristics."""

    personality_traits: List[str] = Field(
        ..., description="Key personality traits that define the brand's character"
    )
    tone_of_voice: str = Field(
        ..., description="How the brand communicates and speaks to its audience"
    )
    communication_style: str = Field(
        ..., description="Overall style and approach to communication"
    )
    brand_voice_attributes: List[str] = Field(
        ...,
        description="Specific voice attributes (e.g., friendly, authoritative, playful)",
    )


class BrandArchetype(BaseModel):
    """Brand archetype definition and characteristics."""

    primary_archetype: ArchetypeEnum = Field(
        ..., description="The primary brand archetype"
    )
    secondary_archetype: Optional[ArchetypeEnum] = Field(
        None, description="Optional secondary archetype for brand complexity"
    )
    archetype_description: str = Field(
        ..., description="Description of how this archetype manifests in the brand"
    )
    core_desire: str = Field(
        ..., description="The fundamental desire that drives this archetype"
    )
    fear: str = Field(..., description="What this archetype fears most")
    strategy: str = Field(
        ..., description="How this archetype typically achieves its goals"
    )


class EmotionalConnection(BaseModel):
    """Emotional aspects of brand connection."""

    emotional_benefits: List[str] = Field(
        ..., description="Emotional benefits customers gain from the brand"
    )
    brand_feelings: List[str] = Field(
        ..., description="Feelings the brand evokes in customers"
    )
    aspirational_identity: str = Field(
        ..., description="The aspirational identity customers associate with the brand"
    )
    emotional_triggers: List[str] = Field(
        ..., description="Key emotional triggers the brand activates"
    )


class BrandEmotion(BaseModel):
    """Complete emotional brand framework."""

    archetype: BrandArchetype
    personality: BrandPersonality
    emotional_connection: EmotionalConnection


class BrandEmotionResponse(BaseModel):
    """Response model for brand emotional analysis."""

    brand_name: str = Field(..., description="Name of the brand")
    emotion: BrandEmotion

    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "TechCorp Solutions",
                "emotion": {
                    "archetype": {
                        "primary_archetype": "sage",
                        "secondary_archetype": "hero",
                        "archetype_description": "A wise guide that empowers others to overcome technological challenges and achieve their business goals.",
                        "core_desire": "To understand the world and share knowledge to help others succeed",
                        "fear": "Being deceived or ignorant, leading others astray",
                        "strategy": "Seek truth and share wisdom through reliable, well-researched solutions",
                    },
                    "personality": {
                        "personality_traits": [
                            "Knowledgeable",
                            "Trustworthy",
                            "Innovative",
                            "Approachable",
                            "Reliable",
                        ],
                        "tone_of_voice": "Confident yet humble, informative but not condescending",
                        "communication_style": "Clear, educational, and solution-focused",
                        "brand_voice_attributes": [
                            "Expert",
                            "Helpful",
                            "Patient",
                            "Professional",
                            "Inspiring",
                        ],
                    },
                    "emotional_connection": {
                        "emotional_benefits": [
                            "Confidence in technology decisions",
                            "Sense of empowerment",
                            "Reduced anxiety about tech complexity",
                        ],
                        "brand_feelings": [
                            "Trust",
                            "Capability",
                            "Progress",
                            "Security",
                            "Innovation",
                        ],
                        "aspirational_identity": "A forward-thinking business leader who makes smart technology decisions",
                        "emotional_triggers": [
                            "Fear of falling behind",
                            "Desire for growth",
                            "Need for reliability",
                            "Aspiration for innovation",
                        ],
                    },
                },
            }
        }
