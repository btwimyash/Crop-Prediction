# System Architecture & Flow Documentation

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + CSS3)                      │
│  ┌──────────────┐    ┌────────────────┐    ┌──────────────┐   │
│  │  CropForm    │    │  ResultCard    │    │   Chatbot    │   │
│  │  Component   │    │  Component     │    │  Component   │   │
│  └──────┬───────┘    └────────┬───────┘    └──────┬───────┘   │
│         │                     │                    │           │
│         └─────────────────────┴────────────────────┘           │
│                        ↓                                        │
│                   API Service (api.js)                        │
│              (HTTP Requests to Backend)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓ HTTP
                    ┌──────────────┐
                    │  Port 3000   │
          ┌─────────┴──────────────┴─────────┐
          │                                  │
          ↓                                  ↓
    ┌──────────────────────────────────────────────────────────┐
    │            BACKEND (FastAPI + Python)                    │
    │                                                          │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │          Main FastAPI Application (main.py)      │    │
    │  │  Routes: /predict, /chatbot, /states, etc       │    │
    │  └──────┬──────────────────────────────────────────┘    │
    │         │                                                │
    │  ┌──────▼──────────────────────────────────────────┐    │
    │  │           Service Layer (services/)              │    │
    │  │                                                  │    │
    │  │  ┌──────────────────────────────────────────┐   │    │
    │  │  │  weather_service.py                      │   │    │
    │  │  │  - Fetches temp/humidity from API        │   │    │
    │  │  │  - Uses OpenWeatherMap API               │   │    │
    │  │  └──────────────────────────────────────────┘   │    │
    │  │                                                  │    │
    │  │  ┌──────────────────────────────────────────┐   │    │
    │  │  │  soil_service.py                         │   │    │
    │  │  │  - Provides default soil values          │   │    │
    │  │  │  - Fetches rainfall data (CSV)           │   │    │
    │  │  │  - District-wise soil mapping            │   │    │
    │  │  └──────────────────────────────────────────┘   │    │
    │  │                                                  │    │
    │  │  ┌──────────────────────────────────────────┐   │    │
    │  │  │  crop_service.py                         │   │    │
    │  │  │  - Loads trained DNN model (PyTorch)     │   │    │
    │  │  │  - Returns top 3 crops                   │   │    │
    │  │  │  - Calculates confidence scores          │   │    │
    │  │  └──────────────────────────────────────────┘   │    │
    │  │                                                  │    │
    │  │  ┌──────────────────────────────────────────┐   │    │
    │  │  │  translation_service.py                  │   │    │
    │  │  │  - Translates responses                  │   │    │
    │  │  │  - Supports: EN, HI, MR                  │   │    │
    │  │  └──────────────────────────────────────────┘   │    │
    │  │                                                  │    │
    │  │  ┌──────────────────────────────────────────┐   │    │
    │  │  │  chatbot_service.py                      │   │    │
    │  │  │  - Conversational state machine          │   │    │
    │  │  │  - Guides data collection                │   │    │
    │  │  │  - Session management                    │   │    │
    │  │  └──────────────────────────────────────────┘   │    │
    │  └──────────────────────────────────────────────────┘    │
    │         │                                                │
    │  ┌──────▼──────────────────────────────────────────┐    │
    │  │      Data & ML Model Layer                      │    │
    │  │                                                  │    │
    │  │  data/                                          │    │
    │  │  ├── district wise rainfall normal.csv          │    │
    │  │  └── other datasets                             │    │
    │  │                                                  │    │
    │  │  model/                                         │    │
    │  │  ├── baseline/baseline.hdf5 (DNN Model)        │    │
    │  │  ├── normalization/normalization.npz            │    │
    │  │  └── pkl_files/encoder.pkl (Label Encoder)     │    │
    │  └──────────────────────────────────────────────────┘    │
    │                                                          │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │        External API Integrations                │    │
    │  │  - OpenWeatherMap API (weather data)           │    │
    │  └─────────────────────────────────────────────────┘    │
    └──────────────────────────┬───────────────────────────────┘
                           │
                           ↓
              ┌────────────────────────┐
              │  Port 8000             │
              │  FastAPI Server        │
              └────────────────────────┘
