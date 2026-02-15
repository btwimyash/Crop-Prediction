"""
Translation Service - Handles multilingual support (English, Hindi, Marathi)
"""

from typing import Dict
from enum import Enum


class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"


class TranslationService:
    """Service to handle translations for agricultural terms and messages"""
    
    # Translation dictionary
    TRANSLATIONS = {
        # Crops
        "Rice": {
            "hi": "चावल",
            "mr": "तांदूळ"
        },
        "Maize": {
            "hi": "मक्का",
            "mr": "मका"
        },
        "Cotton": {
            "hi": "कपास",
            "mr": "कपाळ"
        },
        "Sugarcane": {
            "hi": "गन्ना",
            "mr": "उस"
        },
        "Coffee": {
            "hi": "कॉफी",
            "mr": "कॉफी"
        },
        "Wheat": {
            "hi": "गेहूँ",
            "mr": "गहू"
        },
        "Soybean": {
            "hi": "सोयाबीन",
            "mr": "सोयाबीन"
        },
        
        # Risk Levels
        "Low Risk": {
            "hi": "कम जोखिम",
            "mr": "कमी जोखिम"
        },
        "Medium Risk": {
            "hi": "मध्यम जोखिम",
            "mr": "मध्यम जोखिम"
        },
        "High Risk": {
            "hi": "उच्च जोखिम",
            "mr": "उच्च जोखिम"
        },
        
        # Messages
        "Top Recommendations": {
            "hi": "शीर्ष सिफारिशें",
            "mr": "शीर्ष शिफारसी"
        },
        "Confidence": {
            "hi": "आत्मविश्वास",
            "mr": "आत्मविश्वास"
        },
        "Risk Level": {
            "hi": "जोखिम स्तर",
            "mr": "जोखिम स्तर"
        },
        "Weather Conditions": {
            "hi": "मौसम की स्थिति",
            "mr": "हवामान परिस्थिती"
        },
        "Temperature": {
            "hi": "तापमान",
            "mr": "तापमान"
        },
        "Humidity": {
            "hi": "आर्द्रता",
            "mr": "आर्द्रता"
        },
        "Rainfall": {
            "hi": "वर्षा",
            "mr": "पावसाळ"
        },
        
        # Advisory messages
        "is highly recommended": {
            "hi": "अत्यधिक अनुशंसित है",
            "mr": "अत्यंत शिफारस केली जाते"
        },
        "with adequate rainfall": {
            "hi": "पर्याप्त वर्षा के साथ",
            "mr": "पर्याप्त पावसाळसह"
        },
        "Ensure proper irrigation": {
            "hi": "उचित सिंचाई सुनिश्चित करें",
            "mr": "योग्य सिंचन सुनिश्चित करा"
        },
        "Monitor soil moisture": {
            "hi": "मिट्टी की नमी की निगरानी करें",
            "mr": "माती ची ओलावपणा नियंत्रणात ठेवा"
        },
    }
    
    # Advisory message templates
    ADVISORY_TEMPLATES = {
        "en": {
            "low_risk": "{crop} is highly recommended for {district} in {month} with optimal conditions. Rainfall is adequate and soil conditions are favorable.",
            "medium_risk": "{crop} is recommended for {district} in {month}. Monitor rainfall and ensure proper irrigation. Temperature and humidity are within acceptable range.",
            "high_risk": "{crop} can be grown in {district} in {month}, but requires careful management. Rainfall is limited - ensure supplementary irrigation.",
        },
        "hi": {
            "low_risk": "{crop} {district} में {month} के लिए अत्यधिक अनुशंसित है। वर्षा पर्याप्त है और मिट्टी की स्थिति अनुकूल है।",
            "medium_risk": "{crop} {district} में {month} के लिए अनुशंसित है। वर्षा की निगरानी करें और उचित सिंचाई सुनिश्चित करें।",
            "high_risk": "{crop} {district} में {month} में उगाया जा सकता है, लेकिन सावधानीपूर्वक प्रबंधन की आवश्यकता है। वर्षा सीमित है।",
        },
        "mr": {
            "low_risk": "{crop} {district} मध्ये {month} साठी अत्यंत शिफारस केली जाते. पावसाळ पर्याप्त आहे आणि मातीची स्थिती अनुकूल आहे.",
            "medium_risk": "{crop} {district} मध्ये {month} साठी शिफारस केली जाते. पावसाळवर लक्ष ठेवा आणि योग्य सिंचन सुनिश्चित करा.",
            "high_risk": "{crop} {district} मध्ये {month} मध्ये उगवले जाऊ शकते, परंतु सावधानीपूर्वक व्यवस्थापन आवश्यक आहे.",
        }
    }
    
    def translate(self, text: str, language: str) -> str:
        """
        Translate text to specified language.
        
        Args:
            text: Text to translate
            language: Target language code (en, hi, mr)
            
        Returns:
            Translated text or original if translation not found
        """
        if language == "en":
            return text
        
        if text in self.TRANSLATIONS and language in self.TRANSLATIONS[text]:
            return self.TRANSLATIONS[text][language]
        
        # Return original if translation not found
        return text
    
    def get_advisory_message(self, crop: str, district: str, month: str, 
                            risk_level: str, language: str = "en") -> str:
        """
        Generate advisory message based on conditions.
        
        Args:
            crop: Crop name
            district: District name
            month: Month
            risk_level: Risk level (Low, Medium, High)
            language: Language code
            
        Returns:
            Advisory message in specified language
        """
        template_key = f"{risk_level.lower().replace(' ', '_')}"
        template = self.ADVISORY_TEMPLATES.get(language, {}).get(
            template_key, 
            self.ADVISORY_TEMPLATES["en"][template_key]
        )
        
        return template.format(crop=crop, district=district, month=month)


def get_translation_service() -> TranslationService:
    """Factory function to create TranslationService instance"""
    return TranslationService()
