# यह file AI explanation generate करती है

def generate_explanation(before, after):

    explanation = ""

    # -------------------------------
    # BEFORE ANALYSIS
    # -------------------------------
    if before.get("bias") == "Yes":
        explanation += "Before mitigation, the dataset shows bias. "
    else:
        explanation += "Before mitigation, the dataset appears fair. "

    # -------------------------------
    # AFTER ANALYSIS
    # -------------------------------
    if after.get("bias") == "Yes":
        explanation += "After mitigation, some bias still exists. "
    else:
        explanation += "After mitigation, fairness has improved significantly. "

    # -------------------------------
    # METRICS INTERPRETATION
    # -------------------------------
    di = after.get("disparate_impact", 0)

    if di < 0.8:
        explanation += "Disparate Impact is low, indicating unfair outcomes. "
    else:
        explanation += "Disparate Impact is acceptable, indicating fair outcomes. "

    # -------------------------------
    # RISK LEVEL
    # -------------------------------
    risk = after.get("risk_level", "Unknown")

    if risk == "High Risk":
        explanation += "The system has high risk of bias."
    elif risk == "Medium Risk":
        explanation += "The system has moderate bias risk."
    else:
        explanation += "The system is considered fair and low risk."

    return explanation