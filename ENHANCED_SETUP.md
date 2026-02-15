# 🌾 Smart Crop Advisory System - v2.0.0

A complete AI-powered crop recommendation system with React frontend, FastAPI backend, multilingual support, and AI chatbot integration.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Setup Instructions](#setup-instructions)
6. [API Documentation](#api-documentation)
7. [Frontend Documentation](#frontend-documentation)
8. [Deployment](#deployment)

---

## 🎯 Overview

This system provides intelligent crop recommendations based on:
- **Geographic Location** (State, District, Month)
- **Soil Properties** (Nitrogen, Phosphorous, Potassium, pH)
- **Weather Data** (Temperature, Humidity, Rainfall via OpenWeatherMap API)
- **Machine Learning Model** (99% accurate Deep Neural Network)

### Key Enhancements from v1.0
- ✅ Returns **TOP 3 CROPS** with confidence scores
- ✅ **Multilingual support** (English, Hindi, Marathi)
- ✅ **AI Chatbot** for conversational UX
- ✅ **Risk analysis** based on weather conditions
- ✅ **Auto-fetch missing data** from external APIs
- ✅ **Beautiful React UI** with responsive design

---

## ✨ Features

### 1. Crop Prediction
- Returns top 3 recommended crops with confidence percentages
- Validates soil data against expected ranges
- Risk level assessment (Low, Medium, High)
- Weather-aware recommendations

### 2. AI Chatbot
- Conversational interface for data collection
- Guides users through mandatory and optional fields
- Auto-fetches missing soil data
- Context-aware responses

### 3. Multilingual Support
- English
- Hindi (हिंदी)
- Marathi (मराठी)
- Agricultural terminology correctly translated

### 4. Weather Integration
- Real-time temperature & humidity via OpenWeatherMap API
- Rainfall data from Indian rainfall dataset
- Risk assessment based on weather patterns

### 5. Smart Defaults
- Auto-detection of soil values by district
- Default rainfall data lookup
- Intelligent handling of missing data

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **PyTorch** - ML model inference
- **Pandas** - Data manipulation
- **Requests** - HTTP client for APIs
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **CSS3** - Styling & animations
- **Fetch API** - HTTP requests

### ML Model
- **Architecture**: Deep Neural Network (DNN)
  - Input: 7 features
  - Hidden layers: 64 → 128 → 64 neurons
  - Output: 22 crops (Softmax)
- **Activation**: SeLU (hidden), Softmax (output)
- **Accuracy**: 99% on test data

---

## 📁 Project Structure

```
crop-prediction-main/
├── backend/
│   ├── main.py                 # Enhanced FastAPI app
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Configuration
│   ├── services/
│   │   ├── weather_service.py    # Weather API integration
│   │   ├── soil_service.py       # Soil data management
│   │   ├── crop_service.py       # ML model predictions
│   │   ├── translation_service.py # Multilingual support
│   │   └── chatbot_service.py     # Chatbot logic
│   ├── models/
│   │   ├── request_models.py     # Pydantic request schemas
│   │   └── response_models.py    # Response schemas
│   └── utils/
│       └── helpers.py           # Utility functions
│
├── frontend/
│   ├── package.json             # NPM dependencies
│   ├── .env                     # React environment config
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx              # Main component
│       ├── App.css
│       ├── components/
│       │   ├── CropForm.jsx      # Prediction form
│       │   ├── CropForm.css
│       │   ├── ResultCard.jsx    # Results display
│       │   ├── ResultCard.css
│       │   ├── Chatbot.jsx       # Chatbot UI
│       │   └── Chatbot.css
│       ├── services/
│       │   └── api.js           # API calls
│       └── index.js
│
├── data/
│   ├── district wise rainfall normal.csv
│   └── [other data files]
│
├── model/
│   ├── baseline/
│   │   └── baseline.hdf5        # Trained model
│   ├── normalization/
│   │   └── normalization.npz    # Normalization params
│   └── pkl_files/
│       └── encoder.pkl          # Label encoder
│
└── ENHANCED_SETUP.md            # This file
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip/npm package managers

### Backend Setup

#### 1. Create Virtual Environment
```bash
cd backend
python -m venv NLP
source NLP/Scripts/activate  # Windows: .\NLP\Scripts\Activate.ps1
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
Edit `.env` file:
```dotenv
OPENWEATHER_API_KEY=your_api_key_here
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
PORT=8000
```

**Get OpenWeatherMap API Key:**
1. Visit https://openweathermap.org/api
2. Sign up (free tier)
3. Create an API key in your dashboard
4. Add to `.env`

#### 4. Run Backend Server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Server running at: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

### Frontend Setup

#### 1. Install Dependencies
```bash
cd ../frontend
npm install
```

#### 2. Configure Environment
```dotenv
REACT_APP_API_URL=http://localhost:8000
```

#### 3. Start Development Server
```bash
npm start
```

✅ App running at: **http://localhost:3000**

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Predict Crop (Main Endpoint)
```http
POST /predict/
```

**Request:**
```json
{
  "state": "MAHARASHTRA",
  "district": "PUNE",
  "month": "JUN",
  "nitrogen": 90,
  "phosphorous": 40,
  "potassium": 40,
  "ph": 6.5,
  "language": "en",
  "use_auto_values": false
}
```

**Required Fields:**
- `state`: State name (UPPERCASE)
- `district`: District name (UPPERCASE)
- `month`: Month abbreviation (JAN-DEC)

**Optional Fields:**
- `nitrogen`: 0-140 (auto-fetched if null)
- `phosphorous`: 0-145 (auto-fetched if null)
- `potassium`: 0-205 (auto-fetched if null)
- `ph`: 0-14 (auto-fetched if null)

**Response:**
```json
{
  "top_predictions": [
    {
      "crop": "Rice",
      "confidence": 87.5
    },
    {
      "crop": "Maize",
      "confidence": 9.2
    },
    {
      "crop": "Cotton",
      "confidence": 3.3
    }
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

#### 2. Chatbot API
```http
POST /chatbot/
```

**Request:**
```json
{
  "message": "Which crop should I grow?",
  "session_id": "abc123",
  "language": "en"
}
```

**Response:**
```json
{
  "message": "Great! For Pune in June, I recommend Rice...",
  "next_step": "Would you like to know about fertilizer?",
  "requires_input": false,
  "crop_recommendation": {
    "crop": "Rice",
    "confidence": 87.5
  }
}
```

#### 3. Get States
```http
GET /states/
```

**Response:**
```json
{
  "states": ["MAHARASHTRA", "KARNATAKA", ...]
}
```

#### 4. Get Districts
```http
GET /districts/{state}
```

**Response:**
```json
{
  "state": "MAHARASHTRA",
  "districts": ["PUNE", "MUMBAI CITY", "NAGPUR", ...]
}
```

#### 5. Get Months
```http
GET /months/
```

**Response:**
```json
{
  "months": ["JAN", "FEB", ...]
}
```

#### 6. Health Check
```http
GET /health
```

---

## 🎨 Frontend Documentation

### Components

#### CropForm.jsx
Responsive form for crop prediction.

**Props:**
- `onPredictionSuccess`: Callback when prediction succeeds
- `onError`: Callback when error occurs
- `language`: Language code (en, hi, mr)

**Features:**
- Dropdown selection for state, district, month
- Toggle switch for soil values
- Form validation
- Responsive design

#### ResultCard.jsx
Displays crop predictions and analysis.

**Props:**
- `prediction`: Prediction data object
- `language`: Language code

**Shows:**
- Top 3 crops with confidence bars
- Risk level badge
- Weather conditions
- Soil values used
- Advisory message

#### Chatbot.jsx
Conversational interface for crop advisory.

**Props:**
- `onRecommendation`: Callback when crop recommended
- `language`: Language code

**Features:**
- Guided conversation flow
- Auto-validation of inputs
- Typing indicators
- Session management

### API Service (`api.js`)

**Functions:**
- `predictCrop()` - Submit prediction request
- `sendChatMessage()` - Send chat message
- `getStates()` - Fetch available states
- `getDistricts()` - Fetch districts for state
- `getMonths()` - Fetch months list
- `healthCheck()` - API health status

### Styling

All components use CSS3 with:
- Responsive grid layouts
- CSS animations
- CSS variables for theming
- Mobile-first design

---

## 🌐 Using the System

### Form-Based REC (Recommendation):

1. Select State → District → Month
2. Choose: "Use My Values" OR "Auto Detect"
3. (Optional) Enter soil values
4. Click "Get Recommendation"
5. View top 3 crops with confidence & risk analysis

### Chatbot-Based Recommendation:

1. Click "Chatbot Assistant" tab
2. Answer guided questions conversationally
3. Skip optional questions for auto-detection
4. Receive crop recommendation
5. Ask follow-up questions

### Multilingual Usage:

- Click language buttons (English, हिंदी, मराठी)
- All labels, responses, and messages translate
- Agricultural terminology correctly localized

---

## 🚢 Deployment

### Backend Deployment (Heroku)

```bash
# Create Procfile
echo "web: gunicorn main:app" > Procfile

# Deploy
heroku create crop-advisory-api
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)

```bash
# Build optimized production bundle
npm run build

# Deploy with Vercel
vercel --prod
```

### Docker Deployment

**Dockerfile (Backend):**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## 📊 Model Performance

- **Accuracy**: 99% (test set)
- **Training Epochs**: 100
- **Loss Function**: Categorical Crossentropy
- **Optimizer**: ADAM
- **Crops Recognized**: 22 types
- **Input Features**: 7 (N, P, K, Temp, Humidity, pH, Rainfall)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `CORS Error` | Check `origins` in `main.py` matches frontend URL |
| `API Key Error` | Verify `.env` has valid OpenWeatherMap key |
| `Weather API Fails` | Check internet connection & API rate limits |
| `Model Not Found` | Ensure model files in `model/` directory |
| `Port Already In Use` | Change port: `--port 8001` |

---

## 📚 API Examples

### cURL
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "MAHARASHTRA",
    "district": "PUNE",
    "month": "JUN",
    "language": "en",
    "use_auto_values": true
  }'
```

### Python Requests
```python
import requests

response = requests.post(
    "http://localhost:8000/predict/",
    json={
        "state": "MAHARASHTRA",
        "district": "PUNE",
        "month": "JUN",
        "language": "en",
        "use_auto_values": True
    }
)

print(response.json())
```

### JavaScript Fetch
```javascript
const response = await fetch("http://localhost:8000/predict/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    state: "MAHARASHTRA",
    district: "PUNE",
    month: "JUN",
    language: "en",
    use_auto_values: true
  })
});

const data = await response.json();
console.log(data);
```

---

## 📝 License

This project is provided for educational and commercial use.

---

## 👥 Contributors

- Your Team

---

## 📧 Support

For issues and questions:
- Email: support@cropadvice.com
- GitHub Issues: [Project Issues]
- Documentation: [Full Docs]

---

**Happy Farming! 🌾🚜**
