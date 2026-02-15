# API Request-Response Examples

Complete examples for testing all endpoints.

## 1. Crop Prediction Endpoint

### Example 1: Full Prediction (All Fields Provided)

**Request:**
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "MAHARASHTRA",
    "district": "PUNE",
    "month": "JUN",
    "nitrogen": 90,
    "phosphorous": 40,
    "potassium": 40,
    "ph": 6.5,
    "language": "en",
    "use_auto_values": false
  }'
```

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
  "advisory_message": "Rice is highly recommended for PUNE in JUN with moderate rainfall. Monitor rainfall and ensure proper irrigation. Temperature and humidity are within acceptable range.",
  "soil_values_used": {
    "nitrogen": 90.0,
    "phosphorous": 40.0,
    "potassium": 40.0,
    "ph": 6.5
  }
}
```

### Example 2: Prediction with Auto-Detection

**Request:**
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "KARNATAKA",
    "district": "BANGALORE",
    "month": "SEP",
    "language": "en",
    "use_auto_values": true
  }'
```

**Response:**
```json
{
  "top_predictions": [
    {
      "crop": "Rice",
      "confidence": 78.2
    },
    {
      "crop": "Sugarcane",
      "confidence": 15.6
    },
    {
      "crop": "Maize",
      "confidence": 6.2
    }
  ],
  "risk_level": "Low Risk",
  "rainfall": 95.3,
  "temperature": 25.8,
  "humidity": 68.0,
  "advisory_message": "Rice is highly recommended for BANGALORE in SEP with optimal conditions. Rainfall is adequate and soil conditions are favorable.",
  "soil_values_used": {
    "nitrogen": 88.0,
    "phosphorous": 42.0,
    "potassium": 39.0,
    "ph": 6.4
  }
}
```

### Example 3: Hindi Language Response

**Request:**
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "MAHARASHTRA",
    "district": "NAGPUR",
    "month": "OCT",
    "language": "hi",
    "use_auto_values": true
  }'
```

**Response:**
```json
{
  "top_predictions": [
    {"crop": "कपास", "confidence": 85.7},
    {"crop": "मक्का", "confidence": 10.3},
    {"crop": "गेहूँ", "confidence": 4.0}
  ],
  "risk_level": "कम जोखिम",
  "rainfall": 78.4,
  "temperature": 27.5,
  "humidity": 65.0,
  "advisory_message": "कपास {NAGPUR} में {OCT} के लिए अत्यधिक अनुशंसित है। वर्षा पर्याप्त है और मिट्टी की स्थिति अनुकूल है।",
  "soil_values_used": {
    "nitrogen": 95.0,
    "phosphorous": 45.0,
    "potassium": 42.0,
    "ph": 6.2
  }
}
```

---

## 2. Chatbot Endpoints

### Chat Flow Example

**Step 1: Initial greeting**
```
Request:
POST /chatbot/
{
  "message": "hello",
  "language": "en"
}

Response:
{
  "message": "Hello! 👋 I'm your Crop Advisory Assistant. I'll help you find the best crop to grow. Let's start! What state are you in?",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}
```

**Step 2: User provides state**
```
Request:
POST /chatbot/
{
  "message": "Maharashtra",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "Great! Now, which district in MAHARASHTRA?",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}
```

**Step 3: User provides district**
```
Request:
POST /chatbot/
{
  "message": "Pune",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "Perfect! Which month are you planning to grow the crop? (e.g., JAN, FEB, MAR, etc)",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}
```

**Step 4: User provides month**
```
Request:
POST /chatbot/
{
  "message": "JUN",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "Do you have your own soil test values (Nitrogen, Phosphorous, Potassium, pH)? Or should I use default values?",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}
```

**Step 5a: Skip soil values (auto-detect)**
```
Request:
POST /chatbot/
{
  "message": "No, use defaults",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "Based on your information, I recommend Rice with 87.5% confidence! 🌾",
  "requires_input": false,
  "next_step": "Would you like to know the risk level or fertilizer requirements?",
  "crop_recommendation": {
    "crop": "Rice",
    "confidence": 87.5
  }
}
```

**Step 5b: Provide soil values**
```
Request:
POST /chatbot/
{
  "message": "Yes, I have values",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "What is the Nitrogen content in your soil? (0-140)",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}

[User provides: 85]

Next Request:
POST /chatbot/
{
  "message": "85",
  "session_id": "abc123",
  "language": "en"
}

Response:
{
  "message": "What is the Phosphorous content? (0-145)",
  "requires_input": true,
  "next_step": null,
  "crop_recommendation": null
}

[Continue for Potassium and pH...]
```

---

## 3. Utility Endpoints

### Get States

**Request:**
```bash
curl "http://localhost:8000/states/"
```

**Response:**
```json
{
  "states": [
    "MAHARASHTRA",
    "KARNATAKA",
    "TAMIL NADU",
    "PUNJAB",
    "HARYANA",
    "UTTAR PRADESH",
    "MADHYA PRADESH",
    "RAJASTHAN",
    "WEST BENGAL",
    "ANDHRA PRADESH",
    "TELANGANA",
    "BIHAR",
    "GUJRAT",
    "UTTARANCHAL",
    "HIMACHAL",
    "ORISSA",
    "ASSAM"
  ]
}
```

### Get Districts for a State

**Request:**
```bash
curl "http://localhost:8000/districts/MAHARASHTRA"
```

