import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ===============================
# Title
# ===============================

st.title("SprintRisk AI - Sprint Risk Analyzer")

# ===============================
# Show Project Screenshots
# ===============================

st.subheader("Project Overview Screenshots")

col1, col2, col3 = st.columns(3)

img1 = Image.open("Sprint_graph.png")
img2 = Image.open("Sprintrisk_dashboard_streamlit.png")
img3 = Image.open("Streamlit_progress.png")

col1.image(img1, width="stretch", caption="Sprint Graph")
col2.image(img2, width="stretch", caption="Sprint Risk Dashboard")
col3.image(img3, width="stretch", caption="Progress Metrics")

# ===============================
# File Upload
# ===============================

uploaded_file = st.file_uploader(
    "Upload your sprint_updates.csv",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # ===============================
    # Risk Detection Logic
    # ===============================

    def detect_risk(row):

        if row["blockers"] > 0 and row["progress"] < 50:
            return "High"

        elif row["blockers"] > 0:
            return "Medium"

        elif row["progress"] < 50:
            return "Medium"

        else:
            return "Low"

    df["Calculated Risk"] = df.apply(detect_risk, axis=1)

    # ===============================
    # Show Table
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
        "red" if r == "High"
        else "orange" if r == "Medium"
        else "green"
        for r in risk_counts.index
    ]

    ax.bar(
        risk_counts.index,
        risk_counts.values,
        color=colors
    )

    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Count")
    ax.set_title("Sprint Risk Distribution")

    st.pyplot(fig)

    # Optional static image display
    try:
        risk_img = Image.open("risk_distribution.png")
        st.image(
            risk_img,
            caption="Sample Risk Distribution",
            width="stretch"
        )
    except:
        pass

    # ===============================
    # Sprint Summary Metrics
    # ===============================

    total_tasks = len(df)

    high_risk_tasks = len(
        df[df["Calculated Risk"] == "High"]
    )

    medium_risk_tasks = len(
        df[df["Calculated Risk"] == "Medium"]
    )

    low_risk_tasks = len(
        df[df["Calculated Risk"] == "Low"]
    )

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

    st.metric(
        "Total Blockers",
        total_blockers
    )

    # ===============================
    # Progress Summary
    # ===============================

    avg_progress = df["progress"].mean()

    st.subheader("Progress Summary")

    st.metric(
        "Average Progress (%)",
        round(avg_progress, 1)
    )

    # ===============================
    # Sprint Health Score
    # ===============================

    health_score = (
        (low_risk_tasks * 1.0)
        + (medium_risk_tasks * 0.5)
        + (high_risk_tasks * 0.2)
    ) / total_tasks * 100

    st.subheader("Sprint Health Score")

    st.metric(
        "Sprint Health (%)",
        round(health_score, 1)
    )

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
