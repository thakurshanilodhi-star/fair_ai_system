import streamlit as st
import pandas as pd
import os

# modules
from fair_ai.bias_detection import detect_bias
from fair_ai.mitigation import apply_mitigation
from fair_ai.model import get_best_model
from fair_ai.ai_explainer import generate_explanation
from fair_ai.llm_bot import get_response
from fair_ai.voice import speak
from fair_ai.utils import preprocess_data, split_features_target, detect_sensitive_columns
from fair_ai.visualization import plot_selection_rates, plot_before_after, plot_metrics_comparison
from fair_ai.pdf_handler import extract_text_from_pdf, text_to_dataframe

st.set_page_config(page_title="FairAI Ultimate", layout="wide")

# -------------------------------
# 🎨 UI STYLE
# -------------------------------
st.markdown("""
<style>

/* 💧 Animated water gradient background */
html, body, [class*="css"] {
    background: linear-gradient(270deg, #020617, #0f172a, #1e3a8a, #06b6d4);
    background-size: 400% 400%;
    animation: waterFlow 12s ease infinite;
    color: white !important;
}

/* 🌊 Animation */
@keyframes waterFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 🚀 Glass effect container */
.block-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
}

/* 🔥 Header */
.header-box {
    background: linear-gradient(90deg, #1e3a8a, #06b6d4);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #00f5ff;
    box-shadow: 0 0 25px rgba(0,255,255,0.6);
}

/* 💬 Subtitle */
.subtitle {
    text-align: center;
    color: #cbd5f5;
}

/* 🔥 Inputs */
input, textarea {
    background-color: rgba(30, 41, 59, 0.8) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* 🔥 Selectbox */
.stSelectbox div {
    background-color: rgba(30, 41, 59, 0.8) !important;
    color: white !important;
}

/* 🔥 Buttons */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 10px;
    border: none;
}

/* 🤖 Chat box */
.chat-box {
    background: rgba(0,0,0,0.4);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(0,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🚀 HEADER
# -------------------------------
st.title("Fair AI System")
st.markdown("AI system to detect and reduce bias in datasets and models")

st.markdown("---")

# -------------------------------
# ⚙ MODE
# -------------------------------
mode = st.selectbox("Mode", ["Auto AI", "Manual", "Hybrid"])

# -------------------------------
# 📂 FILE UPLOAD
# -------------------------------
file = st.file_uploader("Upload Dataset (CSV or PDF)", type=["csv", "pdf"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        text = extract_text_from_pdf(file)
        df = text_to_dataframe(text)

        if df is None:
            st.error("PDF parsing failed")
            st.stop()
else:
    if os.path.exists("data/sample.csv"):
        df = pd.read_csv("data/sample.csv")
    else:
        st.warning("Upload dataset to continue")
        st.stop()

# -------------------------------
# 👀 PREVIEW
# -------------------------------
st.subheader("Dataset Preview")
st.write(df.head())

st.markdown("---")

# -------------------------------
# 🎯 COLUMN SELECT
# -------------------------------
cols = df.columns.tolist()
suggested = detect_sensitive_columns(df)

if mode == "Auto AI":
    sensitive_col = suggested[0] if suggested else cols[0]
    target_col = cols[-1]
else:
    col1, col2 = st.columns(2)
    sensitive_col = col1.selectbox("Sensitive Column", cols)
    target_col = col2.selectbox("Target Column", cols)

# -------------------------------
# ▶ RUN
# -------------------------------
if st.button("🚀 Run Full Analysis"):

    with st.spinner("Processing..."):

        df = df.dropna()

        # BEFORE
        st.subheader("Before Mitigation")
        result_before = detect_bias(df, sensitive_col, target_col)
        st.write(result_before)

        st.pyplot(plot_selection_rates(result_before["selection_rates"]))

        st.markdown("---")

        # MITIGATION
        method = "reweight"
        if mode == "Manual":
            method = st.selectbox("Mitigation Method", ["reweight", "oversample"])

        df_balanced = apply_mitigation(df, sensitive_col, method)

        # AFTER
        st.subheader("After Mitigation")
        result_after = detect_bias(df_balanced, sensitive_col, target_col)
        st.write(result_after)

        st.pyplot(plot_before_after(
            result_before["selection_rates"],
            result_after["selection_rates"]
        ))

        st.pyplot(plot_metrics_comparison(result_before, result_after))

        st.markdown("---")

        # DASHBOARD
        st.subheader("Fairness Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Disparate Impact", round(result_after.get("disparate_impact", 0), 2))
        col2.metric("SPD", round(result_after.get("statistical_parity_difference", 0), 2))
        col3.metric("Risk Level", result_after.get("risk_level", "Unknown"))

        st.markdown("---")

        # MODEL
        st.subheader("Model Performance")

        df_encoded = preprocess_data(df_balanced)
        X, y = split_features_target(df_encoded, target_col)

        best = get_best_model(X, y)

        st.write("Model:", best["type"])
        st.write("Accuracy:", round(best["accuracy"], 2))

        st.markdown("---")

        # EXPLANATION
        st.subheader("AI Explanation")

        explanation = generate_explanation(result_before, result_after)
        st.write(explanation)

        # VOICE
        col1, col2 = st.columns(2)

        if col1.button("🔊 Speak"):
            speak(explanation)

        if col2.checkbox("Auto Speak"):
            speak(explanation)

# -------------------------------
# 🤖 AI ASSISTANT (COOL STYLE)
# -------------------------------
st.markdown("---")

st.markdown("""
<h2 style="
color:#00ffe1;
text-shadow: 0 0 10px #00ffe1;
">
🦋 AI Assistant 🤖
</h2>
""", unsafe_allow_html=True)

user_input = st.text_input("Ask anything about bias or model")

if user_input:
    response = get_response(user_input, {})
    st.markdown(f"""
    <div style="background:#1c1f26;padding:15px;border-radius:10px;">
    <b>You:</b> {user_input}<br><br>
    <b>AI:</b> {response}
    </div>
    """, unsafe_allow_html=True)