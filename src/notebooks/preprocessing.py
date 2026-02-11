import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../healthcare-dataset-stroke-data.csv")

df = pd.read_csv(csv_path)

# Interpolate only numeric columns
df = df.select_dtypes(include=["number"]).interpolate(
    method="linear", limit_direction="both"
)
df = df.dropna()

features = ["age", "bmi", "avg_glucose_level", "hypertension", "heart_disease"]

df = df[features]

df["severity_score"] = (
    (df["age"] > 60).astype(int)
    + (df["bmi"] > 30).astype(int)
    + (df["avg_glucose_level"] > 140).astype(int)
    + df["hypertension"]
    + df["heart_disease"]
)


def map_severity(score):
    if score <= 1:
        return 0
    elif score == 2:
        return 1
    elif score == 3:
        return 2
    return 3


df["stroke_severity"] = df["severity_score"].apply(map_severity)
df["stroke_severity"].value_counts()

output_path = os.path.join(script_dir, "../preprocessed_data.csv")
df.to_csv(output_path, index=False)
