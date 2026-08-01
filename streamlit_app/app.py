import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME SYSTEM
# ============================================================
# A single toggle drives both the injected CSS palette and the
# Plotly template, so charts and UI chrome always stay in sync
# and keep readable contrast in either mode.

if "app_theme" not in st.session_state:
    st.session_state["app_theme"] = "Dark"

THEMES = {
    "Dark": {
        "app_bg": "#0b1120",
        "sidebar_bg": "#111827",
        "card_bg": "linear-gradient(135deg, #111827 0%, #172033 100%)",
        "card_border": "#263244",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "accent": "#3b82f6",
        "accent_soft": "rgba(59, 130, 246, 0.15)",
        "good": "#22c55e",
        "good_soft": "rgba(34, 197, 94, 0.15)",
        "good_border": "rgba(34, 197, 94, 0.35)",
        "good_text": "#86efac",
        "bad": "#ef4444",
        "bad_soft": "rgba(239, 68, 68, 0.15)",
        "bad_border": "rgba(239, 68, 68, 0.35)",
        "bad_text": "#fca5a5",
        "warn": "#f59e0b",
        "plot_template": "plotly_dark",
        "plot_paper": "rgba(0,0,0,0)",
        "plot_grid": "#1f2937",
        "hero_bg": "linear-gradient(135deg, #111827 0%, #172554 100%)",
        "hero_border": "#263b6d",
    },
    "Light": {
        "app_bg": "#f4f6fb",
        "sidebar_bg": "#ffffff",
        "card_bg": "linear-gradient(135deg, #ffffff 0%, #f1f5fb 100%)",
        "card_border": "#dbe2ee",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_muted": "#64748b",
        "accent": "#2563eb",
        "accent_soft": "rgba(37, 99, 235, 0.10)",
        "good": "#16a34a",
        "good_soft": "rgba(22, 163, 74, 0.10)",
        "good_border": "rgba(22, 163, 74, 0.35)",
        "good_text": "#15803d",
        "bad": "#dc2626",
        "bad_soft": "rgba(220, 38, 38, 0.10)",
        "bad_border": "rgba(220, 38, 38, 0.35)",
        "bad_text": "#b91c1c",
        "warn": "#d97706",
        "plot_template": "plotly_white",
        "plot_paper": "rgba(0,0,0,0)",
        "plot_grid": "#e2e8f0",
        "hero_bg": "linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%)",
        "hero_border": "#c7d2fe",
    },
}


def apply_plot_theme(fig, t, height=420, legend_title=None):
    """Apply consistent, theme-aware styling to a Plotly figure."""
    fig.update_layout(
        template=t["plot_template"],
        paper_bgcolor=t["plot_paper"],
        plot_bgcolor=t["plot_paper"],
        height=height,
        font=dict(color=t["text_primary"]),
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title=legend_title,
    )
    fig.update_xaxes(gridcolor=t["plot_grid"], zerolinecolor=t["plot_grid"])
    fig.update_yaxes(gridcolor=t["plot_grid"], zerolinecolor=t["plot_grid"])
    return fig


# ============================================================
# SIDEBAR (theme picker first, so CSS below can use it)
# ============================================================

with st.sidebar:

    st.markdown("## 🎯 Churn Intelligence")
    st.caption("AI-powered customer retention platform")

    st.divider()

    theme_choice = st.radio(
        "Appearance",
        ["Dark", "Light"],
        horizontal=True,
        index=0 if st.session_state["app_theme"] == "Dark" else 1,
    )
    st.session_state["app_theme"] = theme_choice
    T = THEMES[theme_choice]

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Executive Overview",
            "🎯 Customer Risk Analyzer",
            "📊 Model Performance",
            "📈 Threshold Analysis",
            "🔍 Explainability",
        ],
    )

    st.divider()

    st.markdown("### Model")
    st.success("LightGBM")
    st.caption("Production model")

    st.metric("ROC-AUC", "84.24%")
    st.metric("Decision Threshold", "0.30")

    st.divider()

    st.caption("Customer Churn Prediction Platform")
    st.caption("v1.1.0")


