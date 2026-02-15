"""
Soil Service - Provides default soil values by district
"""

import pandas as pd
import os
from typing import Optional, Dict


class SoilService:
    """Service to fetch and provide default soil values"""
    
    # Default soil values for India (by district)
    # In production, this would be from a database
    DEFAULT_SOIL_VALUES = {
        "PUNE": {"nitrogen": 90, "phosphorous": 40, "potassium": 40, "ph": 6.5},
        "MUMBAI CITY": {"nitrogen": 85, "phosphorous": 35, "potassium": 38, "ph": 6.8},
        "NAGPUR": {"nitrogen": 95, "phosphorous": 45, "potassium": 42, "ph": 6.2},
        "AURANGABAD": {"nitrogen": 88, "phosphorous": 42, "potassium": 39, "ph": 6.4},
        "NASHIK": {"nitrogen": 92, "phosphorous": 43, "potassium": 41, "ph": 6.3},
        "JALGAON": {"nitrogen": 90, "phosphorous": 40, "potassium": 40, "ph": 6.5},
        # Add more districts as needed
    }
    
    def __init__(self):
        """Initialize soil service"""
        self.soil_values = self.DEFAULT_SOIL_VALUES
    
    def get_default_soil_values(self, district: str) -> Dict[str, float]:
        """
        Get default soil values for a district.
        
        Args:
            district: District name in UPPERCASE
            
        Returns:
            Dictionary with nitrogen, phosphorous, potassium, ph values
        """
        # Try exact match
        if district in self.soil_values:
            return self.soil_values[district].copy()
        
        # If not found, return general default values
        print(f"⚠ No specific soil data for {district}, using default values")
        return {
            "nitrogen": 90,
            "phosphorous": 40,
            "potassium": 40,
            "ph": 6.5
        }
    
    def get_rainfall_data(self, state: str, district: str, month: str) -> Optional[float]:
        """
        Get rainfall data for a given state, district, and month.
        
        Args:
            state: State name in UPPERCASE
            district: District name in UPPERCASE
            month: Month abbreviation (JAN, FEB, etc)
            
        Returns:
            Rainfall in mm
        """
        try:
            rainfall_file = "data/district wise rainfall normal.csv"
            
            if not os.path.exists(rainfall_file):
                print(f"⚠ Rainfall file not found at {rainfall_file}")
                return 100.0  # Default rainfall
            
            df = pd.read_csv(rainfall_file)
            row = df[(df['STATE_UT_NAME'] == state) & (df['DISTRICT'] == district)]
            
            if row.empty:
                print(f"⚠ No rainfall data for {state}, {district}")
                return 100.0  # Default rainfall
            
            rainfall = row[month].values[0]
            return float(rainfall)
            
        except Exception as e:
            print(f"⚠ Error fetching rainfall data: {str(e)}")
            return 100.0  # Default rainfall


def get_soil_service() -> SoilService:
    """Factory function to create SoilService instance"""
    return SoilService()
