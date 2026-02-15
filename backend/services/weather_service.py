"""
Weather Service - Fetches temperature, humidity from OpenWeatherMap API
"""

import os
import requests
from typing import Tuple, Optional


class WeatherService:
    """Service to fetch weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in .env file")
    
    def get_weather_data(self, district: str, state: Optional[str] = None) -> Tuple[float, float]:
        """
        Fetch temperature and humidity for a given district.
        
        Args:
            district: District name
            state: State name (optional)
            
        Returns:
            Tuple of (temperature in Celsius, humidity in percentage)
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Construct query
            query = f"{district}, {state}" if state else district
            
            params = {
                "q": query,
                "appid": self.api_key,
                "units": "metric"  # Get temperature in Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code != 200:
                raise Exception(
                    f"Weather API error for {district}: {response.json().get('message', 'Unknown error')}"
                )
            
            data = response.json()
            
            # Extract temperature and humidity
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            
            print(f"✓ Weather data fetched for {district}")
            return temperature, humidity
            
        except requests.RequestException as e:
            raise Exception(f"Weather API connection error: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid response format from Weather API: {str(e)}")


def get_weather_service() -> WeatherService:
    """Factory function to create WeatherService instance"""
    return WeatherService()
