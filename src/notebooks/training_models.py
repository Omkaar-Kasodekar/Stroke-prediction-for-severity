import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../preprocessed_data.csv")
model_dir = os.path.join(script_dir, "../model")

# Create model directory if it doesn't exist
os.makedirs(model_dir, exist_ok=True)

df = pd.read_csv(csv_path)

X = df.drop(columns=["stroke_severity", "severity_score"])
y = df["stroke_severity"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)

dt_model.fit(X_train, y_train)
dt_preds = dt_model.predict(X_test)

print("Decision Tree Results")
print(classification_report(y_test, dt_preds))

gb_model = GradientBoostingClassifier(
    n_estimators=150, learning_rate=0.05, max_depth=3, random_state=42
)

gb_model.fit(X_train, y_train)
gb_preds = gb_model.predict(X_test)

print("Gradient Boosting Results")
print(classification_report(y_test, gb_preds))

joblib.dump(dt_model, os.path.join(model_dir, "decision_tree.joblib"))
joblib.dump(gb_model, os.path.join(model_dir, "gradient_boosting.joblib"))
