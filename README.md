# 🚀 SprintRisk AI — Sprint Risk Analyzer Dashboard

## 📌 Overview

SprintRisk AI is an interactive sprint monitoring dashboard built using Streamlit.
It analyzes sprint task data and automatically identifies project risks based on blockers and progress levels.

This tool helps teams monitor sprint health, track blockers, and visualize risks in real time.

---

## 📊 Dashboard Preview

### Sprint Risk Dashboard

![Sprint Dashboard]([Sprintrisk dashboard_streamlit.png](https://github.com/KathyRaina3/ai-sprint-risk-analyzer/blob/main/Sprintrisk%20dashboard_streamlit.png))

---

### Progress Metrics Summary

![Progress Summary]([Streamlit progress.png](https://github.com/KathyRaina3/ai-sprint-risk-analyzer/blob/main/Streamlit%20progress.png))

---

### Risk Distribution Graph

![Sprint Graph](sprintgraph.png)

---

## 🎯 Key Features

✅ Upload sprint update CSV file
✅ Automatic Risk Detection (High / Medium / Low)
✅ Risk Distribution Visualization
✅ Blocker Tracking
✅ Sprint Health Score Calculation
✅ Progress Monitoring
✅ Download Updated Risk Report

---

## 🧠 How Risk Is Calculated

Risk levels are calculated using task progress and blockers:

* **High Risk** → Blockers present AND progress below 50%
* **Medium Risk** → Blockers present OR progress below 50%
* **Low Risk** → No blockers AND good progress

Sprint Health Score is calculated based on:

* Low Risk Tasks → High contribution
* Medium Risk Tasks → Moderate contribution
* High Risk Tasks → Low contribution

This gives an overall percentage showing sprint stability.

---

## 📂 Sample Input Format

Example CSV structure:

ticket_id,progress,blockers
ENG-101,40,1
ENG-102,90,0
ENG-103,60,0
(https://github.com/KathyRaina3/ai-sprint-risk-analyzer/blob/main/sprint_updates_with_risk.csv)

---

## ⚙️ Technologies Used

* Python
* Pandas
* Matplotlib
* Streamlit

---

## ▶️ How to Run Locally

Step 1 — Install dependencies:

pip install streamlit pandas matplotlib

Step 2 — Run the app:

streamlit run sprintrisk_app.py

---

## 📈 Sprint Metrics Included

The dashboard calculates:

* Total Tasks
* High Risk Tasks
* Medium Risk Tasks
* Low Risk Tasks
* Total Blockers
* Average Progress (%)
* Sprint Health Score (%)

---

## 🚀 Future Enhancements

Planned improvements include:

* Risk trend analysis over time
* AI-based text risk detection
* Priority-based risk scoring
* Integration with sprint tools (Jira-style workflows)

---

## 👩‍💻 Project Purpose

This project demonstrates practical implementation of:

* Agile sprint monitoring
* Risk analysis automation
* Data visualization dashboards
* Project health tracking

It reflects real-world sprint risk management practices used in modern software teams.
