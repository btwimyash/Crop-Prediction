"""
Enhanced FastAPI backend for Smart Crop Advisory System
"""

import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from backend/.env (when running from project root)
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Import services (absolute imports from project root)
from backend.services.weather_service import get_weather_service
from backend.services.soil_service import get_soil_service
from backend.services.crop_service import get_crop_service
from backend.services.translation_service import get_translation_service
from backend.services.chatbot_service import get_chatbot_service

# Import models (absolute imports from project root)
from backend.models.request_models import PredictRequest, ChatbotRequest
from backend.models.response_models import PredictResponse, CropPrediction, ChatbotResponse

# Import utilities (absolute imports from project root)
from backend.utils.helpers import (
    calculate_risk_level, validate_soil_values, validate_month,
    get_season_name, format_response
)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Crop Advisory System",
    description="AI-powered crop recommendation engine with multilingual support",
    version="2.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
weather_service = get_weather_service()
soil_service = get_soil_service()
crop_service = get_crop_service()
translation_service = get_translation_service()
chatbot_service = get_chatbot_service()


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Smart Crop Advisory System is running",
        "version": "2.0.0",
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "weather": "✓",
            "soil": "✓",
            "crop_model": "✓",
            "translation": "✓",
            "chatbot": "✓"
        }
    }


# ============================================================================
# MAIN PREDICTION ENDPOINT
# ============================================================================

