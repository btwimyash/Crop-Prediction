/**
 * API Service - Handles all HTTP requests to the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// =============================================================================
// CROP PREDICTION API CALLS
// =============================================================================

/**
 * Get crop predictions based on user input
 */
export const predictCrop = async (predictionData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(predictionData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Prediction failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Prediction error:", error);
    throw error;
  }
};

// =============================================================================
// CHATBOT API CALLS
// =============================================================================

/**
 * Send message to chatbot
 */
export const sendChatMessage = async (message, sessionId, language = "en") => {
  try {
    const response = await fetch(`${API_BASE_URL}/chatbot/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        language,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Chat failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Chat error:", error);
    throw error;
  }
};

// =============================================================================
// UTILITY API CALLS
// =============================================================================

/**
 * Get list of all states
 */
export const getStates = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/states/`);
    if (!response.ok) throw new Error("Failed to fetch states");
    return await response.json();
  } catch (error) {
    console.error("Error fetching states:", error);
    throw error;
  }
};

/**
 * Get districts for a given state
 */
export const getDistricts = async (state) => {
  try {
    const response = await fetch(`${API_BASE_URL}/districts/${state}`);
    if (!response.ok) throw new Error("Failed to fetch districts");
    return await response.json();
  } catch (error) {
    console.error("Error fetching districts:", error);
    throw error;
  }
};

/**
 * Get list of months
 */
export const getMonths = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/months/`);
    if (!response.ok) throw new Error("Failed to fetch months");
    return await response.json();
  } catch (error) {
    console.error("Error fetching months:", error);
    throw error;
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error("Health check failed:", error);
    return null;
  }
};

export default {
  predictCrop,
  sendChatMessage,
  getStates,
  getDistricts,
  getMonths,
  healthCheck,
};
