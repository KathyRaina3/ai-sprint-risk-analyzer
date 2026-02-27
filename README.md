# AI-Powered Sprint Risk Analyzer

## Overview
This project simulates an AI-enabled product management workflow by analyzing sprint updates and identifying delivery risks using automated logic.

It demonstrates how data-driven decision-making can improve sprint visibility and risk mitigation.

---

## Problem Statement
Product managers often rely on manual updates and subjective judgment to assess sprint health. This creates blind spots in:

- Delivery risk
- Blocker impact
- Low progress detection
- Early warning signals

---

## Solution
This project builds a lightweight Python-based risk analysis engine that:

- Reads structured sprint update data
- Applies risk detection logic
- Flags high, medium, and low risk items
- Outputs an updated dataset for decision-making

---

## Project Structure
- `sprint_updates.csv` → Synthetic sprint dataset
- `risk_analyzer.py` → Risk detection logic
- `sprint_updates_with_risk.csv` → Output file with risk levels

---

## Risk Logic

- High Risk → If blockers > 0
- Medium Risk → If progress < 50%
- Low Risk → Otherwise

---

## Tools Used
- Python
- Pandas
- GitHub version control

---

## How to Run

```bash
pip install pandas
python risk_analyzer.py
```

---

## Business Impact

- Enables proactive sprint monitoring
- Reduces delivery uncertainty
- Improves stakeholder reporting
- Demonstrates AI-assisted product decision workflows

---

## Future Improvements

- Integrate with Jira API
- Add ML-based risk prediction
- Create dashboard visualization
- Automate weekly reporting

---

Author: Kathy Raina
