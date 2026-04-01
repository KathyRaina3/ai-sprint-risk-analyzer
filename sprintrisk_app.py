import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ===============================
# Title
# ===============================
st.title("SprintRisk AI - Universal Sprint Risk Analyzer")

# ===============================
# Project Screenshots (Optional)
# ===============================
st.subheader("Project Overview Screenshots")
col1, col2, col3 = st.columns(3)

try:
    img1 = Image.open("Sprint_graph.png")
    img2 = Image.open("Sprintrisk_dashboard_streamlit.png")
    img3 = Image.open("Streamlit_progress.png")

    col1.image(img1, width=300, caption="Sprint Graph")
    col2.image(img2, width=300, caption="Sprint Risk Dashboard")
    col3.image(img3, width=300, caption="Progress Metrics")
except:
    st.info("Project screenshots not found.")

# ===============================
# File Upload
# ===============================
uploaded_file = st.file_uploader("Upload your Sprint CSV File", type=["csv"])

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview Uploaded Data")
    st.dataframe(df.head())

    # ===============================
    # Column Mapping (Fully Flexible)
    # ===============================
    st.subheader("Map Your Columns (Flexible)")

    columns = df.columns.tolist()

    # Ticket / Task ID
    ticket_col = st.selectbox(
        "Select Ticket/Task ID Column",
        columns,
        index=0 if len(columns) > 0 else -1
    )

    # Update / Description Column
    text_col = st.selectbox(
        "Select Update Text Column",
        columns,
        index=1 if len(columns) > 1 else 0
    )

    # Blockers Column (optional, numeric)
    blocker_col = st.selectbox(
        "Select Blockers Column (numeric, optional)",
        ["None"] + columns,
        index=0
    )

    # Progress Column (%) (optional, numeric)
    progress_col = st.selectbox(
        "Select Progress Column (numeric %, optional)",
        ["None"] + columns,
        index=0
    )

    # ===============================
    # Rename Selected Columns
    # ===============================
    df = df.rename(columns={
        ticket_col: "ticket_id",
        text_col: "update_text"
    })

    # Safe numeric conversion
    if blocker_col != "None":
        df["blockers"] = pd.to_numeric(df[blocker_col], errors="coerce").fillna(0)
    else:
        df["blockers"] = 0

    if progress_col != "None":
        df["progress"] = pd.to_numeric(df[progress_col], errors="coerce").fillna(0)
    else:
        df["progress"] = 0

    # ===============================
    # Risk Detection Logic
    # ===============================
    def detect_risk(row):
        blockers = row.get("blockers", 0)
        progress = row.get("progress", 0)

        if blockers > 0 and progress < 50:
            return "High"
        elif blockers > 0 or progress < 50:
            return "Medium"
        else:
            return "Low"

    df["Calculated Risk"] = df.apply(detect_risk, axis=1)

    # ===============================
    # Risk Analysis Table
    # ===============================
    st.subheader("Risk Analysis Results")
    st.dataframe(df)

    # ===============================
    # Risk Distribution Chart
    # ===============================
    st.subheader("Sprint Risk Distribution")

    risk_counts = df["Calculated Risk"].value_counts()
    fig, ax = plt.subplots()
    colors = [
        "red" if r == "High" else
        "orange" if r == "Medium" else
        "green"
        for r in risk_counts.index
    ]
    ax.bar(risk_counts.index, risk_counts.values, color=colors)
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Count")
    ax.set_title("Sprint Risk Distribution")
    st.pyplot(fig)

    # ===============================
    # Metrics Summary
    # ===============================
    total_tasks = len(df)
    high_risk_tasks = (df["Calculated Risk"] == "High").sum()
    medium_risk_tasks = (df["Calculated Risk"] == "Medium").sum()
    low_risk_tasks = (df["Calculated Risk"] == "Low").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("High Risk", high_risk_tasks)
    col3.metric("Medium Risk", medium_risk_tasks)
    col4.metric("Low Risk", low_risk_tasks)

    # Blockers Summary
    total_blockers = df["blockers"].sum()
    st.subheader("Blocker Summary")
    st.metric("Total Blockers", int(total_blockers))

    # Progress Summary
    avg_progress = df["progress"].mean()
    st.subheader("Progress Summary")
    st.metric("Average Progress (%)", round(avg_progress, 1))

    # Sprint Health Score
    health_score = ((low_risk_tasks*1.0 + medium_risk_tasks*0.5 + high_risk_tasks*0.2) / total_tasks) * 100
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

else:
    st.info("Upload a CSV file to begin risk analysis.")