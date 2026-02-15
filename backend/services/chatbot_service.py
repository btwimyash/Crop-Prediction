"""
Chatbot Service - Conversational interface for crop advisory
"""

from typing import Optional, Dict, List
import json


class ChatbotService:
    """Service to handle chatbot conversations"""
    
    # Define conversation states
    STATES = {
        "START": 0,
        "ASK_STATE": 1,
        "ASK_DISTRICT": 2,
        "ASK_MONTH": 3,
        # kept legacy name and alias to avoid KeyError
        "ASK_SOIL_VALUES": 4,
        "ASK_USE_SOIL": 4,
        "ASK_NITROGEN": 5,
        "ASK_PHOSPHOROUS": 6,
        "ASK_POTASSIUM": 7,
        "ASK_PH": 8,
        "PROVIDING_RECOMMENDATION": 9,
    }
    
    # All Indian states (sample)
    STATES_LIST = [
        "MAHARASHTRA", "KARNATAKA", "TAMIL NADU", "PUNJAB", "HARYANA",
        "UTTAR PRADESH", "MADHYA PRADESH", "RAJASTHAN", "WEST BENGAL",
        "ANDHRA PRADESH", "TELANGANA", "BIHAR", "GUJRAT", "UTTARANCHAL",
        "HIMACHAL", "ORISSA", "ASSAM"
    ]
    
    MONTHS_LIST = [
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
    ]
    
    RESPONSES = {
        "en": {
            "welcome": "Hello! 👋 I'm your Crop Advisory Assistant. I'll help you find the best crop to grow. Let's start! What state are you in?",
            "ask_state": "Which state are you in? (e.g., Maharashtra, Karnataka, Tamil Nadu)",
            "invalid_state": "I couldn't find that state. Please choose from: Maharashtra, Karnataka, Tamil Nadu, etc.",
            "ask_district": "Great! Now, which district in {state}?",
            "invalid_district": "I'm not sure about that district. Could you try again or check the spelling?",
            "ask_month": "Perfect! Which month are you planning to grow the crop? (e.g., JAN, FEB, MAR, etc)",
            "ask_use_soil": "Do you have your own soil test values (Nitrogen, Phosphorous, Potassium, pH)? Or should I use default values?",
            "ask_nitrogen": "What is the Nitrogen content in your soil? (0-140)",
            "ask_phosphorous": "What is the Phosphorous content? (0-145)",
            "ask_potassium": "What is the Potassium content? (0-205)",
            "ask_ph": "What is the pH value? (0-14)",
            "processing": "Processing your data...",
            "recommendation": "Based on your location and conditions, I recommend: {crop} with {confidence}% confidence! 🌾",
            "low_risk": "The risk level is low - this is a great choice for {district}!",
            "medium_risk": "The risk level is moderate - you'll need to monitor conditions.",
            "high_risk": "The risk level is high - careful management will be needed.",
            "follow_up": "Would you like to know about fertilizer requirements or irrigation tips?",
        },
        "hi": {
            "welcome": "नमस्ते! 👋 मैं आपका फसल सलाहकार हूँ। मैं आपको सही फसल उगाने में मदद करूँगा। चलिए शुरू करते हैं! आप किस राज्य में हैं?",
            "ask_state": "आप किस राज्य में हैं? (उदा: महाराष्ट्र, कर्नाटक, तमिलनाडु)",
            "ask_district": "ठीक है! अब {state} में आपका जिला कौन सा है?",
            "ask_month": "बढ़िया! आप किस महीने में फसल उगाना चाहते हैं?",
            "ask_use_soil": "क्या आपके पास अपनी मिट्टी परीक्षण मान हैं?",
            "recommendation": "आपकी स्थिति के आधार पर, मैं सुझाते हैं: {crop} - {confidence}% विश्वास! 🌾",
        },
        "mr": {
            "welcome": "नमस्कार! 👋 मी तुमचा पिक सल्लागार आहे. चला सुरुवात करूयात! तुम कोणत्या राज्यात आहात?",
            "ask_state": "तुम कोणत्या राज्यात आहात? (उदा: महाराष्ट्र, कर्नाटक)",
            "ask_district": "बरोबर! {state} मध्ये तुमचा जिल्हा कोणता?",
            "ask_month": "किस महिन्यात तुम पीक घ्यायचा?",
            "recommendation": "तुमच्या परिस्थितीनुसार, मी सुचवतो: {crop} - {confidence}% विश्वास! 🌾",
        }
    }
    
    def __init__(self):
        """Initialize chatbot service"""
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self, session_id: str, language: str = "en") -> Dict:
        """Create a new chat session"""
        self.sessions[session_id] = {
            "state": self.STATES["START"],
            "language": language,
            "data": {},
            "step": 0
        }
        return self.sessions[session_id]
    
    def get_response(self, user_message: str, session_id: str, language: str = "en") -> Dict:
        """
        Process user message and return chatbot response.
        
        Args:
            user_message: User's message
            session_id: Session ID
            language: Language preference
            
        Returns:
            Dictionary with response and next steps
        """
        if session_id not in self.sessions:
            self.create_session(session_id, language)
        
        session = self.sessions[session_id]
        messages = self.RESPONSES.get(language, self.RESPONSES["en"])
        
        # State machine logic
        state = session["state"]
        
        if state == self.STATES["START"]:
            session["state"] = self.STATES["ASK_STATE"]
            return {
                "message": messages["welcome"],
                "requires_input": True,
                "input_type": "text"
            }
        
        elif state == self.STATES["ASK_STATE"]:
            state_input = user_message.upper().strip()
            if any(s.startswith(state_input) for s in self.STATES_LIST):
                session["data"]["state"] = state_input
                session["state"] = self.STATES["ASK_DISTRICT"]
                return {
                    "message": messages["ask_district"].format(state=state_input),
                    "requires_input": True,
                    "input_type": "text"
                }
            else:
                return {
                    "message": messages["invalid_state"],
                    "requires_input": True,
                    "input_type": "text"
                }
        
        elif state == self.STATES["ASK_DISTRICT"]:
            district_input = user_message.upper().strip()
            session["data"]["district"] = district_input
            session["state"] = self.STATES["ASK_MONTH"]
            return {
                "message": messages["ask_month"],
                "requires_input": True,
                "input_type": "select",
                "options": self.MONTHS_LIST
            }
        
        elif state == self.STATES["ASK_MONTH"]:
            month_input = user_message.upper().strip()
            if any(m == month_input for m in self.MONTHS_LIST):
                session["data"]["month"] = month_input
                session["state"] = self.STATES["ASK_USE_SOIL"]
                return {
                    "message": messages["ask_use_soil"],
                    "requires_input": True,
                    "input_type": "select",
                    "options": ["Yes, I have values", "No, use defaults"]
                }
            else:
                return {
                    "message": "Please choose a valid month (JAN, FEB, etc)",
                    "requires_input": True,
                    "input_type": "select",
                    "options": self.MONTHS_LIST
                }
        
        elif state == self.STATES["ASK_USE_SOIL"]:
            if "no" in user_message.lower() or "default" in user_message.lower():
                session["data"]["use_auto_values"] = True
                session["state"] = self.STATES["PROVIDING_RECOMMENDATION"]
                return {
                    "message": messages["processing"],
                    "requires_input": False,
                    "ready_for_prediction": True
                }
            else:
                session["state"] = self.STATES["ASK_NITROGEN"]
                return {
                    "message": messages["ask_nitrogen"],
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif state == self.STATES["ASK_NITROGEN"]:
            try:
                session["data"]["nitrogen"] = float(user_message)
                session["state"] = self.STATES["ASK_PHOSPHOROUS"]
                return {
                    "message": messages["ask_phosphorous"],
                    "requires_input": True,
                    "input_type": "number"
                }
            except ValueError:
                return {
                    "message": "Please enter a valid number",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif state == self.STATES["ASK_PHOSPHOROUS"]:
            try:
                session["data"]["phosphorous"] = float(user_message)
                session["state"] = self.STATES["ASK_POTASSIUM"]
                return {
                    "message": messages["ask_potassium"],
                    "requires_input": True,
                    "input_type": "number"
                }
            except ValueError:
                return {
                    "message": "Please enter a valid number",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif state == self.STATES["ASK_POTASSIUM"]:
            try:
                session["data"]["potassium"] = float(user_message)
                session["state"] = self.STATES["ASK_PH"]
                return {
                    "message": messages["ask_ph"],
                    "requires_input": True,
                    "input_type": "number"
                }
            except ValueError:
                return {
                    "message": "Please enter a valid number",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif state == self.STATES["ASK_PH"]:
            try:
                session["data"]["ph"] = float(user_message)
                session["state"] = self.STATES["PROVIDING_RECOMMENDATION"]
                return {
                    "message": messages["processing"],
                    "requires_input": False,
                    "ready_for_prediction": True,
                    "user_data": session["data"]
                }
            except ValueError:
                return {
                    "message": "Please enter a valid pH value",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        return {
            "message": "How can I help you further?",
            "requires_input": True,
            "input_type": "text"
        }


def get_chatbot_service() -> ChatbotService:
    """Factory function to create ChatbotService instance"""
    return ChatbotService()
