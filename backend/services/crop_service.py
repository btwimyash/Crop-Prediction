"""
Crop Service - Handles crop predictions with top 3 recommendations
"""

import torch
import numpy as np
import pickle
from typing import List, Tuple, Dict
import os


class CropService:
    """Service to predict crops using the trained ML model"""
    
    def __init__(self):
        """Initialize the crop prediction model"""
        self.model = None
        self.encoder = None
        self.normalization = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained PyTorch model and encoder"""
        try:
            # Import the model architecture (model/ is at project root)
            from model.net import Net_64_128_64
            
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Load model
            self.model = Net_64_128_64(7, 22)
            model_path = os.path.join(project_root, "model/baseline/baseline.hdf5")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()  # Set to evaluation mode
            
            # Load normalization parameters
            norm_path = os.path.join(project_root, "model/normalization/normalization.npz")
            if os.path.exists(norm_path):
                self.normalization = np.load(norm_path)
            
            # Load label encoder
            encoder_path = os.path.join(project_root, "model/pkl_files/encoder.pkl")
            if os.path.exists(encoder_path):
                with open(encoder_path, "rb") as f:
                    self.encoder = pickle.load(f)
            
            print("✓ ML Model loaded successfully")
            
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    
    def predict_top_crops(self, 
                         nitrogen: float,
                         phosphorous: float,
                         potassium: float,
                         temperature: float,
                         humidity: float,
                         ph: float,
                         rainfall: float,
                         top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Predict top N crops with confidence scores.
        
        Args:
            nitrogen: Nitrogen content
            phosphorous: Phosphorous content
            potassium: Potassium content
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            ph: pH value
            rainfall: Rainfall in mm
            top_n: Number of top predictions to return
            
        Returns:
            List of tuples (crop_name, confidence_percentage)
        """
        try:
            # Prepare input vector
            input_vector = np.array([
                nitrogen, phosphorous, potassium, 
                temperature, humidity, ph, rainfall
            ], dtype=np.float32)
            
            # Normalize input
            if self.normalization is not None:
                mean = self.normalization["mean"]
                std = self.normalization["std"]
                input_vector = (input_vector - mean) / std
            
            # Convert to tensor
            input_tensor = torch.tensor(input_vector, dtype=torch.float32)
            
            # Get predictions
            with torch.no_grad():
                output = self.model(input_tensor)
                # Apply softmax to get probabilities
                probabilities = torch.softmax(output, dim=0)
                probabilities = probabilities.numpy()
            
            # Get top N predictions
            top_indices = np.argsort(probabilities)[-top_n:][::-1]
            
            # Decode crop names and get confidence scores
            predictions = []
            for idx in top_indices:
                if self.encoder is not None:
                    crop_name = self.encoder.inverse_transform(np.array([idx]))[0]
                else:
                    crop_name = f"Crop_{idx}"
                
                confidence = float(probabilities[idx] * 100)
                predictions.append((crop_name, confidence))
            
            print(f"✓ Predictions generated: {[p[0] for p in predictions]}")
            return predictions
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")


def get_crop_service() -> CropService:
    """Factory function to create CropService instance"""
    return CropService()
