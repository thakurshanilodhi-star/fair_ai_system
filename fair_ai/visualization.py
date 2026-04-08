# यह file graphs और charts के लिए है

import matplotlib.pyplot as plt


# -------------------------------
# Selection Rate Chart
# -------------------------------
def plot_selection_rates(rates):

    groups = list(rates.keys())
    values = list(rates.values())

    fig, ax = plt.subplots()
    ax.bar(groups, values)

    ax.set_title("Selection Rates by Group")
    ax.set_xlabel("Group")
    ax.set_ylabel("Selection Rate")

    return fig


# -------------------------------
# Before vs After Comparison
# -------------------------------
def plot_before_after(before_rates, after_rates):

    groups = list(before_rates.keys())

    before_values = list(before_rates.values())
    after_values = list(after_rates.values())

    x = range(len(groups))

    fig, ax = plt.subplots()

    ax.bar(x, before_values, width=0.4, label="Before")
    ax.bar([i + 0.4 for i in x], after_values, width=0.4, label="After")

    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(groups)

    ax.set_title("Before vs After Bias Comparison")
    ax.set_xlabel("Group")
    ax.set_ylabel("Selection Rate")

    ax.legend()

    return fig


# -------------------------------
# Metrics Comparison (FIXED)
# -------------------------------
def plot_metrics_comparison(before, after):

    labels = ["Disparate Impact", "SPD"]

    # SAFE access (no error)
    before_values = [
        before.get("disparate_impact", 0),
        before.get("statistical_parity_difference", 0)
    ]

    after_values = [
        after.get("disparate_impact", 0),
        after.get("statistical_parity_difference", 0)
    ]

    x = range(len(labels))

    fig, ax = plt.subplots()

    ax.bar(x, before_values, width=0.4, label="Before")
    ax.bar([i + 0.4 for i in x], after_values, width=0.4, label="After")

    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(labels)

    ax.set_title("Fairness Metrics Comparison")
    ax.legend()

    return fig