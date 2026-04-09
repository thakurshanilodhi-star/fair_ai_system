import matplotlib
matplotlib.use('Agg')

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import base64
from io import BytesIO
import datetime
import json
import traceback

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

app = Flask(__name__)
CORS(app)

# -------------------------------
# HISTORY
# -------------------------------
HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_history(entry):
    with open(HISTORY_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)

# -------------------------------
# GRAPH → BASE64
# -------------------------------
def fig_to_base64(fig):
    import matplotlib.pyplot as plt
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.read()).decode("utf-8")

# -------------------------------
# LOAD FILE
# -------------------------------
def load_file(file):
    try:
        if file.filename.endswith(".csv"):
            return pd.read_csv(file)
        elif file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
            return text_to_dataframe(text)
        return None
    except:
        return None

# -------------------------------
# SUGGESTIONS
# -------------------------------
def generate_suggestions(before, after):
    suggestions = []

    if before.get("disparate_impact", 1) < 0.8:
        suggestions.append("Bias detected → Improve mitigation")

    if after.get("disparate_impact", 1) >= 0.8:
        suggestions.append("Bias reduced successfully")

    if after.get("risk_level") == "High":
        suggestions.append("High risk model → retrain required")

    return suggestions

# -------------------------------
# ANALYSIS
# -------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("file")
        mode = request.form.get("mode", "Auto AI")

        if not file:
            return jsonify({"error": "No file uploaded"})

        df = load_file(file)
        if df is None:
            return jsonify({"error": "File processing failed"})

        df = df.dropna()

        # 🔥 SPEED FIX
        if df.shape[0] > 5000:
            df = df.sample(5000)

        cols = df.columns.tolist()
        suggested = detect_sensitive_columns(df)

        sensitive_col = suggested[0] if suggested else cols[0]
        target_col = cols[-1]

        # BEFORE
        before = detect_bias(df, sensitive_col, target_col)
        graph_before = fig_to_base64(plot_selection_rates(before["selection_rates"]))

        # 🔥 MODE BASED MITIGATION
        if mode == "Manual":
            method = "oversample"
        elif mode == "Hybrid":
            method = "reweight"
        else:
            method = "reweight"

        df_balanced = apply_mitigation(df, sensitive_col, method)

        # AFTER
        after = detect_bias(df_balanced, sensitive_col, target_col)
        graph_after = fig_to_base64(plot_before_after(before["selection_rates"], after["selection_rates"]))
        graph_metrics = fig_to_base64(plot_metrics_comparison(before, after))

        # MODEL SAFE
        df_encoded = preprocess_data(df_balanced)

        if df_encoded.shape[0] > 5000:
            df_encoded = df_encoded.sample(5000)

        X, y = split_features_target(df_encoded, target_col)
        best = get_best_model(X, y)

        # EXPLANATION
        explanation = generate_explanation(before, after)
        suggestions = generate_suggestions(before, after)

        save_history({
            "time": str(datetime.datetime.now()),
            "accuracy": best["accuracy"],
            "risk": after.get("risk_level")
        })

        return jsonify({
            "preview": df.head(8).to_dict(orient="records"),

            "dashboard": {
                "di": round(after.get("disparate_impact", 0), 2),
                "spd": round(after.get("statistical_parity_difference", 0), 2),
                "risk": after.get("risk_level", "Unknown")
            },

            "model": {
                "type": best["type"],
                "accuracy": round(best["accuracy"], 2)
            },

            "graphs": {
                "before": graph_before,
                "after": graph_after,
                "metrics": graph_metrics
            },

            "explanation": explanation,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})

# -------------------------------
# CHAT
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        context = data.get("context", {})
        response = get_response(message, context)
        return jsonify({"response": response})
    except:
        return jsonify({"response": "AI error"})

# -------------------------------
# VOICE
# -------------------------------
@app.route("/speak", methods=["POST"])
def voice():
    speak(request.json.get("text", ""))
    return jsonify({"status": "spoken"})

# -------------------------------
# HISTORY
# -------------------------------
@app.route("/history", methods=["GET"])
def history():
    with open(HISTORY_FILE, "r") as f:
        return jsonify(json.load(f))

# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return jsonify({"status": "FairAI Backend Running 🚀"})

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=False)