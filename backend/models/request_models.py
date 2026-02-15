from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PredictRequest(BaseModel):
    """Request model for crop prediction"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "state": "MAHARASHTRA",
                "district": "PUNE",
                "month": "JUN",
                "nitrogen": 90,
                "phosphorous": 40,
                "potassium": 40,
                "ph": 6.5,
                "language": "en",
                "use_auto_values": False
            }
        }
    )
    
    state: str = Field(..., description="State/UT name in UPPERCASE")
    district: str = Field(..., description="District name in UPPERCASE")
    month: str = Field(..., description="Month abbreviation (JAN, FEB, etc)")
    
    nitrogen: Optional[float] = Field(None, description="Nitrogen content (0-140)")
    phosphorous: Optional[float] = Field(None, description="Phosphorous content (0-145)")
    potassium: Optional[float] = Field(None, description="Potassium content (0-205)")
    ph: Optional[float] = Field(None, description="pH value (0-14)")
    
    language: str = Field("en", description="Language: en, hi, mr")
    use_auto_values: bool = Field(True, description="Auto-fetch missing soil values")


class ChatbotRequest(BaseModel):
    """Request model for chatbot"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Which crop should I grow in Pune?",
                "language": "en"
            }
        }
    )
    
    message: str = Field(..., description="User message")
    language: str = Field("en", description="Language: en, hi, mr")
    session_id: Optional[str] = Field(None, description="Session ID for context")
