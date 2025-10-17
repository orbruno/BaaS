# Pydantic models package

# Brand Strategy Models (Currently Active)
from .brand_strategy import (
    GoldenCircle,
    BrandPositioning,
    BrandValues,
    BrandStrategy,
    BrandStrategyResponse,
    GoldenCircleResponse,
)

# TODO: Uncomment when implementing emotion and visual features
# # Brand Emotion Models (Emotional Component)
# from .brand_emotion import (
#     ArchetypeEnum,
#     BrandPersonality,
#     BrandArchetype,
#     EmotionalConnection,
#     BrandEmotion,
#     BrandEmotionResponse,
# )

# # Brand Visual Models (Visual Component)
# from .brand_visual import (
#     ColorPalette,
#     Typography,
#     LogoGuidelines,
#     VisualStyleEnum,
#     DesignElements,
#     BrandVisual,
#     BrandVisualResponse,
# )

__all__ = [
    # Strategy (Active Models)
    "GoldenCircle",
    "BrandPositioning",
    "BrandValues",
    "BrandStrategy",
    "BrandStrategyResponse",
    "GoldenCircleResponse",
    # TODO: Uncomment when implementing emotion and visual features
    # # Emotion
    # "ArchetypeEnum",
    # "BrandPersonality",
    # "BrandArchetype",
    # "EmotionalConnection",
    # "BrandEmotion",
    # "BrandEmotionResponse",
    # # Visual
    # "ColorPalette",
    # "Typography",
    # "LogoGuidelines",
    # "VisualStyleEnum",
    # "DesignElements",
    # "BrandVisual",
    # "BrandVisualResponse",
]
