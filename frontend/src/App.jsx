/**
 * Main App Component
 */

import React, { useState } from "react";
import CropForm from "./components/CropForm";
import ResultCard from "./components/ResultCard";
import Chatbot from "./components/Chatbot";
import "./App.css";

function App() {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("form"); // form, chatbot
  const [language, setLanguage] = useState("en");

  const handlePredictionSuccess = (result) => {
    setPrediction(result);
    setError(null);
    setActiveTab("result");
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setPrediction(null);
  };

  const handleChatbotRecommendation = (recommendation) => {
    setActiveTab("result");
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🌾 Smart Crop Advisory System</h1>
          <p>AI-Powered Crop Recommendations for Better Farming</p>
        </div>
        
        {/* Language Selector */}
        <div className="language-selector">
          <button
            className={`lang-btn ${language === "en" ? "active" : ""}`}
            onClick={() => setLanguage("en")}
          >
            🇬🇧 English
          </button>
          <button
            className={`lang-btn ${language === "hi" ? "active" : ""}`}
            onClick={() => setLanguage("hi")}
          >
            🇮🇳 हिंदी
          </button>
          <button
            className={`lang-btn ${language === "mr" ? "active" : ""}`}
            onClick={() => setLanguage("mr")}
          >
            🇮🇳 मराठी
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Tabs */}
          <div className="tabs">
            <button
              className={`tab-button ${activeTab === "form" ? "active" : ""}`}
              onClick={() => setActiveTab("form")}
            >
              📋 Recommendation Form
            </button>
            <button
              className={`tab-button ${activeTab === "chatbot" ? "active" : ""}`}
              onClick={() => setActiveTab("chatbot")}
            >
              💬 Chatbot Assistant
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="error-alert">
              <span>❌ {error}</span>
              <button onClick={() => setError(null)}>×</button>
            </div>
          )}

          {/* Content Area */}
          <div className="content-area">
            {/* Form Tab */}
            {activeTab === "form" && (
              <div className="tab-content">
                <CropForm
                  onPredictionSuccess={handlePredictionSuccess}
                  onError={handleError}
                  language={language}
                />
              </div>
            )}

            {/* Chatbot Tab */}
            {activeTab === "chatbot" && (
              <div className="tab-content">
                <Chatbot
                  onRecommendation={handleChatbotRecommendation}
                  language={language}
                />
              </div>
            )}

            {/* Results */}
            {prediction && activeTab !== "chatbot" && (
              <div className="tab-content">
                <ResultCard prediction={prediction} language={language} />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          🌾 Smart Crop Advisory System © 2024 | Powered by AI & Machine Learning
        </p>
        <p>For support, contact: support@cropadvice.com</p>
      </footer>
    </div>
  );
}

export default App;
