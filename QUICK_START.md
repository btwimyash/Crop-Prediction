# 🚀 Quick Start Guide

Get up and running with the Smart Crop Advisory System in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 14+
- OpenWeatherMap API Key (free)

## Quick Setup

### 1. Backend (Terminal 1)

```bash
cd backend

# Create & activate virtual environment
python -m venv NLP
source NLP/Scripts/activate  # On Windows: .\NLP\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env and add your OpenWeatherMap key
# OPENWEATHER_API_KEY=your_key_here

# Start server
python -m uvicorn main:app --reload --port 8000
```

✅ Backend ready at: `http://localhost:8000`

### 2. Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

✅ Frontend ready at: `http://localhost:3000`

## Test the System

### Via Web UI
1. Open http://localhost:3000
2. Fill form or use chatbot
3. Get crop recommendations!

### Via API (curl)
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "MAHARASHTRA",
    "district": "PUNE", 
    "month": "JUN",
    "use_auto_values": true
  }'
```

## 🔑 Get OpenWeatherMap API Key

1. Visit: https://openweathermap.org/api
2. Sign up (free)
3. Go to API keys section
4. Copy your key
5. Add to `backend/.env`:
   ```
   OPENWEATHER_API_KEY=your_key_here
   ```

## Supported States

Maharashtra, Karnataka, Tamil Nadu, Punjab, Haryana, Uttar Pradesh, Madhya Pradesh, Rajasthan, West Bengal, Andhra Pradesh, Telangana, Bihar, Gujrat, Uttaranchal, Himachal, Orissa, Assam, and more.

## Features

✨ **Top 3 Crops** with confidence scores
🌍 **Multilingual** (English, Hindi, Marathi)
🤖 **AI Chatbot** for guided recommendations
🎯 **99% Accuracy** crop predictions
🌤️ **Weather Integration** with real-time data
🔄 **Auto-Detection** of missing soil values

## Need Help?

- Read full docs: `ENHANCED_SETUP.md`
- Check API docs: http://localhost:8000/docs
- Report issues in repository

## Key Files

Backend:
- `backend/main.py` - FastAPI app
- `backend/services/` - Business logic
- `backend/.env` - Configuration

Frontend:
- `frontend/src/App.jsx` - Main component
- `frontend/src/components/` - UI components
- `frontend/.env` - React config

---

**Ready to grow smarter crops? 🌾**
