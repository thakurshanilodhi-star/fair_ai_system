# यह file helper functions के लिए है

import pandas as pd


# -------------------------------
# Data Preprocessing
# -------------------------------
import pandas as pd

def preprocess_data(df):

    # limit columns
    if df.shape[1] > 20:
        df = df.iloc[:, :20]

    # limit rows
    if df.shape[0] > 5000:
        df = df.sample(5000, random_state=42)

    df = pd.get_dummies(df, drop_first=True)

    return df


# -------------------------------
# Separate Features and Target
# -------------------------------
def split_features_target(df, target_col):
    """
    X (features) और y (target) अलग करता है
    """

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    return X, y


# -------------------------------
# Detect Possible Sensitive Columns
# -------------------------------
def detect_sensitive_columns(df):
    """
    possible sensitive columns suggest करता है
    """

    keywords = ["gender", "sex", "caste", "religion", "age"]

    sensitive_cols = []

    for col in df.columns:
        for key in keywords:
            if key in col.lower():
                sensitive_cols.append(col)

    return sensitive_cols


# -------------------------------
# Basic Data Info
# -------------------------------
def get_data_info(df):
    """
    dataset का basic summary देता है
    """

    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns)
    }

    return info


# -------------------------------
# Validate Target Column
# -------------------------------
def validate_target(df, target_col):
    """
    check करता है कि target binary है या नहीं
    """

    unique_vals = df[target_col].unique()

    if len(unique_vals) == 2:
        return True
    else:
        return False