@app.post("/predict/", response_model=PredictResponse, tags=["Predictions"])
async def predict_crop(request: PredictRequest):
    """
    Predict top 3 crops with confidence scores.
    
    **Mandatory fields:**
    - state: State/UT name (UPPERCASE)
    - district: District name (UPPERCASE)
    - month: Month abbreviation (JAN, FEB, etc)
    
    **Optional fields (auto-fetched if not provided):**
    - nitrogen, phosphorous, potassium, ph
    
    **Returns:**
    - Top 3 crop recommendations with confidence scores
    - Risk assessment based on weather
    - Advisory message
    """
    
    try:
        # Validate mandatory fields
        if not request.state or not request.district or not request.month:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State, district, and month are mandatory"
            )
        
        # Validate month format
        if not validate_month(request.month):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Month must be in format: JAN, FEB, MAR, ... DEC"
            )
        
        # Fetch or use provided soil values
        nitrogen = request.nitrogen
        phosphorous = request.phosphorous
        potassium = request.potassium
        ph = request.ph
        
        soil_values_used = {
            "nitrogen": nitrogen,
            "phosphorous": phosphorous,
            "potassium": potassium,
            "ph": ph
        }
        
        # If auto-detect is enabled and values are missing, fetch them
        if request.use_auto_values:
            if nitrogen is None or phosphorous is None or potassium is None or ph is None:
                print("📊 Fetching default soil values...")
                default_soil = soil_service.get_default_soil_values(request.district)
                nitrogen = nitrogen or default_soil["nitrogen"]
                phosphorous = phosphorous or default_soil["phosphorous"]
                potassium = potassium or default_soil["potassium"]
                ph = ph or default_soil["ph"]
                
                soil_values_used = {
                    "nitrogen": nitrogen,
                    "phosphorous": phosphorous,
                    "potassium": potassium,
                    "ph": ph
                }
        
        # Validate soil values
        validation = validate_soil_values(nitrogen, phosphorous, potassium, ph)
        if not validation["all_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Soil values are out of valid range"
            )
        
        # Fetch weather data
        print(f"🌤️ Fetching weather data for {request.district}...")
        temperature, humidity = weather_service.get_weather_data(
            request.district, 
            request.state
        )
        
        # Fetch rainfall data
        print(f"💧 Fetching rainfall data...")
        rainfall = soil_service.get_rainfall_data(
            request.state, 
            request.district, 
            request.month
        )
        
        # Get crop predictions
        print(f"🌾 Running crop prediction model...")
        predictions = crop_service.predict_top_crops(
            nitrogen=nitrogen,
            phosphorous=phosphorous,
            potassium=potassium,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            top_n=3
        )
        
        # Calculate risk level
        risk_level, risk_description = calculate_risk_level(rainfall, temperature, humidity)
        
        # Generate advisory message
        top_crop = predictions[0][0]
        advisory_message = translation_service.get_advisory_message(
            crop=top_crop,
            district=request.district,
            month=request.month,
            risk_level=risk_level,
            language=request.language
        )
        
        # Prepare response
        top_predictions = [
            CropPrediction(crop=crop, confidence=round(conf, 2))
            for crop, conf in predictions
        ]
        
        response = PredictResponse(
            top_predictions=top_predictions,
            risk_level=risk_level,
            rainfall=rainfall,
            temperature=temperature,
            humidity=humidity,
            advisory_message=advisory_message,
            soil_values_used=soil_values_used
        )
        
        print("✅ Prediction completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


# ============================================================================
# CHATBOT ENDPOINTS
# ============================================================================

@app.post("/chatbot/", response_model=ChatbotResponse, tags=["Chatbot"])
async def chatbot(request: ChatbotRequest):
    """
    Conversational chatbot for crop advisory.
    
    Guides users through a conversation to collect information
    and provide crop recommendations.
    """
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get chatbot response
        response_data = chatbot_service.get_response(
            user_message=request.message,
            session_id=session_id,
            language=request.language
        )
        
        # Check if ready for prediction
        if response_data.get("ready_for_prediction"):
            # Prepare prediction request from chatbot data
            user_data = response_data.get("user_data", {})
            
            # Create automatic prediction
            predict_request = PredictRequest(
                state=user_data.get("state", ""),
                district=user_data.get("district", ""),
                month=user_data.get("month", ""),
                nitrogen=user_data.get("nitrogen"),
                phosphorous=user_data.get("phosphorous"),
                potassium=user_data.get("potassium"),
                ph=user_data.get("ph"),
                language=request.language,
                use_auto_values=user_data.get("use_auto_values", True)
            )
            
            # Get prediction
            prediction = await predict_crop(predict_request)
            
            # Extract top recommendation
            top_crop = prediction.top_predictions[0]
            
            # Generate chatbot response
            messages = {
                "en": f"Based on your information, I recommend {top_crop.crop} with {top_crop.confidence}% confidence! 🌾",
                "hi": f"आपकी जानकारी के आधार पर, मैं {top_crop.crop} की सिफारिश करता हूं {top_crop.confidence}% आत्मविश्वास के साथ! 🌾",
                "mr": f"तुमच्या माहितीच्या आधारे, मी {top_crop.crop} ची शिफारस करतो {top_crop.confidence}% आत्मविश्वास सह! 🌾"
            }
            
            response = ChatbotResponse(
                message=messages.get(request.language, messages["en"]),
                next_step="Would you like to know the risk level or fertilizer requirements?",
                crop_recommendation={"crop": top_crop.crop, "confidence": top_crop.confidence}
            )
        else:
            response = ChatbotResponse(
                message=response_data.get("message", ""),
                next_step=response_data.get("next_step"),
                requires_input=response_data.get("requires_input", False)
            )
        
        return response
        
    except Exception as e:
        print(f"❌ Chatbot error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot error: {str(e)}"
        )


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/states/", tags=["Utilities"])
async def get_states():
    """Get list of all available states"""
    states = [
        "MAHARASHTRA", "KARNATAKA", "TAMIL NADU", "PUNJAB", "HARYANA",
        "UTTAR PRADESH", "MADHYA PRADESH", "RAJASTHAN", "WEST BENGAL",
        "ANDHRA PRADESH", "TELANGANA", "BIHAR", "GUJRAT", "UTTARANCHAL",
    ]
    return {"states": states}


@app.get("/months/", tags=["Utilities"])
async def get_months():
    """Get list of months"""
    months = [
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
    ]
    return {"months": months}


@app.get("/districts/{state}", tags=["Utilities"])
async def get_districts(state: str):
    """Get districts for a given state"""
    try:
        import pandas as pd
        df = pd.read_csv("data/district wise rainfall normal.csv")
        districts = df[df['STATE_UT_NAME'] == state.upper()]['DISTRICT'].unique().tolist()
        
        if not districts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"State '{state}' not found"
            )
        
        return {"state": state.upper(), "districts": districts}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching districts: {str(e)}"
        )


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
