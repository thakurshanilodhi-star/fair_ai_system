# यह file fairness metrics calculate करने के लिए है

# -------------------------------
# Selection Rate
# -------------------------------
def calculate_selection_rate(df, sensitive_col, target_col):
    """
    हर group का selection rate निकालता है
    """
    return df.groupby(sensitive_col)[target_col].mean()


# -------------------------------
# Disparate Impact (DI)
# -------------------------------
def disparate_impact(rates):
    """
    DI = min(selection rate) / max(selection rate
    """
    values = list(rates.values())

    if len(values) == 2 and max(values) != 0:
        return min(values) / max(values)

    return 1


# -------------------------------
# Statistical Parity Difference (SPD)
# -------------------------------
def statistical_parity_difference(rates):
    """
    SPD = difference between group selection rates
    """
    values = list(rates.values())

    if len(values) == 2:
        return values[0] - values[1]

    return 0


# -------------------------------
# Equal Opportunity Difference (EOD)
# -------------------------------
def equal_opportunity_difference(df, sensitive_col, target_col):
    """
    Simplified version:
    Positive outcome rate difference
    """

    groups = df.groupby(sensitive_col)
    rates = []

    for _, group in groups:
        total = len(group)

        if total == 0:
            rate = 0
        else:
            positive = group[group[target_col] == 1]
            rate = len(positive) / total

        rates.append(rate)

    if len(rates) == 2:
        return rates[0] - rates[1]

    return 0


# -------------------------------
# Risk Level
# -------------------------------
def calculate_risk(di):
    """
    DI के आधार पर risk level निकालता है
    """
    if di < 0.5:
        return "High Risk"
    elif di < 0.8:
        return "Medium Risk"
    else:
        return "Low Risk"


# -------------------------------
# ALL METRICS TOGETHER
# -------------------------------
def calculate_all_metrics(df, sensitive_col, target_col):
    """
    सभी fairness metrics एक साथ return करता है
    """

    # selection rate
    rates_series = calculate_selection_rate(df, sensitive_col, target_col)
    rates = rates_series.to_dict()

    # metrics
    di = disparate_impact(rates)
    spd = statistical_parity_difference(rates)
    eod = equal_opportunity_difference(df, sensitive_col, target_col)

    # risk
    risk = calculate_risk(di)

    return {
        "selection_rates": rates,
        "disparate_impact": di,
        "statistical_parity_difference": spd,
        "equal_opportunity_difference": eod,
        "risk_level": risk
    }