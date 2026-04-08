# यह file bias कम करने के लिए है

import pandas as pd

def reweight_dataset(df, sensitive_col, target_col):
    """
    Dataset balancing के जरिए bias reduce करता है
    """

    # हर group का count निकालो
    group_counts = df[sensitive_col].value_counts()

    # minimum group size
    min_count = group_counts.min()

    # balanced dataset बनाओ
    balanced_df = df.groupby(sensitive_col).apply(
        lambda x: x.sample(min_count, random_state=42)
    ).reset_index(drop=True)

    return balanced_df


# -------------------------------
# Advanced Mitigation (Optional)
# -------------------------------
def oversample_minority(df, sensitive_col):
    """
    छोटे group को बड़ा करके balance करता है
    """

    group_counts = df[sensitive_col].value_counts()
    max_count = group_counts.max()

    balanced_df = df.groupby(sensitive_col).apply(
        lambda x: x.sample(max_count, replace=True, random_state=42)
    ).reset_index(drop=True)

    return balanced_df


# -------------------------------
# Main Mitigation Controller
# -------------------------------
def apply_mitigation(df, sensitive_col, method="reweight"):
    """
    अलग-अलग mitigation method apply करने के लिए
    """

    if method == "reweight":
        return reweight_dataset(df, sensitive_col, None)

    elif method == "oversample":
        return oversample_minority(df, sensitive_col)

    else:
        # fallback: original dataset
        return df