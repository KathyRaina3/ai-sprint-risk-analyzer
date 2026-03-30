import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("SprintRisk AI - Sprint Risk Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload your sprint_updates.csv", type=["csv"])

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Risk detection logic
    def detect_risk(row):

        # High Risk
        if row["blockers"] > 0 and row["progress"] < 50:
            return "High"

        # Medium Risk
        elif row["blockers"] > 0:
            return "Medium"

        elif row["progress"] < 50:
            return "Medium"

        # Low Risk
        else:
            return "Low"

    # Apply risk logic
    df["Calculated Risk"] = df.apply(detect_risk, axis=1)

    st.subheader("Risk Analysis Results")

    st.dataframe(df)

    # ===============================
    # Risk Distribution Chart
    # ===============================

    st.subheader("Sprint Risk Distribution")

    risk_counts = df["Calculated Risk"].value_counts()

    fig, ax = plt.subplots()

    colors = []

    for risk in risk_counts.index:

        if risk == "High":
            colors.append("red")

        elif risk == "Medium":
            colors.append("orange")

        else:
            colors.append("green")

    ax.bar(risk_counts.index, risk_counts.values, color=colors)

    ax.set_xlabel("Risk Level")

    ax.set_ylabel("Count")

    ax.set_title("Sprint Risk Distribution")

    st.pyplot(fig)

    # ===============================
    # Sprint Summary Metrics
    # ===============================

    total_tasks = len(df)
    high_risk_tasks = len(df[df["Calculated Risk"] == "High"])
    medium_risk_tasks = len(df[df["Calculated Risk"] == "Medium"])
    low_risk_tasks = len(df[df["Calculated Risk"] == "Low"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("High Risk", high_risk_tasks)
    col3.metric("Medium Risk", medium_risk_tasks)
    col4.metric("Low Risk", low_risk_tasks)

    # ===============================
    # Blocker Summary
    # ===============================

    total_blockers = df["blockers"].sum()

    st.subheader("Blocker Summary")

    st.metric("Total Blockers", total_blockers)

    # ===============================
    # Progress Summary
    # ===============================

    avg_progress = df["progress"].mean()

    st.subheader("Progress Summary")

    st.metric("Average Progress (%)", round(avg_progress, 1))

    # ===============================
    # Sprint Health Score
    # ===============================

    health_score = (
        (low_risk_tasks * 1.0)
        + (medium_risk_tasks * 0.5)
        + (high_risk_tasks * 0.2)
    ) / total_tasks * 100

    st.subheader("Sprint Health Score")

    st.metric("Sprint Health (%)", round(health_score, 1))

    # ===============================
    # Download Updated CSV
    # ===============================

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV with Calculated Risk",
        data=csv,
        file_name="sprint_updates_with_risk.csv",
        mime="text/csv"
    )