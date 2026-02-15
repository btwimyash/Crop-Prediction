"""
Utility functions for the crop advisory system
"""

from typing import Dict, Tuple


def calculate_risk_level(rainfall: float, temperature: float, humidity: float) -> Tuple[str, str]:
    """
    Calculate risk level based on weather conditions.
    
    Args:
        rainfall: Rainfall in mm
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        
    Returns:
        Tuple of (risk_level, description)
    """
    
    # Risk thresholds
    LOW_RAINFALL_THRESHOLD = 50  # mm
    HIGH_RAINFALL_THRESHOLD = 200  # mm
    
    MIN_TEMP = 15  # Celsius
    MAX_TEMP = 35  # Celsius
    
    OPTIMAL_HUMIDITY = 60  # percentage
    
    risk_score = 0
    factors = []
    
    # Assess rainfall
    if rainfall < LOW_RAINFALL_THRESHOLD:
        risk_score += 3
        factors.append(f"Low rainfall ({rainfall}mm)")
    elif rainfall > HIGH_RAINFALL_THRESHOLD:
        risk_score += 1
        factors.append(f"High rainfall ({rainfall}mm)")
    else:
        factors.append(f"Moderate rainfall ({rainfall}mm)")
    
    # Assess temperature
    if temperature < MIN_TEMP or temperature > MAX_TEMP:
        risk_score += 2
        factors.append(f"Temperature out of range ({temperature}°C)")
    else:
        factors.append(f"Optimal temperature ({temperature}°C)")
    
    # Assess humidity
    if humidity < 40 or humidity > 80:
        risk_score += 1
        factors.append(f"Humidity out of range ({humidity}%)")
    else:
        factors.append(f"Adequate humidity ({humidity}%)")
    
    # Determine risk level
    if risk_score >= 5:
        risk_level = "High Risk"
    elif risk_score >= 3:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    description = ", ".join(factors)
    
    return risk_level, description


def validate_soil_values(nitrogen: float, phosphorous: float, 
                        potassium: float, ph: float) -> Dict[str, bool]:
    """
    Validate soil values against expected ranges.
    
    Args:
        nitrogen: Nitrogen content
        phosphorous: Phosphorous content
        potassium: Potassium content
        ph: pH value
        
    Returns:
        Dictionary with validation  results
    """
    
    validation = {
        "nitrogen_valid": 0 <= nitrogen <= 140,
        "phosphorous_valid": 0 <= phosphorous <= 145,
        "potassium_valid": 0 <= potassium <= 205,
        "ph_valid": 0 <= ph <= 14,
        "all_valid": True
    }
    
    validation["all_valid"] = all([
        validation["nitrogen_valid"],
        validation["phosphorous_valid"],
        validation["potassium_valid"],
        validation["ph_valid"]
    ])
    
    return validation


def format_response(crop_name: str, confidence: float, risk_level: str, 
                   language: str = "en") -> str:
    """
    Format crop recommendation response.
    
    Args:
        crop_name: Name of recommended crop
        confidence: Confidence percentage
        risk_level: Risk level
        language: Language code
        
    Returns:
        Formatted response string
    """
    
    templates = {
        "en": "{crop} is recommended with {confidence}% confidence. Risk Level: {risk}",
        "hi": "{crop} की सिफारिश की जाती है {confidence}% आत्मविश्वास के साथ। जोखिम स्तर: {risk}",
        "mr": "{crop} ची शिफारस {confidence}% आत्मविश्वास सह केली जाते. जोखिम स्तर: {risk}"
    }
    
    template = templates.get(language, templates["en"])
    return template.format(crop=crop_name, confidence=f"{confidence:.1f}", risk=risk_level)


def validate_month(month: str) -> bool:
    """Validate month format"""
    valid_months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", 
                   "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month.upper() in valid_months


def get_month_number(month: str) -> int:
    """Convert month code to number"""
    months = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
        "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
        "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
    }
    return months.get(month.upper(), 1)


def get_season_name(month: str, language: str = "en") -> str:
    """Get season name from month"""
    season_map = {
        "JAN": {"en": "Winter", "hi": "सर्दी", "mr": "हिवाळ"},
        "FEB": {"en": "Winter", "hi": "सर्दी", "mr": "हिवाळ"},
        "MAR": {"en": "Spring", "hi": "वसंत", "mr": "वसंत"},
        "APR": {"en": "Summer", "hi": "गर्मी", "mr": "उन्हाळा"},
        "MAY": {"en": "Summer", "hi": "गर्मी", "mr": "उन्हाळा"},
        "JUN": {"en": "Monsoon", "hi": "मानसून", "mr": "मान्सून"},
        "JUL": {"en": "Monsoon", "hi": "मानसून", "mr": "मान्सून"},
        "AUG": {"en": "Monsoon", "hi": "मानसून", "mr": "मान्सून"},
        "SEP": {"en": "Post-Monsoon", "hi": "पोस्ट-मानसून", "mr": "पोस्ट-मान्सून"},
        "OCT": {"en": "Post-Monsoon", "hi": "पोस्ट-मानसून", "mr": "पोस्ट-मान्सून"},
        "NOV": {"en": "Autumn", "hi": "शरद", "mr": "शरद"},
        "DEC": {"en": "Winter", "hi": "सर्दी", "mr": "हिवाळ"},
    }
    return season_map.get(month.upper(), {}).get(language, "Unknown")
