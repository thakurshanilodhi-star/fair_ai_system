# यह file machine learning model training और prediction के लिए है

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# -------------------------------
# Single Model Training
# -------------------------------
def train_model(X, y, model_type="logistic"):
    """
    model_type:
    - logistic
    - decision_tree
    """

    # data split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # model selection
    if model_type == "logistic":
        model = LogisticRegression(max_iter=1000)

    elif model_type == "decision_tree":
        model = DecisionTreeClassifier()

    else:
        model = LogisticRegression(max_iter=1000)

    # training
    model.fit(X_train, y_train)

    # prediction
    preds = model.predict(X_test)

    # accuracy
    acc = accuracy_score(y_test, preds)

    return model, X_test, y_test, preds, acc


# -------------------------------
# Multi Model Comparison
# -------------------------------
def compare_models(X, y):
    """
    दो models compare करता है
    """

    results = {}

    # Logistic Regression
    _, _, _, _, acc1 = train_model(X, y, "logistic")
    results["Logistic Regression"] = acc1

    # Decision Tree
    _, _, _, _, acc2 = train_model(X, y, "decision_tree")
    results["Decision Tree"] = acc2

    return results


# -------------------------------
# Best Model Selection
# -------------------------------
def get_best_model(X, y):
    """
    best performing model return करता है
    """

    models = ["logistic", "decision_tree"]
    best_model = None
    best_acc = 0

    for m in models:
        model, X_test, y_test, preds, acc = train_model(X, y, m)

        if acc > best_acc:
            best_acc = acc
            best_model = {
                "model": model,
                "type": m,
                "accuracy": acc,
                "X_test": X_test,
                "y_test": y_test,
                "predictions": preds
            }

    return best_model