```

---

## 🔄 Request-Response Flow

### Prediction Flow (Form-based)

```
1. User fills form
   ↓
2. Frontend validates input
   ↓
3. POST /predict/ request sent
   ├─ state: "MAHARASHTRA"
   ├─ district: "PUNE"
   ├─ month: "JUN"
   ├─ nitrogen: [optional]
   └─ language: "en"
   ↓
4. Backend receives request
   ↓
5. Validate mandatory fields
   ├─ State
   ├─ District
   └─ Month
   ↓
6. Fetch missing data (if use_auto_values=true)
   ├─ weather_service.get_weather_data()
   │  └─ Query OpenWeatherMap API
   ├─ soil_service.get_default_soil_values()
   │  └─ Lookup district-wise defaults
   └─ soil_service.get_rainfall_data()
      └─ Query CSV data
   ↓
7. Load ML Model
   ├─ Load DNN from model/baseline/baseline.hdf5
   ├─ Load normalization params
   └─ Load label encoder
   ↓
8. Prepare input vector
   ├─ Combine all 7 features
   └─ Normalize using saved statistics
   ↓
9. Run inference
   ├─ Forward pass through DNN
   ├─ Apply softmax activation
   └─ Get probability distribution
   ↓
10. Extract top 3 predictions
    ├─ Get top 3 indices
    ├─ Decode crop names using encoder
    └─ Convert to percentages
    ↓
11. Calculate risk level
    ├─ Assess rainfall (high/low)
    ├─ Check temperature range
    └─ Evaluate humidity
    ↓
12. Generate advisory message
    ├─ Translate to user's language
    └─ Create context-aware message
    ↓
13. Prepare response object
    ├─ top_predictions (array of 3 crops)
    ├─ risk_level (Low/Medium/High)
    ├─ weather data (temp, humidity, rainfall)
    ├─ soil values used
    └─ advisory message
    ↓
14. Return JSON response
    ↓
15. Frontend displays results
```

### Chatbot Flow

```
1. User clicks "Chatbot Tab"
   ↓
2. Chatbot initializes
   ├─ Generate session ID
   └─ Load initial greeting
   ↓
3. User sends message
   ↓
4. POST /chatbot/ request
   ├─ message: user text
   ├─ session_id: unique identifier
   └─ language: preference
   ↓
5. Chatbot state machine processes
   ├─ START
   │  └─ Ask for state
   ├─ ASK_STATE
   │  ├─ Validate user state
   │  └─ Ask for district
   ├─ ASK_DISTRICT
   │  ├─ Save district
   │  └─ Ask for month
   ├─ ASK_MONTH
   │  ├─ Validate month
   │  └─ Ask about soil values
   ├─ ASK_USE_SOIL (branch)
   │  ├─ Yes → Ask nitrogen, P, K, pH
   │  └─ No → Set use_auto_values=true
   └─ PROVIDING_RECOMMENDATION
      ├─ Trigger prediction
      └─ Return recommendation
      ↓
6. Chatbot response sent
   ├─ message: response text
   ├─ requires_input: boolean
   └─ next_step: indication
   ↓
7. Frontend displays message
   ↓
