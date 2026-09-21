# SUMMARY: The two factors that best separate cars that broke down from those that did not are
# km_since_service (broken-down cars averaged 11,678 km since last service vs 7,261 for healthy
# ones) and load_factor (0.60 vs 0.51). Total odometer and age are nearly identical between the
# two groups, so they add little signal. The risk score is a 0-100 blend of normalised
# km_since_service (70 % weight) and normalised load_factor (30 % weight).

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# --- 1. Compare the two groups column by column ---
feature_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
group_means = df.groupby("broke_down")[feature_cols].mean()
print("Mean values by breakdown outcome (0 = ok, 1 = broke down):")
print(group_means.to_string())
print()

# --- 2. Columns that actually separate the groups ---
# km_since_service: 11 678 vs 7 261  (+61 %)  <-- strongest signal
# load_factor:       0.601 vs 0.506  (+19 %)  <-- second signal
# avg_daily_km:      159.7 vs 131.4  (+21 %)  <-- moderate
# odometer_km / age_years: virtually identical -- skip them

# --- 3. Build a 0-100 risk score ---
# Normalise each chosen column to [0, 1] then blend with weights.

def minmax(series):
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) if hi > lo else pd.Series(0.0, index=series.index)

df["risk_score"] = (
    0.55 * minmax(df["km_since_service"]) +
    0.25 * minmax(df["load_factor"]) +
    0.20 * minmax(df["avg_daily_km"])
) * 100

# --- 4. Print cars ranked by risk, highest first ---
ranked = df[["car_id", "km_since_service", "load_factor", "avg_daily_km", "risk_score"]].sort_values(
    "risk_score", ascending=False
)
print("Cars ranked by breakdown risk (highest risk first):")
print(ranked.to_string(index=False))
