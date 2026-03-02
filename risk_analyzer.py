import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("sprint_updates.csv")

# Text-based risk detection
def calculate_risk(text):
    text = text.lower()
    
    if "blocked" in text or "critical" in text:
        return "High Risk"
    elif "delay" in text or "issue" in text:
        return "Medium Risk"
    else:
        return "Low Risk"

# Apply logic
df["Risk Level"] = df["update_text"].apply(calculate_risk)

# Save output
df.to_csv("sprint_updates_with_risk.csv", index=False)

# Visualization
risk_counts = df["Risk Level"].value_counts()
risk_counts.plot(kind="bar")
plt.title("Sprint Risk Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("risk_distribution.png")
plt.show()

print("Risk analysis complete. Files generated.")