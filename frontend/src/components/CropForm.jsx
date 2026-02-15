/**
 * CropForm Component - Main form for crop prediction
 */

import React, { useState, useEffect } from "react";
import { predictCrop, getStates, getDistricts, getMonths } from "../services/api";
import "./CropForm.css";

const CropForm = ({ onPredictionSuccess, onError, language = "en" }) => {
  const [formData, setFormData] = useState({
    state: "",
    district: "",
    month: "",
    nitrogen: "",
    phosphorous: "",
    potassium: "",
    ph: "",
    language: language,
    use_auto_values: true,
  });

  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [months, setMonths] = useState([]);
  const [loading, setLoading] = useState(false);
  const [useOwnValues, setUseOwnValues] = useState(false);
  const [errors, setErrors] = useState({});

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [statesData, monthsData] = await Promise.all([
          getStates(),
          getMonths(),
        ]);
        setStates(statesData.states || []);
        setMonths(monthsData.months || []);
      } catch (error) {
        onError("Failed to load data");
      }
    };
    loadData();
  }, [onError]);

  // Load districts when state changes
  useEffect(() => {
    const loadDistricts = async () => {
      if (formData.state) {
        try {
          const data = await getDistricts(formData.state);
          setDistricts(data.districts || []);
        } catch (error) {
          setDistricts([]);
        }
      }
    };
    loadDistricts();
  }, [formData.state]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Clear error for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.state) newErrors.state = "State is required";
    if (!formData.district) newErrors.district = "District is required";
    if (!formData.month) newErrors.month = "Month is required";

    if (useOwnValues) {
      if (formData.nitrogen === "" || isNaN(formData.nitrogen))
        newErrors.nitrogen = "Valid nitrogen value required";
      if (formData.phosphorous === "" || isNaN(formData.phosphorous))
        newErrors.phosphorous = "Valid phosphorous value required";
      if (formData.potassium === "" || isNaN(formData.potassium))
        newErrors.potassium = "Valid potassium value required";
      if (formData.ph === "" || isNaN(formData.ph))
        newErrors.ph = "Valid pH value required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      onError("Please fill all required fields correctly");
      return;
    }

    setLoading(true);

    try {
      const submitData = {
        state: formData.state,
        district: formData.district,
        month: formData.month,
        language: formData.language,
        use_auto_values: !useOwnValues,
      };

      // Add soil values only if user provided them
      if (useOwnValues) {
        submitData.nitrogen = parseFloat(formData.nitrogen);
        submitData.phosphorous = parseFloat(formData.phosphorous);
        submitData.potassium = parseFloat(formData.potassium);
        submitData.ph = parseFloat(formData.ph);
      }

      const result = await predictCrop(submitData);
      onPredictionSuccess(result);
    } catch (error) {
      onError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const labels = {
    en: {
      state: "State",
      district: "District",
      month: "Month",
      nitrogen: "Nitrogen (N)",
      phosphorous: "Phosphorous (P)",
      potassium: "Potassium (K)",
      ph: "pH Value",
      submit: "Get Recommendation",
      useSoilValues: "Use My Own Soil Values",
      autoDetect: "Auto Detect Soil Values",
      selectState: "Select State",
      selectDistrict: "Select District",
      selectMonth: "Select Month",
    },
    hi: {
      state: "राज्य",
      district: "जिला",
      month: "महीना",
      nitrogen: "नाइट्रोजन (N)",
      phosphorous: "फॉस्फोरस (P)",
      potassium: "पोटेशियम (K)",
      ph: "pH मान",
      submit: "सिफारिश प्राप्त करें",
      useSoilValues: "मेरे अपने मिट्टी मान का उपयोग करें",
      autoDetect: "मिट्टी मान स्वचालित रूप से प्राप्त करें",
      selectState: "राज्य चुनें",
      selectDistrict: "जिला चुनें",
      selectMonth: "महीना चुनें",
    },
    mr: {
      state: "राज्य",
      district: "जिल्हा",
      month: "महिना",
      nitrogen: "नायट्रोजन (N)",
      phosphorous: "फॉस्फोरस (P)",
      potassium: "पोटॅशियम (K)",
      ph: "pH मूल्य",
      submit: "शिफारस प्राप्त करा",
      useSoilValues: "माझे स्वतःचे माती मूल्य वापरा",
      autoDetect: "माती मूल्य स्वयंचलितपणे शोधा",
      selectState: "राज्य निवडा",
      selectDistrict: "जिल्हा निवडा",
      selectMonth: "महिना निवडा",
    },
  };

  const t = labels[language] || labels.en;

  return (
    <form className="crop-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>{t.state}</label>
        <select
          name="state"
          value={formData.state}
          onChange={handleInputChange}
          className={errors.state ? "input-error" : ""}
        >
          <option value="">{t.selectState}</option>
          {states.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
        {errors.state && <span className="error">{errors.state}</span>}
      </div>

      <div className="form-group">
        <label>{t.district}</label>
        <select
          name="district"
          value={formData.district}
          onChange={handleInputChange}
          disabled={!formData.state}
          className={errors.district ? "input-error" : ""}
        >
          <option value="">{t.selectDistrict}</option>
          {districts.map((district) => (
            <option key={district} value={district}>
              {district}
            </option>
          ))}
        </select>
        {errors.district && <span className="error">{errors.district}</span>}
      </div>

      <div className="form-group">
        <label>{t.month}</label>
        <select
          name="month"
          value={formData.month}
          onChange={handleInputChange}
          className={errors.month ? "input-error" : ""}
        >
          <option value="">{t.selectMonth}</option>
          {months.map((month) => (
            <option key={month} value={month}>
              {month}
            </option>
          ))}
        </select>
        {errors.month && <span className="error">{errors.month}</span>}
      </div>

      {/* Toggle for soil values */}
      <div className="toggle-group">
        <label className="toggle-label">
          <input
            type="checkbox"
            checked={useOwnValues}
            onChange={(e) => setUseOwnValues(e.target.checked)}
          />
          <span className="toggle-text">
            {useOwnValues ? t.useSoilValues : t.autoDetect}
          </span>
        </label>
      </div>

      {/* Soil value inputs - only show if useOwnValues is true */}
      {useOwnValues && (
        <div className="soil-values-group">
          <div className="form-row">
            <div className="form-group">
              <label>{t.nitrogen}</label>
              <input
                type="number"
                name="nitrogen"
                value={formData.nitrogen}
                onChange={handleInputChange}
                placeholder="0-140"
                className={errors.nitrogen ? "input-error" : ""}
              />
              {errors.nitrogen && (
                <span className="error">{errors.nitrogen}</span>
              )}
            </div>

            <div className="form-group">
              <label>{t.phosphorous}</label>
              <input
                type="number"
                name="phosphorous"
                value={formData.phosphorous}
                onChange={handleInputChange}
                placeholder="0-145"
                className={errors.phosphorous ? "input-error" : ""}
              />
              {errors.phosphorous && (
                <span className="error">{errors.phosphorous}</span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>{t.potassium}</label>
              <input
                type="number"
                name="potassium"
                value={formData.potassium}
                onChange={handleInputChange}
                placeholder="0-205"
                className={errors.potassium ? "input-error" : ""}
              />
              {errors.potassium && (
                <span className="error">{errors.potassium}</span>
              )}
            </div>

            <div className="form-group">
              <label>{t.ph}</label>
              <input
                type="number"
                name="ph"
                value={formData.ph}
                onChange={handleInputChange}
                placeholder="0-14"
                step="0.1"
                className={errors.ph ? "input-error" : ""}
              />
              {errors.ph && <span className="error">{errors.ph}</span>}
            </div>
          </div>
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="submit-button"
      >
        {loading ? "Processing..." : t.submit}
      </button>
    </form>
  );
};

export default CropForm;
