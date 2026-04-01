import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ===============================
# Title
# ===============================

st.title("SprintRisk AI - Universal Sprint Risk Analyzer")

# ===============================
# Instructions
# ===============================

st.info("""
How to Map Columns:

Ticket ID → Unique task ID (Task ID, Issue ID, Ticket Number)

Update Text → Task description (Summary, Title, Task Name)

Blockers → Number of blockers (optional)

Progress → % completion (optional)

If your dataset does not contain blockers or progress,
default values will be used.
""")

# ===============================
# Show Project Screenshots
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

uploaded_file = st.file_uploader(
    "Upload your CSV File",
    type=["csv"]
)

# ===============================
# Auto-detect Column Suggestions
# ===============================

def suggest_column(columns, keywords):

    for col in columns:
        col_lower = col.lower()

        for key in keywords:
            if key in col_lower:
                return col

    return columns[0]

# ===============================
# Main Logic
# ===============================

if uploaded_file:

    try:

        df = pd.read_csv(uploaded_file)

        st.subheader("Preview Uploaded Data")

        st.dataframe(df.head())

        columns = df.columns.tolist()

        # ===============================
        # Auto Suggestions
        # ===============================

        ticket_default = suggest_column(
            columns,
            ["ticket", "id", "issue"]
        )

        text_default = suggest_column(
            columns,
            ["summary", "task", "title", "description"]
        )

        blocker_default = suggest_column(
            columns,
            ["block", "dependency", "impediment"]
        )

        progress_default = suggest_column(
            columns,
            ["progress", "complete", "%"]
        )

        # ===============================
        # Column Mapping UI
        # ===============================

        st.subheader("Map Your Columns")

        ticket_col = st.selectbox(
            "Select Ticket ID Column",
            columns,
            index=columns.index(ticket_default)
        )

        text_col = st.selectbox(
            "Select Update Text Column",
            columns,
            index=columns.index(text_default)
        )

        blocker_col = st.selectbox(
            "Select Blockers Column (optional)",
            ["None"] + columns
        )

        progress_col = st.selectbox(
            "Select Progress Column (%) (optional)",
            ["None"] + columns
        )

        # ===============================
        # Rename Required Columns
        # ===============================

        df = df.rename(columns={
            ticket_col: "ticket_id",
            text_col: "update_text"
        })

        # ===============================
        # Safe Numeric Handling
        # ===============================

        # Blockers

        if blocker_col != "None":

            df["blockers"] = pd.to_numeric(
                df[blocker_col],
                errors="coerce"
            ).fillna(0)

        else:

            df["blockers"] = 0

            st.warning(
                "No blocker column selected. Using default value = 0."
            )

        # Progress

        if progress_col != "None":

            df["progress"] = pd.to_numeric(
                df[progress_col],
                errors="coerce"
            ).fillna(50)

        else:

            df["progress"] = 50

            st.warning(
                "No progress column selected. Using default value = 50%."
            )

        # ===============================
        # Risk Detection Logic
        # ===============================

        def detect_risk(row):

            if row["blockers"] > 0 and row["progress"] < 50:
                return "High"

            elif row["blockers"] > 0 or row["progress"] < 50:
                return "Medium"

            else:
                return "Low"

        df["Calculated Risk"] = df.apply(
            detect_risk,
            axis=1
        )

        # ===============================
        # Results Table
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

        # ===============================
        # Summary Metrics
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
            int(total_blockers)
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
            (
                low_risk_tasks * 1.0
                + medium_risk_tasks * 0.5
                + high_risk_tasks * 0.2
            )
            / total_tasks
            * 100
        )

        st.subheader("Sprint Health Score")

        st.metric(
            "Sprint Health (%)",
            round(health_score, 1)
        )

        # ===============================
        # Download CSV
        # ===============================

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV with Calculated Risk",
            data=csv,
            file_name="sprint_updates_with_risk.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(
            "Error reading file. Please upload a valid CSV."
        )

else:

    st.info("Upload a CSV file to begin risk analysis.")