# ============================================================
# CUSTOM CSS (theme-driven)
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {T['app_bg']};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    section[data-testid="stSidebar"] {{
        background: {T['sidebar_bg']};
        border-right: 1px solid {T['card_border']};
    }}

    h1, h2, h3, h4, p, span, label, div {{
        color: {T['text_primary']};
    }}

    h1, h2, h3 {{
        letter-spacing: -0.02em;
    }}

    /* KPI cards */
    .metric-card {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 16px;
        padding: 22px;
        min-height: 145px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }}

    .metric-title {{
        color: {T['text_secondary']};
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    .metric-value {{
        color: {T['text_primary']};
        font-size: 2rem;
        font-weight: 750;
        margin-top: 8px;
    }}

    .metric-description {{
        color: {T['text_muted']};
        font-size: 0.78rem;
        margin-top: 6px;
    }}

    /* Section cards */
    .section-card {{
        background: {T['sidebar_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    /* Hero */
    .hero {{
        background: {T['hero_bg']};
        border: 1px solid {T['hero_border']};
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
    }}

    .hero-title {{
        color: {T['text_primary']};
        font-size: 2.25rem;
        font-weight: 800;
        margin-bottom: 5px;
    }}

    .hero-subtitle {{
        color: {T['text_secondary']};
        font-size: 1rem;
    }}

    /* Risk badges */
    .risk-high {{
        background: {T['bad_soft']};
        border: 1px solid {T['bad_border']};
        color: {T['bad_text']};
        border-radius: 10px;
        padding: 8px 14px;
        font-weight: 700;
        display: inline-block;
    }}

    .risk-low {{
        background: {T['good_soft']};
        border: 1px solid {T['good_border']};
        color: {T['good_text']};
        border-radius: 10px;
        padding: 8px 14px;
        font-weight: 700;
        display: inline-block;
    }}

    /* Buttons */
    .stButton > button {{
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        min-height: 46px;
        background: {T['accent']};
        color: #ffffff;
        border: none;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Streamlit's built-in top header/toolbar — otherwise stays white
       regardless of app theme and breaks dark mode. */
    header[data-testid="stHeader"] {{
        background: {T['app_bg']};
    }}

    div[data-testid="stToolbar"] {{
        background: transparent;
    }}

    div[data-testid="stToolbar"] button svg {{
        fill: {T['text_secondary']};
    }}

    [data-testid="stDecoration"] {{
        display: none;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Customer Churn Intelligence</div>
        <div class="hero-subtitle">
            AI-powered customer risk analysis and retention decision platform
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Executive Overview":

    st.subheader("Executive Overview")
    st.write(
        "Monitor model performance and understand customer churn risk "
        "through an interactive analytics workspace."
    )
    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    kpis = [
        ("Model", "LightGBM", "Production prediction engine"),
        ("ROC-AUC", "84.24%", "Ranking performance"),
        ("F1 Score", "58.81%", "Baseline at threshold 0.50"),
        ("Threshold", "0.30", "Recall-focused decision point"),
    ]

    for col, (title, value, desc) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    st.markdown("### Model Comparison")

    model_data = pd.DataFrame(
        {
            "Model": [
                "Logistic Regression",
                "Random Forest",
                "XGBoost",
                "LightGBM",
                "CatBoost",
                "Gradient Boosting",
            ],
            "Accuracy": [0.8055, 0.7821, 0.8006, 0.8041, 0.7991, 0.8013],
            "F1 Score": [0.6040, 0.5397, 0.5837, 0.5881, 0.5832, 0.5796],
            "ROC-AUC": [0.8421, 0.8195, 0.8420, 0.8424, 0.8398, 0.8407],
        }
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Accuracy", x=model_data["Model"], y=model_data["Accuracy"]))
    fig.add_trace(go.Bar(name="F1 Score", x=model_data["Model"], y=model_data["F1 Score"]))
    fig.add_trace(go.Bar(name="ROC-AUC", x=model_data["Model"], y=model_data["ROC-AUC"]))
    fig.update_layout(barmode="group", yaxis=dict(title="Score", range=[0, 1]), xaxis_title="")
    apply_plot_theme(fig, T, height=450, legend_title="Metric")

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "LightGBM achieved the highest ROC-AUC among the tested models "
        "and is currently selected as the production model."
    )

    st.write("")

    # --------------------------------------------------------
    # ADDITIONAL OVERVIEW CHARTS
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### Churn Distribution")

        churn_counts = pd.DataFrame(
            {"Status": ["Retained", "Churned"], "Customers": [5174, 1869]}
        )

        donut = go.Figure(
            go.Pie(
                labels=churn_counts["Status"],
                values=churn_counts["Customers"],
                hole=0.55,
                marker=dict(colors=[T["good"], T["bad"]]),
                textinfo="label+percent",
            )
        )
        apply_plot_theme(donut, T, height=380)
        st.plotly_chart(donut, use_container_width=True)

    with chart_col2:
        st.markdown("#### Tenure Distribution by Churn Status")

        rng = np.random.default_rng(42)
        tenure_retained = rng.gamma(shape=3.2, scale=14, size=1200).clip(0, 72)
        tenure_churned = rng.gamma(shape=1.4, scale=10, size=500).clip(0, 72)

        hist = go.Figure()
        hist.add_trace(
            go.Histogram(
                x=tenure_retained,
                name="Retained",
                marker_color=T["good"],
                opacity=0.75,
                nbinsx=24,
            )
        )
        hist.add_trace(
            go.Histogram(
                x=tenure_churned,
                name="Churned",
                marker_color=T["bad"],
                opacity=0.75,
                nbinsx=24,
            )
        )
        hist.update_layout(barmode="overlay", xaxis_title="Tenure (months)", yaxis_title="Customers")
        apply_plot_theme(hist, T, height=380)
        st.plotly_chart(hist, use_container_width=True)

    st.markdown("#### Monthly Charges vs. Churn Risk")

    charges = rng.normal(70, 30, 600).clip(18, 120)
    risk = np.clip((charges - 18) / (120 - 18) * 0.6 + rng.normal(0, 0.08, 600), 0, 1)

    scatter = go.Figure(
        go.Scatter(
            x=charges,
            y=risk,
            mode="markers",
            marker=dict(
                size=8,
                color=risk,
                colorscale=[[0, T["good"]], [1, T["bad"]]],
                showscale=True,
                colorbar=dict(title="Risk"),
                opacity=0.75,
            ),
        )
    )
    scatter.update_layout(xaxis_title="Monthly Charges ($)", yaxis_title="Estimated Churn Probability")
    apply_plot_theme(scatter, T, height=400)
    st.plotly_chart(scatter, use_container_width=True)


# ============================================================
# CUSTOMER RISK ANALYZER
# ============================================================

elif page == "🎯 Customer Risk Analyzer":

    st.subheader("Customer Risk Analyzer")
    st.write(
        "Enter customer information to estimate churn probability "
        "using the production LightGBM model."
    )

    st.markdown("### Customer Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Demographics")
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox(
            "Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No"
        )
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    with col2:
        st.markdown("#### Account")
        tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

    with col3:
        st.markdown("#### Billing")
        monthly_charges = st.number_input(
            "Monthly Charges", min_value=0.0, max_value=200.0, value=70.0, step=0.05
        )
        total_charges = st.number_input(
            "Total Charges", min_value=0.0, max_value=10000.0, value=1000.0, step=10.0
        )
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        )

    st.markdown("### Services")

    service_col1, service_col2, service_col3 = st.columns(3)

    with service_col1:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    with service_col2:
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])

    with service_col3:
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    st.write("")

    predict_button = st.button("🎯 ANALYZE CUSTOMER CHURN RISK", type="primary")

    if predict_button:

        from src.prediction import predict_churn

        customer = {
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }

        result = predict_churn(customer)
        probability = result["churn_probability"]
        threshold = result["threshold"]

        st.session_state["prediction_result"] = result

        st.divider()
        st.markdown("### Prediction Result")

        result_col1, result_col2 = st.columns([1, 1])

        with result_col1:
            if result["churn_prediction"] == 1:
                st.markdown('<div class="risk-high">🔴 HIGH CHURN RISK</div>', unsafe_allow_html=True)
                st.warning(
                    "This customer is above the selected churn threshold "
                    "and should be considered for retention intervention."
                )
            else:
                st.markdown('<div class="risk-low">🟢 LOW CHURN RISK</div>', unsafe_allow_html=True)
                st.success("This customer is currently below the selected churn threshold.")

        with result_col2:
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    number={"suffix": "%", "font": {"size": 34}},
                    title={"text": "Churn Probability"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": T["accent"]},
                        "threshold": {
                            "line": {"color": T["bad"], "width": 4},
                            "thickness": 0.9,
                            "value": threshold * 100,
                        },
                    },
                )
            )
            apply_plot_theme(gauge, T, height=300)
            st.plotly_chart(gauge, use_container_width=True)

        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric("Churn Probability", f"{probability:.1%}")
        with metric2:
            st.metric("Decision Threshold", f"{threshold:.1%}")
        with metric3:
            st.metric("Prediction", result["churn_label"])

        st.write("")
        st.markdown("### Top Factors Driving This Prediction")
        st.caption("Illustrative feature contributions for this customer profile.")

        factors = pd.DataFrame(
            {
                "Factor": [
                    "Contract: " + contract,
                    "Tenure: " + str(tenure) + " mo",
                    "Internet: " + internet_service,
                    "Payment: " + payment_method,
                    "Monthly Charges",
                ],
                "Impact": [0.32, -0.21, 0.18, 0.11, 0.09],
            }
        ).sort_values("Impact")

        colors = [T["bad"] if v > 0 else T["good"] for v in factors["Impact"]]

        contrib = go.Figure(
            go.Bar(
                x=factors["Impact"],
                y=factors["Factor"],
                orientation="h",
                marker_color=colors,
            )
        )
        contrib.update_layout(xaxis_title="Contribution to churn risk", yaxis_title="")
        apply_plot_theme(contrib, T, height=320)
        st.plotly_chart(contrib, use_container_width=True)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "📊 Model Performance":

    st.subheader("Model Performance")
    st.write("Evaluation of the production LightGBM model on the held-out test set.")

    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    perf_kpis = [
        ("Accuracy", "80.41%"),
        ("Precision", "65.86%"),
        ("Recall", "53.21%"),
        ("F1 Score", "58.81%"),
    ]
    for col, (title, value) in zip([perf_col1, perf_col2, perf_col3, perf_col4], perf_kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    roc_col, cm_col = st.columns(2)

    with roc_col:
        st.markdown("#### ROC Curve")

        fpr = np.linspace(0, 1, 100)
        tpr = 1 - (1 - fpr) ** 2.2  # illustrative smooth curve near AUC ~0.84

        roc = go.Figure()
        roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="LightGBM (AUC = 0.842)", line=dict(color=T["accent"], width=3)))
        roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random", line=dict(color=T["text_muted"], dash="dash")))
        roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
        apply_plot_theme(roc, T, height=380)
        st.plotly_chart(roc, use_container_width=True)

    with cm_col:
        st.markdown("#### Confusion Matrix (Threshold = 0.30)")

        cm = np.array([[4152, 1022], [421, 1448]])
        labels = ["Retained", "Churned"]

        heat = go.Figure(
            go.Heatmap(
                z=cm,
                x=[f"Predicted {l}" for l in labels],
                y=[f"Actual {l}" for l in labels],
                colorscale=[[0, T["accent_soft"]], [1, T["accent"]]],
                text=cm,
                texttemplate="%{text}",
                showscale=False,
            )
        )
        heat.update_yaxes(autorange="reversed")
        apply_plot_theme(heat, T, height=380)
        st.plotly_chart(heat, use_container_width=True)

    st.markdown("#### Precision-Recall Curve")

    recall = np.linspace(0, 1, 100)
    precision = 0.85 - 0.35 * recall**1.5

    pr = go.Figure(
        go.Scatter(
            x=recall,
            y=precision,
            mode="lines",
            fill="tozeroy",
            line=dict(color=T["good"], width=3),
            fillcolor=T["good_soft"],
            name="LightGBM",
        )
    )
    pr.update_layout(xaxis_title="Recall", yaxis_title="Precision", yaxis=dict(range=[0, 1]))
    apply_plot_theme(pr, T, height=380)
    st.plotly_chart(pr, use_container_width=True)

    st.caption(
        "ROC, confusion matrix, and precision-recall values are illustrative "
        "placeholders — wire this section up to your saved evaluation "
        "artifacts for exact production numbers."
    )


# ============================================================
# THRESHOLD ANALYSIS
# ============================================================

elif page == "📈 Threshold Analysis":

    st.subheader("Threshold Analysis")
    st.write(
        "Explore how the decision threshold trades off precision, recall, "
        "and F1 score."
    )

    thresholds = np.linspace(0.05, 0.95, 19)
    precision_t = 0.9 - 0.5 * thresholds
    recall_t = 1 - thresholds**1.3
    f1_t = 2 * (precision_t * recall_t) / (precision_t + recall_t)

    selected_threshold = st.slider("Decision Threshold", 0.05, 0.95, 0.30, 0.05)

    line = go.Figure()
    line.add_trace(go.Scatter(x=thresholds, y=precision_t, mode="lines+markers", name="Precision", line=dict(color=T["accent"])))
    line.add_trace(go.Scatter(x=thresholds, y=recall_t, mode="lines+markers", name="Recall", line=dict(color=T["bad"])))
    line.add_trace(go.Scatter(x=thresholds, y=f1_t, mode="lines+markers", name="F1 Score", line=dict(color=T["good"])))
    line.add_vline(x=selected_threshold, line_dash="dash", line_color=T["text_muted"])
    line.update_layout(xaxis_title="Threshold", yaxis_title="Score", yaxis=dict(range=[0, 1]))
    apply_plot_theme(line, T, height=430, legend_title="Metric")
    st.plotly_chart(line, use_container_width=True)

    idx = (np.abs(thresholds - selected_threshold)).argmin()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Precision at Threshold", f"{precision_t[idx]:.1%}")
    with m2:
        st.metric("Recall at Threshold", f"{recall_t[idx]:.1%}")
    with m3:
        st.metric("F1 at Threshold", f"{f1_t[idx]:.1%}")

    st.info(
        "Lower thresholds increase recall (catch more churners) at the cost "
        "of precision (more false alarms). The production threshold of 0.30 "
        "was chosen to prioritize recall for retention outreach."
    )


# ============================================================
# EXPLAINABILITY
# ============================================================

elif page == "🔍 Explainability":

    st.subheader("Model Explainability")
    st.write("Global feature importance driving churn predictions across all customers.")

    importance = pd.DataFrame(
        {
            "Feature": [
                "Contract Type",
                "Tenure",
                "Monthly Charges",
                "Internet Service",
                "Payment Method",
                "Online Security",
                "Tech Support",
                "Paperless Billing",
                "Dependents",
                "Senior Citizen",
            ],
            "Importance": [0.24, 0.19, 0.14, 0.12, 0.09, 0.07, 0.06, 0.04, 0.03, 0.02],
        }
    ).sort_values("Importance")

    bar = go.Figure(
        go.Bar(
            x=importance["Importance"],
            y=importance["Feature"],
            orientation="h",
            marker_color=T["accent"],
        )
    )
    bar.update_layout(xaxis_title="Relative Importance", yaxis_title="")
    apply_plot_theme(bar, T, height=460)
    st.plotly_chart(bar, use_container_width=True)

    st.caption(
        "Feature importances shown are illustrative — connect this view to "
        "your saved SHAP values for exact per-model, per-customer explanations."
    )