8. User continues conversation
```

---

## 📊 Data Flow Diagram

```
┌──────────────────┐
│   User Input     │
└────────┬─────────┘
         │
         ↓
    ┌────────────┐
    │ Validation │
    └────────┬───┘
             │
    ┌────────▼────────────┐
    │ Fetch Missing Data  │
    │ ┌────────────────┐  │
    │ │ Weather API    │  │
    │ │ Soil Defaults  │  │
    │ │ Rainfall CSV   │  │
    │ └────────────────┘  │
    └────────┬────────────┘
             │
    ┌────────▼──────┐
    │ Feature Set   │
    │ [7 features]  │
    └────────┬──────┘
             │
    ┌────────▼─────────────┐
    │ Normalization        │
    │ (Standardization)    │
    └────────┬─────────────┘
             │
    ┌────────▼──────────┐
    │ ML Model Inference│
    │ (PyTorch DNN)     │
    └────────┬──────────┘
             │
    ┌────────▼──────────┐
    │ Top 3 Crops +     │
    │ Probabilities     │
    └────────┬──────────┘
             │
    ┌────────▼──────────┐
    │ Risk Assessment   │
    └────────┬──────────┘
             │
    ┌────────▼──────────┐
    │ Translation       │
    └────────┬──────────┘
             │
    ┌────────▼──────────┐
    │ Response JSON     │
    └────────┬──────────┘
             │
    ┌────────▼────────┐
    │ Frontend Display │
    └──────────────────┘
```

---

## 🎛️ Configuration & Settings

### Backend `.env` Configuration
```dotenv
# API Keys
OPENWEATHER_API_KEY=your_key_here

# URLs
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
PORT=8000
```

### Frontend `.env` Configuration
```dotenv
REACT_APP_API_URL=http://localhost:8000
```

---

## 🔐 Security Considerations

1. **API Keys**
   - Never commit .env files
   - Use environment variables
   - Rotate keys regularly

2. **CORS Configuration**
   - Whitelist only trusted origins
   - In production, use specific domains

3. **Input Validation**
   - Pydantic models validate all inputs
   - Frontend validation before sending
   - Range checks for numeric values

4. **Error Handling**
   - Graceful error messages
   - No sensitive info in errors
   - Logging for debugging

---

## 📈 Scalability Considerations

### Current Architecture
- Single backend server
- Synchronous ML inference
- In-memory model loading

### For Production Scaling

1. **Load Balancing**
   - Use multiple backend instances
   - Load balancer (nginx, HAProxy)

2. **Model Optimization**
   - ONNX model format for faster inference
   - GPU acceleration (CUDA)
   - Model quantization

3. **Caching**
   - Redis for session data
   - CDN for frontend static files

4. **Database**
   - Store predictions/user data in PostgreSQL
   - User session management

5. **Monitoring**
   - ELK stack for logging
   - Prometheus for metrics
   - Sentry for error tracking

---

## 🧪 Testing Flows

### Test Case 1: Complete Prediction
Input → Validation → Data Fetch → Model → Response
Expected: Top 3 crops with confidence > 0

### Test Case 2: Missing Soil Data
Input (without soil) → Auto-fetch → Normalization → Prediction
Expected: Default values used, valid prediction

### Test Case 3: Invalid State
Input (state=INVALID) → Validation fails
Expected: Error 400 with clear message

### Test Case 4: Chatbot Flow
Message → State machine → Transition → Response
Expected: Guided conversation leading to prediction

---

## 📝 API Response Examples

### Success Response
```json
{
  "top_predictions": [
    {"crop": "Rice", "confidence": 87.5},
    {"crop": "Maize", "confidence": 9.2},
    {"crop": "Cotton", "confidence": 3.3}
  ],
  "risk_level": "Medium Risk",
  "rainfall": 156.5,
  "temperature": 28.3,
  "humidity": 72.0,
  "advisory_message": "Rice is highly recommended...",
  "soil_values_used": {
    "nitrogen": 90,
    "phosphorous": 40,
    "potassium": 40,
    "ph": 6.5
  }
}
```

### Error Response
```json
{
  "detail": "State, district, and month are mandatory"
}
```

---

## 🔄 CI/CD Pipeline Suggestion

```
Code Push
  ↓
Tests (Unit + Integration)
  ↓
Linting & Code Quality
  ↓
Build Docker Images
  ↓
Deploy to Staging
  ↓
Smoke Tests
  ↓
Deploy to Production
```

---

End of Architecture Documentation
