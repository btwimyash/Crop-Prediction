/**
 * ResultCard Component - Display prediction results
 */

import React from "react";
import "./ResultCard.css";

const ResultCard = ({ prediction, language = "en" }) => {
  if (!prediction) return null;

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case "Low Risk":
        return "low-risk";
      case "Medium Risk":
        return "medium-risk";
      case "High Risk":
        return "high-risk";
      default:
        return "medium-risk";
    }
  };

  const labels = {
    en: {
      topRecommendations: "Top Recommendations",
      riskLevel: "Risk Level",
      weatherConditions: "Weather Conditions",
      soilValues: "Soil Values Used",
      advisory: "Advisory Message",
      confidence: "Confidence",
      temperature: "Temperature",
      humidity: "Humidity",
      rainfall: "Rainfall",
    },
    hi: {
      topRecommendations: "शीर्ष सिफारिशें",
      riskLevel: "जोखिम स्तर",
      weatherConditions: "मौसम की स्थिति",
      soilValues: "उपयोग की गई मिट्टी मान",
      advisory: "सलाह संदेश",
      confidence: "आत्मविश्वास",
      temperature: "तापमान",
      humidity: "आर्द्रता",
      rainfall: "वर्षा",
    },
    mr: {
      topRecommendations: "शीर्ष शिफारसी",
      riskLevel: "जोखिम स्तर",
      weatherConditions: "हवामान परिस्थिती",
      soilValues: "वापरल्या जाणारे माती मूल्य",
      advisory: "सल्ला संदेश",
      confidence: "आत्मविश्वास",
      temperature: "तापमान",
      humidity: "आर्द्रता",
      rainfall: "पावसाळ",
    },
  };

  const t = labels[language] || labels.en;

  return (
    <div className="result-card">
      {/* Top Recommendations */}
      <div className="result-section">
        <h2 className="section-title">{t.topRecommendations}</h2>
        <div className="recommendations-grid">
          {prediction.top_predictions.map((item, index) => (
            <div key={index} className="recommendation-item">
              <div className="rank-badge">{index + 1}</div>
              <div className="crop-name">{item.crop}</div>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{ width: `${item.confidence}%` }}
                ></div>
              </div>
              <div className="confidence-text">
                {t.confidence}: {item.confidence.toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Level */}
      <div className="result-section">
        <h3 className="section-title">{t.riskLevel}</h3>
        <div className={`risk-badge ${getRiskColor(prediction.risk_level)}`}>
          {prediction.risk_level}
        </div>
      </div>

      {/* Weather Conditions */}
      <div className="result-section">
        <h3 className="section-title">{t.weatherConditions}</h3>
        <div className="weather-grid">
          <div className="weather-item">
            <span className="weather-label">{t.temperature}</span>
            <span className="weather-value">{prediction.temperature?.toFixed(1)}°C</span>
          </div>
          <div className="weather-item">
            <span className="weather-label">{t.humidity}</span>
            <span className="weather-value">{prediction.humidity}%</span>
          </div>
          <div className="weather-item">
            <span className="weather-label">{t.rainfall}</span>
            <span className="weather-value">{prediction.rainfall?.toFixed(1)} mm</span>
          </div>
        </div>
      </div>

      {/* Soil Values */}
      <div className="result-section">
        <h3 className="section-title">{t.soilValues}</h3>
        <div className="soil-grid">
          <div className="soil-item">
            <span className="label">N (Nitrogen)</span>
            <span className="value">{prediction.soil_values_used.nitrogen}</span>
          </div>
          <div className="soil-item">
            <span className="label">P (Phosphorous)</span>
            <span className="value">{prediction.soil_values_used.phosphorous}</span>
          </div>
          <div className="soil-item">
            <span className="label">K (Potassium)</span>
            <span className="value">{prediction.soil_values_used.potassium}</span>
          </div>
          <div className="soil-item">
            <span className="label">pH</span>
            <span className="value">{prediction.soil_values_used.ph}</span>
          </div>
        </div>
      </div>

      {/* Advisory Message */}
      <div className="result-section">
        <h3 className="section-title">{t.advisory}</h3>
        <div className="advisory-message">
          <p>{prediction.advisory_message}</p>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
