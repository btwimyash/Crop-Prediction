from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CropPrediction(BaseModel):
    """Single crop prediction with confidence"""
    crop: str
    confidence: float  # 0-100
    risk_level: Optional[str] = None


class PredictResponse(BaseModel):
    """Response model for crop predictions"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "top_predictions": [
                    {"crop": "Rice", "confidence": 87},
                    {"crop": "Maize", "confidence": 9},
                    {"crop": "Cotton", "confidence": 4}
                ],
                "risk_level": "Medium",
                "rainfall": 156.5,
                "temperature": 28.3,
                "humidity": 72,
                "advisory_message": "Rice is highly recommended for Pune in June with moderate rainfall...",
                "soil_values_used": {
                    "nitrogen": 90,
                    "phosphorous": 40,
                    "potassium": 40,
                    "ph": 6.5
                }
            }
        }
    )
    
    top_predictions: List[CropPrediction]
    risk_level: str  # Low, Medium, High
    rainfall: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    advisory_message: str
    soil_values_used: dict  # Show which values were used


class ChatbotResponse(BaseModel):
    """Response model for chatbot"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Great! For Pune in June, I recommend Rice with 87% confidence.",
                "next_step": "Would you like to know about fertilizer requirements?",
                "requires_input": None,
                "crop_recommendation": {"crop": "Rice", "confidence": 87}
            }
        }
    )
    
    message: str
    next_step: Optional[str] = None
    requires_input: Optional[List[str]] = None
    crop_recommendation: Optional[dict] = None
