import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


# ── 1. PAGE CONFIGURATION (MUST BE FIRST) ───────────────────────────────────
st.set_page_config(
    page_title="Inventory Calculator",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── 2. CUSTOM CSS STYLING ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main { 
    background: #f8fafc; 
}
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%);
}

/* Hero banner */
.hero-banner {
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    background: rgba(255,255,255,0.75);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #2563eb, #7c3aed, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #475569;
    font-size: 1rem;
    margin-top: 0.5rem;
}

/* Module cards */
.module-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.5rem;
}
.module-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    background: #eff6ff;
}
.module-card.active {
    border-color: #3b82f6;
    background: linear-gradient(135deg, #eff6ff, #eef2ff);
    box-shadow: 0 0 24px rgba(59,130,246,0.15);
}
.module-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.module-name { font-weight: 600; color: #0f172a; font-size: 0.9rem; }
.module-desc { color: #64748b; font-size: 0.75rem; margin-top: 0.2rem; }

/* Result metric cards */
.metric-card {
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-label {
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
}
.metric-unit {
    color: #64748b;
    font-size: 0.75rem;
    margin-top: 0.2rem;
}

/* Formula trace */
.formula-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
.formula-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.85rem;
}
.formula-row:last-child { border-bottom: none; }
.formula-name { color: #2563eb; font-family: monospace; }
.formula-result { color: #059669; font-weight: 600; }

/* Section headers */
.section-header {
    color: #475569;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}

/* Input styling override */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

/* Divider */
hr { border-color: #e2e8f0 !important; }

/* Tabs */
div[data-testid="stTabs"] button {
    color: #64748b !important;
    font-weight: 500 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2563eb !important;
    border-bottom-color: #2563eb !important;
}

/* Expander */
details {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}

/* Multiselect tags */
span[data-testid="stTag"] {
    background: #eff6ff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 20px !important;
}

.stAlert {
    border-radius: 12px !important;
}

/* Hide default streamlit menu bar branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)



# ── 3. HELPER FUNCTIONS ─────────────────────────────────────────────────────


def metric_html(label, value, unit=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>"""


def formula_html(rows):
    inner = "".join(
        f'<div class="formula-row"><span class="formula-name">{n}</span><span class="formula-result">{v}</span></div>'
        for n, v in rows
    )
    return f'<div class="formula-box">{inner}</div>'


def cols_metrics(items, ncols=4):
    cols = st.columns(ncols)
    for i, (label, value, unit) in enumerate(items):
        with cols[i % ncols]:
            st.markdown(metric_html(label, value, unit), unsafe_allow_html=True)


def color_gauge(value, max_val, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#475569", "size": 14}},
        number={"font": {"color": "#0f172a", "size": 28}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#94a3b8"},
            "bar": {"color": color},
            "bgcolor": "#ffffff",
            "bordercolor": "#cbd5e1",
            "steps": [{"range": [0, max_val], "color": "#f8fafc"}],
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
        height=220,
        margin=dict(t=40, b=10, l=20, r=20),
    )
    return fig


def bar_chart(labels, values, colors, title, y_label="Value"):
    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:,.0f}" for v in values],
        textposition="outside",
        textfont={"color": "#0f172a", "size": 13},
    ))
    fig.update_layout(
        title={"text": title, "font": {"color": "#0f172a", "size": 16}, "x": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#475569"},
        yaxis={"title": y_label, "gridcolor": "#e2e8f0", "color": "#64748b"},
        xaxis={"color": "#64748b"},
        height=320,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig


def line_chart(x, y_dict, title, y_label):
    palette = ["#2563eb", "#059669", "#db2777", "#ea580c", "#7c3aed"]
    fig = go.Figure()
    for i, (name, vals) in enumerate(y_dict.items()):
        fig.add_trace(go.Scatter(
            x=x, y=vals, name=name,
            mode="lines+markers",
            line={"color": palette[i % len(palette)], "width": 2.5},
            marker={"size": 7},
        ))
    fig.update_layout(
        title={"text": title, "font": {"color": "#0f172a", "size": 16}, "x": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#475569"},
        yaxis={"title": y_label, "gridcolor": "#e2e8f0", "color": "#64748b"},
        xaxis={"color": "#64748b"},
        legend={"bgcolor": "rgba(0,0,0,0)", "bordercolor": "#cbd5e1"},
        height=340,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig


def hist_chart(data, mean, title):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data, nbinsx=max(5, len(data)//2),
        marker_color="#6366f1", opacity=0.8,
        name="Demand",
    ))
    fig.add_vline(x=mean, line_dash="dash", line_color="#059669",
                  annotation_text=f"μ = {mean:.1f}", annotation_font_color="#059669")
    fig.update_layout(
        title={"text": title, "font": {"color": "#0f172a", "size": 16}, "x": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#475569"},
        yaxis={"title": "Frequency", "gridcolor": "#e2e8f0", "color": "#64748b"},
        xaxis={"title": "Demand (units)", "color": "#64748b"},
        height=300,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig



# ── 4. APP STATE & CONFIGURATION ───────────────────────────────────────────


if "module" not in st.session_state:
    st.session_state.module = None


MODULES = [
    ("📊", "Mean, Variance & SD",  "Demand statistics",     "stats"),
    ("🛡️", "Safety Stock",         "Buffer inventory",      "ss"),
    ("🔄", "Reorder Point",        "When to reorder",       "rop"),
    ("📦", "EOQ",                  "Optimal order qty",     "eoq"),
    ("💰", "Total Cost",           "Full inventory cost",   "tc"),
    ("🎯", "Service Level",        "Stock-out protection",  "sl"),
    ("🚀", "Calculate all",    "Calculate everything",  "all"),
]



# ── 5. HEADER HERO ──────────────────────────────────────────────────────────


st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📦 Inventory Management Calculator</div>
    <div class="hero-sub">Stochastic demand modelling · EOQ · Safety stock · Reorder point · Total cost</div>
</div>
""", unsafe_allow_html=True)



st.markdown('<div class="section-header">Please choose what you want to calculate</div>', unsafe_allow_html=True)



# ── 6. NAVIGATION PANEL ─────────────────────────────────────────────────────


cols = st.columns(7)
for i, (icon, name, desc, mid) in enumerate(MODULES):
    with cols[i]:
        active = st.session_state.module == mid
        border = "border: 2px solid #3b82f6;" if active else ""
        bg = "background: linear-gradient(135deg,#eff6ff,#eef2ff);" if active else ""
        st.markdown(f"""
        <div class="module-card" style="{border}{bg}">
            <div class="module-icon">{icon}</div>
            <div class="module-name">{name}</div>
            <div class="module-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Open", key=f"btn_{mid}", use_container_width=True):
            st.session_state.module = mid
            st.rerun()


st.markdown("---")



# ── 7. CALCULATOR PAGES ─────────────────────────────────────────────────────


mod = st.session_state.module


if mod is None:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 0; color: #64748b;">
        <div style="font-size:3rem; margin-bottom:1rem">👆</div>
        <div style="font-size:1.1rem; font-weight:500; color:#475569">Select a calculator above to begin</div>
        <div style="font-size:0.85rem; margin-top:0.5rem; color:#64748b">Each module calculates a specific inventory formula</div>
    </div>
    """, unsafe_allow_html=True)

# ... keep the rest of your code exactly the same ...

# In the TOTAL COST section, change only this line:
# lead  = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
