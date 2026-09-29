import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Load professional dashboard CSS
css_path = Path("static/style.css")

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
else:
    st.warning("CSS file not found: assets/style.css")

# Initialize dashboard counters
if "total_analyzed" not in st.session_state:
    st.session_state.total_analyzed = 0

if "high_drift" not in st.session_state:
    st.session_state.high_drift = 0

if "medium_drift" not in st.session_state:
    st.session_state.medium_drift = 0

if "low_drift" not in st.session_state:
    st.session_state.low_drift = 0


# Load AI model
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# Application title
st.title("🛡️ ReqGuard-AI")
st.subheader("AI-Based Requirements Drift Detection System")

st.write(
    "Compare baseline and current software requirements using "
    "AI-based semantic similarity to detect potential requirements drift."
)

st.markdown("---")


# Dashboard placeholder
dashboard_placeholder = st.empty()


# Requirement Analysis
st.header("📋 Requirement Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Baseline Requirement")

    baseline = st.text_area(
        "Original requirement",
        placeholder="Example: The system response time must be less than 2 seconds.",
        height=150
    )

with col2:
    st.subheader("Current Requirement")

    current = st.text_area(
        "Current requirement",
        placeholder="Example: The system response time must be less than 500 milliseconds.",
        height=150
    )


# Analyze button
if st.button("🔍 Analyze Requirement Drift"):

    if not baseline.strip() or not current.strip():

        st.warning(
            "Please enter both the baseline and current requirements."
        )

    else:

        # Generate embeddings
        baseline_embedding = model.encode([baseline])
        current_embedding = model.encode([current])

        # Calculate semantic similarity
        similarity = cosine_similarity(
            baseline_embedding,
            current_embedding
        )[0][0]

        # Calculate drift
        drift_score = 1 - similarity

        # Classify drift
        if drift_score >= 0.40:
            status = "HIGH DRIFT"
        elif drift_score >= 0.20:
            status = "MEDIUM DRIFT"
        else:
            status = "LOW DRIFT"


        # Update dashboard counters
        st.session_state.total_analyzed += 1

        if status == "HIGH DRIFT":
            st.session_state.high_drift += 1

        elif status == "MEDIUM DRIFT":
            st.session_state.medium_drift += 1

        else:
            st.session_state.low_drift += 1


        # Drift Detection
        st.markdown("---")
        st.header("🔍 Drift Detection")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Semantic Similarity",
                f"{similarity * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Drift Score",
                f"{drift_score * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Drift Status",
                status
            )


        # Requirement Comparison
        st.markdown("### Requirement Comparison")

        st.write("**Baseline:**")
        st.write(baseline)

        st.write("**Current:**")
        st.write(current)


        # Impact Analysis
        st.markdown("---")
        st.header("📊 Impact Analysis")

        if drift_score >= 0.40:

            st.warning(
                "Significant semantic change detected. "
                "The following components may require review."
            )

            impacted_components = [
                "Application logic",
                "Database layer",
                "Performance tests",
                "API implementation"
            ]

        elif drift_score >= 0.20:

            st.warning(
                "Moderate semantic change detected."
            )

            impacted_components = [
                "Application logic",
                "Test cases"
            ]

        else:

            st.success(
                "No significant semantic drift detected."
            )

            impacted_components = [
                "Requirement documentation"
            ]


        st.write("**Potentially affected components:**")

        for component in impacted_components:
            st.write(f"• {component}")


        # Drift Report
        st.markdown("---")
        st.header("📄 Drift Report")

        st.write(
            f"**Semantic Similarity:** "
            f"{similarity * 100:.1f}%"
        )

        st.write(
            f"**Drift Score:** "
            f"{drift_score * 100:.1f}%"
        )

        st.write(
            f"**Classification:** {status}"
        )

        st.write(
            f"**Potential Impact:** "
            f"{', '.join(impacted_components)}"
        )

        st.success(
            "Requirement drift analysis completed successfully."
        )


        # Requirement Traceability
        st.markdown("---")
        st.header("🔗 Requirement Traceability")

        st.write("**Baseline Requirement:**")
        st.write(baseline)

        st.write("**Current Requirement:**")
        st.write(current)

        st.write("**Traceability Status:**")
        st.success(
            "Baseline and current requirements are linked for comparison."
        )
        report_text = f"""
ReqGuard-AI Drift Analysis Report

Baseline Requirement:
{baseline}

Current Requirement:
{current}

Semantic Similarity:
{similarity * 100:.1f}%

Drift Score:
{drift_score * 100:.1f}%

Drift Status:
{status}

Potential Impact:
{', '.join(impacted_components)}
"""

        st.download_button(
            "⬇️ Download Drift Report",
            report_text,
            file_name="reqguard_drift_report.txt",
            mime="text/plain"
        )


# Update Dashboard AFTER analysis
with dashboard_placeholder.container():

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Requirements Analyzed",
            st.session_state.total_analyzed
        )

    with col2:
        st.metric(
            "High Drift",
            st.session_state.high_drift
        )

    with col3:
        st.metric(
            "Low/Medium Drift",
            st.session_state.medium_drift
            + st.session_state.low_drift
        )

    st.markdown("### Drift Distribution")

    chart_data = pd.DataFrame(
        {
            "Drift Level": ["High", "Medium", "Low"],
            "Count": [
                st.session_state.high_drift,
                st.session_state.medium_drift,
                st.session_state.low_drift
            ]
        }
    ).set_index("Drift Level")

    st.bar_chart(chart_data)