# यह file bias detect करने के लिए है

def calculate_selection_rate(df, sensitive_col, target_col):
    # हर group का selection rate निकालता है
    return df.groupby(sensitive_col)[target_col].mean()


def disparate_impact(df, sensitive_col, target_col):
    rates = calculate_selection_rate(df, sensitive_col, target_col)

    if len(rates) == 2:
        return min(rates) / max(rates)

    return 1


def detect_bias(df, sensitive_col, target_col):
    rates = calculate_selection_rate(df, sensitive_col, target_col)
    di = disparate_impact(df, sensitive_col, target_col)

    # bias check
    bias = "Yes" if di < 0.8 else "No"

    return {
        "selection_rates": rates.to_dict(),
        "disparate_impact": di,
        "bias": bias
    }