**Response:**
```json
{
  "state": "MAHARASHTRA",
  "districts": [
    "MUMBAI CITY",
    "RAIGAD",
    "RATNAGIRI",
    "THANE",
    "SINDHUDURG",
    "MUMBAI SUB",
    "AHMEDNAGAR",
    "DHULE",
    "JALGAON",
    "KOLHAPUR",
    "NASHIK",
    "PUNE",
    "SANGLI",
    "SATARA",
    "SOLAPUR",
    "NANDURBAR",
    "AURANGABAD",
    "BEED",
    "NANDED",
    "OSMANABAD",
    "PARBHANI",
    "LATUR",
    "JALNA",
    "HINGOLI",
    "AKOLA",
    "AMRAVATI",
    "BHANDARA",
    "BULDHANA",
    "CHANDRAPUR",
    "NAGPUR",
    "YAVATMAL",
    "WARDHA",
    "GADCHIROLI",
    "WASHIM",
    "GONDIA"
  ]
}
```

### Get Months

**Request:**
```bash
curl "http://localhost:8000/months/"
```

**Response:**
```json
{
  "months": [
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC"
  ]
}
```

### Health Check

**Request:**
```bash
curl "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "weather": "✓",
    "soil": "✓",
    "crop_model": "✓",
    "translation": "✓",
    "chatbot": "✓"
  }
}
```

---

## 4. Python Integration Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Example 1: Simple Prediction
def get_crop_recommendation():
    """Get crop recommendation with auto-detection"""
    payload = {
        "state": "MAHARASHTRA",
        "district": "PUNE",
        "month": "JUN",
        "language": "en",
        "use_auto_values": True
    }
    
    response = requests.post(f"{BASE_URL}/predict/", json=payload)
    result = response.json()
    
    print(f"Recommended Crop: {result['top_predictions'][0]['crop']}")
    print(f"Confidence: {result['top_predictions'][0]['confidence']:.1f}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Advisory: {result['advisory_message']}")
    
    return result

# Example 2: Custom Soil Values
def predict_with_custom_soil():
    """Prediction with custom soil values"""
    payload = {
        "state": "KARNATAKA",
        "district": "BANGALORE",
        "month": "SEP",
        "nitrogen": 95,
        "phosphorous": 45,
        "potassium": 50,
        "ph": 6.8,
        "language": "en",
        "use_auto_values": False
    }
    
    response = requests.post(f"{BASE_URL}/predict/", json=payload)
    return response.json()

# Example 3: Chatbot Conversation
def chatbot_conversation():
    """Simulated chatbot conversation"""
    session_id = "user_12345"
    
    # Initial message
    messages = [
        "hello",
        "Maharashtra",
        "Nagpur",
        "JUN",
        "No"  # Use auto defaults
    ]
    
    for msg in messages:
        payload = {
            "message": msg,
            "session_id": session_id,
            "language": "en"
        }
        
        response = requests.post(f"{BASE_URL}/chatbot/", json=payload)
        data = response.json()
        
        print(f"Bot: {data['message']}")
        
        if data.get('crop_recommendation'):
            print(f"✓ Recommendation: {data['crop_recommendation']['crop']}")
            break

# Run examples
if __name__ == "__main__":
    print("=== Example 1: Simple Prediction ===")
    get_crop_recommendation()
    
    print("\n=== Example 2: Custom Soil Values ===")
    print(predict_with_custom_soil())
    
    print("\n=== Example 3: Chatbot ===")
    chatbot_conversation()
```

---

## 5. JavaScript Integration Example

```javascript
// Using Fetch API

// Example 1: Predict with Auto-Detection
async function predictCrop() {
  const payload = {
    state: "MAHARASHTRA",
    district: "PUNE",
    month: "JUN",
    language: "en",
    use_auto_values: true
  };
  
  const response = await fetch("http://localhost:8000/predict/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  
  const data = await response.json();
  console.log("Top Crop:", data.top_predictions[0].crop);
  console.log("Confidence:", data.top_predictions[0].confidence);
  console.log("Risk:", data.risk_level);
}

// Example 2: Chatbot Message
async function sendChatMessage(message, sessionId) {
  const response = await fetch("http://localhost:8000/chatbot/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      language: "en"
    })
  });
  
  const data = await response.json();
  return data;
}

// Example 3: Get Available Districts
async function getDistricts(state) {
  const response = await fetch(`http://localhost:8000/districts/${state}`);
  const data = await response.json();
  return data.districts;
}

// Usage
predictCrop().then(console.log);
```

---

## Error Handling Examples

### Invalid State
```
Request:
POST /predict/
{
  "state": "INVALID",
  "district": "PUNE",
  "month": "JUN"
}

Response (400):
{
  "detail": "State, district, and month are mandatory"
}
```

### Invalid Soil Values
```
Request:
POST /predict/
{
  "state": "MAHARASHTRA",
  "district": "PUNE",
  "month": "JUN",
  "nitrogen": 500,
  "use_auto_values": false
}

Response (400):
{
  "detail": "Soil values are out of valid range"
}
```

### API Connection Error
```
Request:
(Weather API unreachable)

Response (500):
{
  "detail": "Prediction failed: Weather API connection error"
}
```

---

## Performance Tips

1. **Batch Requests**: Use sessions for multiple predictions
2. **Caching**: Cache state/district lists on frontend
3. **Async**: Use async/await for better performance
4. **Compression**: Enable gzip compression on backend
5. **CDN**: Serve static assets from CDN

---

End of API Examples
