import pandas as pd

# Load sprint updates dataset
df = pd.read_csv("sprint_updates.csv")

# Simple risk logic
def calculate_risk(row):
    if row["Blockers"] > 0 and row["Progress (%)"] < 50:
        return "Critical Risk"
    elif row["Blockers"] > 0:
        return "High Risk"
    elif row["Progress (%)"] < 50:
        return "Medium Risk"
    else:
        return "Low Risk"

# Apply risk logic
df["Risk Level"] = df.apply(calculate_risk, axis=1)

# Save updated file
df.to_csv("sprint_updates_with_risk.csv", index=False)

print("Risk analysis complete. Updated file saved.")
