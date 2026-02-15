/**
 * Chatbot Component - Conversational interface for crop advisory
 */

import React, { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "../services/api";
import "./Chatbot.css";

const Chatbot = ({ onRecommendation, language = "en" }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(Math.random().toString(36).substr(2, 9));
  const messagesEndRef = useRef(null);
  const initialized = useRef(false);

  // Initialize chatbot
  useEffect(() => {
    if (!initialized.current) {
      initializeChatbot();
      initialized.current = true;
    }
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const initializeChatbot = async () => {
    try {
      setLoading(true);
      const response = await sendChatMessage("hello", sessionId, language);
      setMessages([
        {
          type: "bot",
          text: response.message,
          requiresInput: response.requires_input,
        },
      ]);
    } catch (error) {
      setMessages([
        {
          type: "bot",
          text: "Sorry, I'm having trouble connecting. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    setMessages([...messages, { type: "user", text: inputValue }]);
    setInputValue("");
    setLoading(true);

    try {
      const response = await sendChatMessage(inputValue, sessionId, language);

      const botMessage = {
        type: "bot",
        text: response.message,
        requiresInput: response.requires_input,
      };

      setMessages((prev) => [...prev, botMessage]);

      // If recommendation received, notify parent
      if (response.crop_recommendation && onRecommendation) {
        setTimeout(() => {
          onRecommendation(response.crop_recommendation);
        }, 1000);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>🌾 Crop Advisory Chatbot</h3>
        <p>Chat with me to get crop recommendations</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.type === "user" ? "user-message" : "bot-message"}`}
          >
            {msg.type === "bot" && <span className="bot-avatar">🤖</span>}
            <div className="message-content">
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot-message">
            <span className="bot-avatar">🤖</span>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chatbot-input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
          className="chatbot-input"
        />
        <button
          type="submit"
          disabled={loading || !inputValue.trim()}
          className="chatbot-send-btn"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
