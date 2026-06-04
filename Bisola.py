import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# ── 1. APP CONFIGURATION & INITIALIZATION ────────────────────────────────────
st.set_page_config(
    page_title="Inventory Optimization Suite",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# ── 2. BRIGHT & MODERN CUSTOM CSS STYLING ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
}

.hero-banner {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0284c7, #4f46e5, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-sub {
    color: #64748b;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 500;
}

.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.4rem;
}

.module-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.module-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -8px rgba(59, 130, 246, 0.15);
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: transform 0.2s;
}

.metric-card:hover {
    transform: scale(1.02);
}

.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #0f172a;
}

.metric-label {
    font-size: 0.85rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
    font-weight: 600;
}

.metric-unit {
    font-size: 0.8rem;
    color: #2563eb;
    font-weight: 500;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
}

.audit-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
    background: #ffffff;
    border-radius: 8px;
    overflow: hidden;
}

.audit-table th {
    background-color: #f1f5f9;
    color: #0f172a;
    text-align: left;
    padding: 10px;
    font-size: 0.9rem;
    border-bottom: 2px solid #e2e8f0;
}

.audit-table td {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.85rem;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ── 3. HELPER RENDERING FUNCTIONS ───────────────────────────────────────────
def cols_metrics(metric_list, ncols=4):
    cols = st.columns(ncols)
    for idx, (label, val, unit) in enumerate(metric_list):
        with cols[idx % ncols]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

def formula_html(steps):
    html = '<table class="audit-table"><tr><th>Target Identifier</th><th>Calculated Formula Operation Breakdowns</th></tr>'
    for title, formula in steps:
        html += f'<tr><td><b>{title}</b></td><td><code>{formula}</code></td></tr>'
    html += '</table>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
# ── 4. APP STATE & CONFIGURATION ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Mathematical Inventory Optimization Suite</div>
    <div class="hero-sub">Enterprise Multi-Model Supply Chain Parameter Calibrator Engine</div>
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊", "Economic Order Quantity", "Classic Wilson EOQ model", "eoq"),
    ("🛡️", "Safety Stock & ROP",     "Buffer stock optimization", "ss"),
    ("💰", "Total Inventory Cost",    "System cost distribution",  "tc"),
    ("🚀", "Calculate All",            "Calculate everything",      "all")
]

st.sidebar.markdown("### 🗺️ Control Engine")
mod = st.sidebar.radio(
    "Select Optimization Module", 
    [m[3] for m in modules], 
    format_func=lambda x: next(f"{m[0]} {m[1]}" for m in modules if m[3] == x)
)

# ─────────────────────────────────────────────────────────────────────────────
# ── 5. INDIVIDUAL MODULE LOGICS ──────────────────────────────────────────────

# --- MODULE 1: EOQ ---
if mod == "eoq":
    st.markdown("### 📊 Economic Order Quantity (Wilson Framework)")
    st.markdown("Balance procurement transaction costs against asset warehousing holding premiums.")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume (units/yr)", min_value=0.0, value=18250.0, step=100.0)
        S = st.number_input("Ordering Cost per Order (S, ₦)", min_value=0.0, value=5000.0, step=250.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Year (H, ₦)", min_value=0.001, value=20.0, step=1.0)
    
    if st.button("Execute EOQ Optimization"):
        eoq_val = np.sqrt((2 * D * S) / H)
        orders_yr = D / eoq_val
        cycle_time = 365 / orders_yr
        
        cols_metrics([
            ("Economic Order Qty (Q*)", f"{eoq_val:,.1f}", "Units per Order"),
            ("Optimal Orders Frequency", f"{orders_yr:.1f}", "Orders / Year"),
            ("Average Cycle Duration", f"{cycle_time:.1f}", "Days between orders")
        ], ncols=3)

# --- MODULE 2: SAFETY STOCK & ROP ---
elif mod == "ss":
    st.markdown("### 🛡️ Safety Stock & Reorder Point Engine")
    st.markdown("Calculate strategic buffer levels to hedge against stochastic demand during supplier lead periods.")
    
    col1, col2 = st.columns(2)
    with col1:
        mu = st.number_input("Mean Daily Demand (μ)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Daily Demand (σ)", min_value=0.0, value=12.5, step=0.5)
    with col2:
        lead = st.number_input("Lead Time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Desired Service Level (Z-score)", options=[1.28, 1.65, 1.96, 2.33], index=1,
                         format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x])
    
    if st.button("Execute Safety Stock Evaluation"):
        sigma_L = sigma * np.sqrt(lead) if lead > 0 else 0
        ss_val = z * sigma_L
        demand_lt = mu * lead
        rop_val = demand_lt + ss_val
        
        cols_metrics([
            ("Lead Time Sigma", f"{sigma_L:.2f}", "Stochastic Deviation"),
            ("Safety Stock Buffer", f"{ss_val:.1f}", "Strategic Units"),
            ("Reorder Point (ROP)", f"{rop_val:.1f}", "Trigger Inventory Level")
        ], ncols=3)

# --- MODULE 3: TOTAL COST ---
elif mod == "tc":
    st.markdown("### 💰 Total System Inventory Cost Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume", min_value=0.0, value=18250.0, step=100.0)
        Q = st.number_input("Current Order Size Quantity (Q)", min_value=1.0, value=3000.0, step=50.0)
        S = st.number_input("Setup/Ordering Cost (S)", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Yr (H)", min_value=0.0, value=20.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Demand", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
    
    if st.button("Analyze System Cost Distribution"):
        hc = (Q / 2) * H
        oc = (D / Q) * S
        shc = 50.0 * sigma * 0.1 * (D / Q)
        tc_val = hc + oc + shc
        
        cols_metrics([
            ("Holding Premium", f"₦{hc:,.2f}", "Carrying Cost"),
            ("Ordering Overhead", f"₦{oc:,.2f}", "Procurement Cost"),
            ("Shortage Exposure", f"₦{shc:,.2f}", "Risk Cost"),
            ("Total Combined Cost", f"₦{tc_val:,.2f}", "Annual Matrix")
        ], ncols=4)

# --- MODULE 4: CALCULATE ALL MASTER ---
elif mod == "all":
    st.markdown("### 🚀 Calculate All")
    st.markdown("Enter all your core thresholds below to evaluate every single inventory metric at once.")

    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        mu_all    = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Std deviation (σ)",     min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with icol2:
        lead_all  = st.number_input("Lead time (days, L)",   min_value=0,   value=5,    step=1,   key="all_lead")
        z_all     = st.selectbox("Service level",            options=[1.28, 1.65, 1.96, 2.33], index=1,
                                 format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x], key="all_z")
    with icol3:
        S_all     = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all     = st.number_input("Holding cost per unit/yr (₦)",min_value=0.0, value=20.0,  step=1.0,  key="all_H")
        SC_all    = st.number_input("Shortage cost per unit (₦)",  min_value=0.0, value=50.0,  step=1.0,  key="all_SC")

    calculate_all = st.button("Run Master Calculation", key="calc_all_run")

    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            D_all = mu_all * 365
            sigma_L_all = sigma_all * np.sqrt(lead_all) if lead_all > 0 else 0
            ss_all = z_all * sigma_L_all
            demand_during_lt_all = mu_all * lead_all
            rop_all = demand_during_lt_all + ss_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all
            hc_all = (eoq_all / 2) * H_all
            oc_all = orders_all * S_all
            shc_all = SC_all * sigma_all * 0.1 * orders_all
            tc_all = hc_all + oc_all + shc_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]

            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Economic Order Qty", f"{eoq_all:,.0f}", "units/order"),
                ("Safety Stock (SS)",  f"{ss_all:.1f}",   "units Buffer"),
                ("Reorder Point (ROP)",f"{rop_all:.1f}",  "inventory scale"),
                ("Total Annual Cost",  f"₦{tc_all:,.0f}", "combined system"),
            ], ncols=4)

            st.markdown('<div class="section-header">Operations Framework Breakdown</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Annual Demand Volume", f"{D_all:,.0f}",       "units/year"),
                ("Orders Placed",        f"{orders_all:.1f}",   "times/year"),
                ("Lead Time Demand",     f"{demand_during_lt_all:.1f}", "units"),
                ("Cycle Service Level",  f"{pct_all}%",         f"z={z_all}"),
            ], ncols=4)

            st.markdown('<div class="section-header">System Optimization Visualizations</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                q_range = np.linspace(eoq_all * 0.2, eoq_all * 3, 200)
                hc_line = (q_range / 2) * H_all
                oc_line = (D_all / q_range) * S_all
                tc_line = hc_line + oc_line + (SC_all * sigma_all * 0.1 * (D_all / q_range))
                fig_all = go.Figure()
                fig_all.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color":"#4f46e5","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color":"#ec4899","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total system", line={"color":"#10b981","width":3}, mode="lines"))
                fig_all.add_vline(x=eoq_all, line_dash="dash", line_color="#3b82f6", annotation_text=f"EOQ={eoq_all:,.0f}", annotation_font_color="#3b82f6")
                fig_all.update_layout(
                    title={"text":"Total Optimization Cost Curves","font":{"color":"#0f172a","size":15}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family":"Inter","color":"#475569"},
                    yaxis={"title":"Cost (₦)","gridcolor":"#e2e8f0","color":"#475569"},
                    xaxis={"title":"Order quantity Thresholds","color":"#475569"},
                    legend={"bgcolor":"rgba(255,255,255,0.8)"},
                    height=320, margin=dict(t=50,b=20,l=20,r=20),
                )
                st.plotly_chart(fig_all, use_container_width=True)
            with c2:
                fig_wf = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during LT", "Safety stock", "Reorder point"],
                    y=[demand_during_lt_all, ss_all, 0],
                    connector={"line": {"color": "#cbd5e1"}},
                    increasing={"marker": {"color": "#10b981"}},
                    totals={"marker": {"color": "#3b82f6"}},
                    text=[f"{demand_during_lt_all:.1f}", f"{ss_all:.1f}", f"{rop_all:.1f}"],
                    textposition="outside",
                    textfont={"color": "#0f172a"},
                ))
                fig_wf.update_layout(
                    title={"text": "Reorder Point (ROP) Structure Balance", "font": {"color": "#0f172a", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"gridcolor": "#e2e8f0", "color": "#475569"},
                    xaxis={"color": "#475569"},
                    height=320, margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_wf, use_container_width=True)

            with st.expander("📖 View Consolidated Formula Audit Trail"):
                st.markdown(formula_html([
                    ("Annual Demand Volume (D)", f"{mu_all} × 365 = {D_all:,.0f} units/yr"),
                    ("EOQ Engine = √(2DS/H)", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                    ("Safety Stock Formula (SS)", f"{z_all} × ({sigma_all} × √{lead_all}) = {ss_all:.1f} units"),
                    ("Reorder Point Target (ROP)", f"{demand_during_lt_all:.1f} + {ss_all:.1f} = {rop_all:.1f} units"),
                    ("Consolidated Cost Matrix", f"HC (₦{hc_all:,.0f}) + OC (₦{oc_all:,.0f}) + SC (₦{shc_all:,.0f}) = ₦{tc_all:,.0f}/yr")
                ]), unsafe_allow_html=True)
    else:
        st.info("👈 Complete the global parameter values and click **Run Master Calculation** to get an instant snapshot of your entire optimization portfolio.")    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0284c7, #4f46e5, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #64748b;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* Form Sections Dividers */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.4rem;
}

/* Clean Interactive Sidebar/Module Cards */
.module-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.module-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -8px rgba(59, 130, 246, 0.15);
}

/* Beautiful High-Contrast Metric Result Display Panels */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: scale(1.02);
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #0f172a;
}
.metric-label {
    font-size: 0.85rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
    font-weight: 600;
}
.metric-unit {
    font-size: 0.8rem;
    color: #2563eb;
    font-weight: 500;
}

/* Input Fields Adjustments */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

/* Vibrant Royal Blue Action Trigger Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
}

/* Audit Logs HTML Tables */
.audit-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
    background: #ffffff;
    border-radius: 8px;
    overflow: hidden;
}
.audit-table th {
    background-color: #f1f5f9;
    color: #0f172a;
    text-align: left;
    padding: 10px;
    font-size: 0.9rem;
    border-bottom: 2px solid #e2e8f0;
}
.audit-table td {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.85rem;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ── 3. HELPER RENDERING FUNCTIONS ───────────────────────────────────────────
def cols_metrics(metric_list, ncols=4):
    cols = st.columns(ncols)
    for idx, (label, val, unit) in enumerate(metric_list):
        with cols[idx % ncols]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

def formula_html(steps):
    html = '<table class="audit-table"><tr><th>Target Identifier</th><th>Calculated Formula Operation Breakdowns</th></tr>'
    for title, formula in steps:
        html += f'<tr><td><b>{title}</b></td><td><code>{formula}</code></td></tr>'
    html += '</table>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
# ── 4. APP STATE & CONFIGURATION ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Mathematical Inventory Optimization Suite</div>
    <div class="hero-sub">Enterprise Multi-Model Supply Chain Parameter Calibrator Engine</div>
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊", "Economic Order Quantity", "Classic Wilson EOQ model", "eoq"),
    ("🛡️", "Safety Stock & ROP",     "Buffer stock optimization", "ss"),
    ("💰", "Total Inventory Cost",    "System cost distribution",  "tc"),
    ("🚀", "Calculate All",            "Calculate everything",      "all")
]

st.sidebar.markdown("### 🗺️ Control Engine")
mod = st.sidebar.radio(
    "Select Optimization Module", 
    [m[3] for m in modules], 
    format_func=lambda x: next(f"{m[0]} {m[1]}" for m in modules if m[3] == x)
)

# ─────────────────────────────────────────────────────────────────────────────
# ── 5. INDIVIDUAL MODULE LOGICS ──────────────────────────────────────────────

# --- MODULE 1: EOQ ---
if mod == "eoq":
    st.markdown("### 📊 Economic Order Quantity (Wilson Framework)")
    st.markdown("Balance procurement transaction costs against asset warehousing holding premiums.")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume (units/yr)", min_value=0.0, value=18250.0, step=100.0)
        S = st.number_input("Ordering Cost per Order (S, ₦)", min_value=0.0, value=5000.0, step=250.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Year (H, ₦)", min_value=0.001, value=20.0, step=1.0)
    
    if st.button("Execute EOQ Optimization"):
        eoq_val = np.sqrt((2 * D * S) / H)
        orders_yr = D / eoq_val
        cycle_time = 365 / orders_yr
        
        cols_metrics([
            ("Economic Order Qty (Q*)", f"{eoq_val:,.1f}", "Units per Order"),
            ("Optimal Orders Frequency", f"{orders_yr:.1f}", "Orders / Year"),
            ("Average Cycle Duration", f"{cycle_time:.1f}", "Days between orders")
        ], ncols=3)

# --- MODULE 2: SAFETY STOCK & ROP ---
elif mod == "ss":
    st.markdown("### 🛡️ Safety Stock & Reorder Point Engine")
    st.markdown("Calculate strategic buffer levels to hedge against stochastic demand during supplier lead periods.")
    
    col1, col2 = st.columns(2)
    with col1:
        mu = st.number_input("Mean Daily Demand (μ)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Daily Demand (σ)", min_value=0.0, value=12.5, step=0.5)
    with col2:
        lead = st.number_input("Lead Time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Desired Service Level (Z-score)", options=[1.28, 1.65, 1.96, 2.33], index=1,
                         format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x])
    
    if st.button("Execute Safety Stock Evaluation"):
        sigma_L = sigma * np.sqrt(lead) if lead > 0 else 0
        ss_val = z * sigma_L
        demand_lt = mu * lead
        rop_val = demand_lt + ss_val
        
        cols_metrics([
            ("Lead Time Sigma", f"{sigma_L:.2f}", "Stochastic Deviation"),
            ("Safety Stock Buffer", f"{ss_val:.1f}", "Strategic Units"),
            ("Reorder Point (ROP)", f"{rop_val:.1f}", "Trigger Inventory Level")
        ], ncols=3)

# --- MODULE 3: TOTAL COST ---
elif mod == "tc":
    st.markdown("### 💰 Total System Inventory Cost Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume", min_value=0.0, value=18250.0, step=100.0)
        Q = st.number_input("Current Order Size Quantity (Q)", min_value=1.0, value=3000.0, step=50.0)
        S = st.number_input("Setup/Ordering Cost (S)", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Yr (H)", min_value=0.0, value=20.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Demand", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
    
    if st.button("Analyze System Cost Distribution"):
        hc = (Q / 2) * H
        oc = (D / Q) * S
        shc = 50.0 * sigma * 0.1 * (D / Q)
        tc_val = hc + oc + shc
        
        cols_metrics([
            ("Holding Premium", f"₦{hc:,.2f}", "Carrying Cost"),
            ("Ordering Overhead", f"₦{oc:,.2f}", "Procurement Cost"),
            ("Shortage Exposure", f"₦{shc:,.2f}", "Risk Cost"),
            ("Total Combined Cost", f"₦{tc_val:,.2f}", "Annual Matrix")
        ], ncols=4)

# --- MODULE 4: CALCULATE ALL MASTER ---
elif mod == "all":
    st.markdown("### 🚀 Calculate All")
    st.markdown("Enter all your core thresholds below to evaluate every single inventory metric at once.")

    # Input Fields Grid Split
    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        mu_all    = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Std deviation (σ)",     min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with icol2:
        lead_all  = st.number_input("Lead time (days, L)",   min_value=0,   value=5,    step=1,   key="all_lead")
        z_all     = st.selectbox("Service level",            options=[1.28, 1.65, 1.96, 2.33], index=1,
                                 format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x], key="all_z")
    with icol3:
        S_all     = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all     = st.number_input("Holding cost per unit/yr (₦)",min_value=0.0, value=20.0,  step=1.0,  key="all_H")
        SC_all    = st.number_input("Shortage cost per unit (₦)",  min_value=0.0, value=50.0,  step=1.0,  key="all_SC")

    calculate_all = st.button("Run Master Calculation", key="calc_all_run")

    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            # 1. Master Logic Compilations
            D_all = mu_all * 365
            sigma_L_all = sigma_all * np.sqrt(lead_all) if lead_all > 0 else 0
            ss_all = z_all * sigma_L_all
            demand_during_lt_all = mu_all * lead_all
            rop_all = demand_during_lt_all + ss_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all
            hc_all = (eoq_all / 2) * H_all
            oc_all = orders_all * S_all
            shc_all = SC_all * sigma_all * 0.1 * orders_all
            tc_all = hc_all + oc_all + shc_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]

            # 2. Primary Outputs Visual Panel
            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Economic Order Qty", f"{eoq_all:,.0f}", "units/order"),
                ("Safety Stock (SS)",  f"{ss_all:.1f}",   "units Buffer"),
                ("Reorder Point (ROP)",f"{rop_all:.1f}",  "inventory scale"),
                ("Total Annual Cost",  f"₦{tc_all:,.0f}", "combined system"),
            ], ncols=4)

            # 3. Operations Support Panel
            st.markdown('<div class="section-header">Operations Framework Breakdown</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Annual Demand Volume", f"{D_all:,.0f}",       "units/year"),
                ("Orders Placed",        f"{orders_all:.1f}",   "times/year"),
                ("Lead Time Demand",     f"{demand_during_lt_all:.1f}", "units"),
                ("Cycle Service Level",  f"{pct_all}%",         f"z={z_all}"),
            ], ncols=4)

            # 4. Merged Master Visualization Graphics
            st.markdown('<div class="section-header">System Optimization Visualizations</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                # Continuous Optimization Cost Curves
                q_range = np.linspace(eoq_all * 0.2, eoq_all * 3, 200)
                hc_line = (q_range / 2) * H_all
                oc_line = (D_all / q_range) * S_all
                tc_line = hc_line + oc_line + (SC_all * sigma_all * 0.1 * (D_all / q_range))
                fig_all = go.Figure()
                fig_all.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color":"#4f46e5","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color":"#ec4899","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total system", line={"color":"#10b981","width":3}, mode="lines"))
                fig_all.add_vline(x=eoq_all, line_dash="dash", line_color="#3b82f6", annotation_text=f"EOQ={eoq_all:,.0f}", annotation_font_color="#3b82f6")
                fig_all.update_layout(
                    title={"text":"Total Optimization Cost Curves","font":{"color":"#0f172a","size":15}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family":"Inter","color":"#475569"},
                    yaxis={"title":"Cost (₦)","gridcolor":"#e2e8f0","color":"#475569"},
                    xaxis={"title":"Order quantity Thresholds","color":"#475569"},
                    legend={"bgcolor":"rgba(255,255,255,0.8)"},
                    height=320, margin=dict(t=50,b=20,l=20,r=20),
                )
                st.plotly_chart(fig_all, use_container_width=True)
            with c2:
                # Cascade Waterfall ROP
                fig_wf = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during LT", "Safety stock", "Reorder point"],
                    y=[demand_during_lt_all, ss_all, 0],
                    connector={"line": {"color": "#cbd5e1"}},
                    increasing={"marker": {"color": "#10b981"}},
                    totals={"marker": {"color": "#3b82f6"}},
                    text=[f"{demand_during_lt_all:.1f}", f"{ss_all:.1f}", f"{rop_all:.1f}"],
                    textposition="outside",
                    textfont={"color": "#0f172a"},
                ))
                fig_wf.update_layout(
                    title={"text": "Reorder Point (ROP) Structure Balance", "font": {"color": "#0f172a", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"gridcolor": "#e2e8f0", "color": "#475569"},
                    xaxis={"color": "#475569"},
                    height=320, margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_wf, use_container_width=True)

            # 5. Dropdown Audit Trail formulas 
            with st.expander("📖 View Consolidated Formula Audit Trail"):
                st.markdown(formula_html([
                    ("Annual Demand Volume (D)", f"{mu_all} × 365 = {D_all:,.0f} units/yr"),
                    ("EOQ Engine = √(2DS/H)", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                    ("Safety Stock Formula (SS)", f"{z_all} × ({sigma_all} × √{lead_all}) = {ss_all:.1f} units"),
                    ("Reorder Point Target (ROP)", f"{demand_during_lt_all:.1f} + {ss_all:.1f} = {rop_all:.1f} units"),
                    ("Consolidated Cost Matrix", f"HC (₦{hc_all:,.0f}) + OC (₦{oc_all:,.0f}) + SC (₦{shc_all:,.0f}) = ₦{tc_all:,.0f}/yr")
                ]), unsafe_allow_html=True)
    else:
        st.info("👈 Complete the global parameter values and click **Run Master Calculation** to get an instant snapshot of your entire optimization portfolio.")    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0284c7, #4f46e5, #059669);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #64748b;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* Form Sections Dividers */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.4rem;
}

/* Clean Interactive Sidebar/Module Cards */
.module-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.module-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -8px rgba(59, 130, 246, 0.15);
}

/* Beautiful High-Contrast Metric Result Display Panels */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: scale(1.02);
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #0f172a;
}
.metric-label {
    font-size: 0.85rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
    font-weight: 600;
}
.metric-unit {
    font-size: 0.8rem;
    color: #2563eb;
    font-weight: 500;
}

/* Input Fields Adjustments */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

/* Vibrant Royal Blue Action Trigger Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
}

/* Audit Logs HTML Tables */
.audit-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
    background: #ffffff;
    border-radius: 8px;
    overflow: hidden;
}
.audit-table th {
    background-color: #f1f5f9;
    color: #0f172a;
    text-align: left;
    padding: 10px;
    font-size: 0.9rem;
    border-bottom: 2px solid #e2e8f0;
}
.audit-table td {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.85rem;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ── 3. HELPER RENDERING FUNCTIONS ───────────────────────────────────────────
def cols_metrics(metric_list, ncols=4):
    cols = st.columns(ncols)
    for idx, (label, val, unit) in enumerate(metric_list):
        with cols[idx % ncols]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

def formula_html(steps):
    html = '<table class="audit-table"><tr><th>Target Identifier</th><th>Calculated Formula Operation Breakdowns</th></tr>'
    for title, formula in steps:
        html += f'<tr><td><b>{title}</b></td><td><code>{formula}</code></td></tr>'
    html += '</table>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
# ── 4. APP STATE & CONFIGURATION ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Mathematical Inventory Optimization Suite</div>
    <div class="hero-sub">Enterprise Multi-Model Supply Chain Parameter Calibrator Engine</div>
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊", "Economic Order Quantity", "Classic Wilson EOQ model", "eoq"),
    ("🛡️", "Safety Stock & ROP",     "Buffer stock optimization", "ss"),
    ("💰", "Total Inventory Cost",    "System cost distribution",  "tc"),
    ("🚀", "Calculate All",            "Calculate everything",      "all")
]

st.sidebar.markdown("### 🗺️ Control Engine")
mod = st.sidebar.radio(
    "Select Optimization Module", 
    [m[3] for m in modules], 
    format_func=lambda x: next(f"{m[0]} {m[1]}" for m in modules if m[3] == x)
)

# ─────────────────────────────────────────────────────────────────────────────
# ── 5. INDIVIDUAL MODULE LOGICS ──────────────────────────────────────────────

# --- MODULE 1: EOQ ---
if mod == "eoq":
    st.markdown("### 📊 Economic Order Quantity (Wilson Framework)")
    st.markdown("Balance procurement transaction costs against asset warehousing holding premiums.")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume (units/yr)", min_value=0.0, value=18250.0, step=100.0)
        S = st.number_input("Ordering Cost per Order (S, ₦)", min_value=0.0, value=5000.0, step=250.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Year (H, ₦)", min_value=0.001, value=20.0, step=1.0)
    
    if st.button("Execute EOQ Optimization"):
        eoq_val = np.sqrt((2 * D * S) / H)
        orders_yr = D / eoq_val
        cycle_time = 365 / orders_yr
        
        cols_metrics([
            ("Economic Order Qty (Q*)", f"{eoq_val:,.1f}", "Units per Order"),
            ("Optimal Orders Frequency", f"{orders_yr:.1f}", "Orders / Year"),
            ("Average Cycle Duration", f"{cycle_time:.1f}", "Days between orders")
        ], ncols=3)

# --- MODULE 2: SAFETY STOCK & ROP ---
elif mod == "ss":
    st.markdown("### 🛡️ Safety Stock & Reorder Point Engine")
    st.markdown("Calculate strategic buffer levels to hedge against stochastic demand during supplier lead periods.")
    
    col1, col2 = st.columns(2)
    with col1:
        mu = st.number_input("Mean Daily Demand (μ)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Daily Demand (σ)", min_value=0.0, value=12.5, step=0.5)
    with col2:
        lead = st.number_input("Lead Time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Desired Service Level (Z-score)", options=[1.28, 1.65, 1.96, 2.33], index=1,
                         format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x])
    
    if st.button("Execute Safety Stock Evaluation"):
        sigma_L = sigma * np.sqrt(lead) if lead > 0 else 0
        ss_val = z * sigma_L
        demand_lt = mu * lead
        rop_val = demand_lt + ss_val
        
        cols_metrics([
            ("Lead Time Sigma", f"{sigma_L:.2f}", "Stochastic Deviation"),
            ("Safety Stock Buffer", f"{ss_val:.1f}", "Strategic Units"),
            ("Reorder Point (ROP)", f"{rop_val:.1f}", "Trigger Inventory Level")
        ], ncols=3)

# --- MODULE 3: TOTAL COST ---
elif mod == "tc":
    st.markdown("### 💰 Total System Inventory Cost Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume", min_value=0.0, value=18250.0, step=100.0)
        Q = st.number_input("Current Order Size Quantity (Q)", min_value=1.0, value=3000.0, step=50.0)
        S = st.number_input("Setup/Ordering Cost (S)", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Yr (H)", min_value=0.0, value=20.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Demand", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
    
    if st.button("Analyze System Cost Distribution"):
        hc = (Q / 2) * H
        oc = (D / Q) * S
        shc = 50.0 * sigma * 0.1 * (D / Q)
        tc_val = hc + oc + shc
        
        cols_metrics([
            ("Holding Premium", f"₦{hc:,.2f}", "Carrying Cost"),
            ("Ordering Overhead", f"₦{oc:,.2f}", "Procurement Cost"),
            ("Shortage Exposure", f"₦{shc:,.2f}", "Risk Cost"),
            ("Total Combined Cost", f"₦{tc_val:,.2f}", "Annual Matrix")
        ], ncols=4)

# --- MODULE 4: CALCULATE ALL MASTER ---
elif mod == "all":
    st.markdown("### 🚀 Calculate All")
    st.markdown("Enter all your core thresholds below to evaluate every single inventory metric at once.")

    # Input Fields Grid Split
    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        mu_all    = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Std deviation (σ)",     min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with icol2:
        lead_all  = st.number_input("Lead time (days, L)",   min_value=0,   value=5,    step=1,   key="all_lead")
        z_all     = st.selectbox("Service level",            options=[1.28, 1.65, 1.96, 2.33], index=1,
                                 format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x], key="all_z")
    with icol3:
        S_all     = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all     = st.number_input("Holding cost per unit/yr (₦)",min_value=0.0, value=20.0,  step=1.0,  key="all_H")
        SC_all    = st.number_input("Shortage cost per unit (₦)",  min_value=0.0, value=50.0,  step=1.0,  key="all_SC")

    calculate_all = st.button("Run Master Calculation", key="calc_all_run")

    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            # 1. Master Logic Compilations
            D_all = mu_all * 365
            sigma_L_all = sigma_all * np.sqrt(lead_all) if lead_all > 0 else 0
            ss_all = z_all * sigma_L_all
            demand_during_lt_all = mu_all * lead_all
            rop_all = demand_during_lt_all + ss_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all
            hc_all = (eoq_all / 2) * H_all
            oc_all = orders_all * S_all
            shc_all = SC_all * sigma_all * 0.1 * orders_all
            tc_all = hc_all + oc_all + shc_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]

            # 2. Primary Outputs Visual Panel
            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Economic Order Qty", f"{eoq_all:,.0f}", "units/order"),
                ("Safety Stock (SS)",  f"{ss_all:.1f}",   "units Buffer"),
                ("Reorder Point (ROP)",f"{rop_all:.1f}",  "inventory scale"),
                ("Total Annual Cost",  f"₦{tc_all:,.0f}", "combined system"),
            ], ncols=4)

            # 3. Operations Support Panel
            st.markdown('<div class="section-header">Operations Framework Breakdown</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Annual Demand Volume", f"{D_all:,.0f}",       "units/year"),
                ("Orders Placed",        f"{orders_all:.1f}",   "times/year"),
                ("Lead Time Demand",     f"{demand_during_lt_all:.1f}", "units"),
                ("Cycle Service Level",  f"{pct_all}%",         f"z={z_all}"),
            ], ncols=4)

            # 4. Merged Master Visualization Graphics
            st.markdown('<div class="section-header">System Optimization Visualizations</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                # Continuous Optimization Cost Curves
                q_range = np.linspace(eoq_all * 0.2, eoq_all * 3, 200)
                hc_line = (q_range / 2) * H_all
                oc_line = (D_all / q_range) * S_all
                tc_line = hc_line + oc_line + (SC_all * sigma_all * 0.1 * (D_all / q_range))
                fig_all = go.Figure()
                fig_all.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color":"#4f46e5","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color":"#ec4899","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total system", line={"color":"#10b981","width":3}, mode="lines"))
                fig_all.add_vline(x=eoq_all, line_dash="dash", line_color="#3b82f6", annotation_text=f"EOQ={eoq_all:,.0f}", annotation_font_color="#3b82f6")
                fig_all.update_layout(
                    title={"text":"Total Optimization Cost Curves","font":{"color":"#0f172a","size":15}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family":"Inter","color":"#475569"},
                    yaxis={"title":"Cost (₦)","gridcolor":"#e2e8f0","color":"#475569"},
                    xaxis={"title":"Order quantity Thresholds","color":"#475569"},
                    legend={"bgcolor":"rgba(255,255,255,0.8)"},
                    height=320, margin=dict(t=50,b=20,l=20,r=20),
                )
                st.plotly_chart(fig_all, use_container_width=True)
            with c2:
                # Cascade Waterfall ROP
                fig_wf = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during LT", "Safety stock", "Reorder point"],
                    y=[demand_during_lt_all, ss_all, 0],
                    connector={"line": {"color": "#cbd5e1"}},
                    increasing={"marker": {"color": "#10b981"}},
                    totals={"marker": {"color": "#3b82f6"}},
                    text=[f"{demand_during_lt_all:.1f}", f"{ss_all:.1f}", f"{rop_all:.1f}"],
                    textposition="outside",
                    textfont={"color": "#0f172a"},
                ))
                fig_wf.update_layout(
                    title={"text": "Reorder Point (ROP) Structure Balance", "font": {"color": "#0f172a", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"gridcolor": "#e2e8f0", "color": "#475569"},
                    xaxis={"color": "#475569"},
                    height=320, margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_wf, use_container_width=True)

            # 5. Dropdown Audit Trail formulas 
            with st.expander("📖 View Consolidated Formula Audit Trail"):
                st.markdown(formula_html([
                    ("Annual Demand Volume (D)", f"{mu_all} × 365 = {D_all:,.0f} units/yr"),
                    ("EOQ Engine = √(2DS/H)", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                    ("Safety Stock Formula (SS)", f"{z_all} × ({sigma_all} × √{lead_all}) = {ss_all:.1f} units"),
                    ("Reorder Point Target (ROP)", f"{demand_during_lt_all:.1f} + {ss_all:.1f} = {rop_all:.1f} units"),
                    ("Consolidated Cost Matrix", f"HC (₦{hc_all:,.0f}) + OC (₦{oc_all:,.0f}) + SC (₦{shc_all:,.0f}) = ₦{tc_all:,.0f}/yr")
                ]), unsafe_allow_html=True)
    else:
        st.info("👈 Complete the global parameter values and click **Run Master Calculation** to get an instant snapshot of your entire optimization portfolio.")}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    text-shadow: 0 0 30px rgba(129, 140, 248, 0.3);
}
.hero-sub {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.5rem;
}

/* Section Dividers */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 0.4rem;
}

/* Glassmorphism Interactive Module cards */
.module-card {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 0.5rem;
}
.module-card:hover {
    border-color: #38bdf8;
    transform: translateY(-4px);
    background: rgba(56, 189, 248, 0.1);
    box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.2);
}

/* Brilliant Result metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.7));
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #f8fafc;
    text-shadow: 0 2px 10px rgba(255,255,255,0.1);
}
.metric-label {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
}
.metric-unit {
    font-size: 0.8rem;
    color: #38bdf8;
}

/* Input Fields Styling */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}

/* Electric Pulsing Call to Action Button */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    width: 100%;
}
div[data-testid="stButton"] button:hover {
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    transform: scale(1.01);
}

/* Audit Logs HTML Tables */
.audit-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
}
.audit-table th {
    background-color: rgba(15, 23, 42, 0.6);
    color: #38bdf8;
    text-align: left;
    padding: 8px;
    font-size: 0.9rem;
    border-bottom: 2px solid rgba(255,255,255,0.1);
}
.audit-table td {
    padding: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.85rem;
    color: #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# ── 3. HELPER RENDERING FUNCTIONS ───────────────────────────────────────────
def cols_metrics(metric_list, ncols=4):
    cols = st.columns(ncols)
    for idx, (label, val, unit) in enumerate(metric_list):
        with cols[idx % ncols]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

def formula_html(steps):
    html = '<table class="audit-table"><tr><th>Target Identifier</th><th>Calculated Formula Operation Breakdowns</th></tr>'
    for title, formula in steps:
        html += f'<tr><td><b>{title}</b></td><td><code>{formula}</code></td></tr>'
    html += '</table>'
    return html

# ── 4. APP STATE & CONFIGURATION ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Mathematical Inventory Optimization Suite</div>
    <div class="hero-sub">Enterprise Multi-Model Supply Chain Parameter Calibrator Engine</div>
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊", "Economic Order Quantity", "Classic Wilson EOQ model", "eoq"),
    ("🛡️", "Safety Stock & ROP",     "Buffer stock optimization", "ss"),
    ("💰", "Total Inventory Cost",    "System cost distribution",  "tc"),
    ("🚀", "Calculate All",            "Calculate everything",      "all")
]

# Sidebar navigation
st.sidebar.markdown("### 🗺️ Control Engine")
mod = st.sidebar.radio("Select Optimization Module", [m[3] for m in modules], 
                       format_func=lambda x: next(f"{m[0]} {m[1]}" for m in modules if m[3] == x))

# ── 5. MODULE IMPLEMENTATIONS ────────────────────────────────────────────────

# 📊 MODULE: EOQ
if mod == "eoq":
    st.markdown("### 📊 Economic Order Quantity (Wilson Framework)")
    st.markdown("Balance procurement transaction costs against asset warehousing holding premiums.")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume (units/yr)", min_value=0.0, value=18250.0, step=100.0)
        S = st.number_input("Ordering Cost per Order (S, ₦)", min_value=0.0, value=5000.0, step=250.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Year (H, ₦)", min_value=0.001, value=20.0, step=1.0)
    
    if st.button("Execute EOQ Optimization"):
        eoq_val = np.sqrt((2 * D * S) / H)
        orders_yr = D / eoq_val
        cycle_time = 365 / orders_yr
        
        cols_metrics([
            ("Economic Order Qty (Q*)", f"{eoq_val:,.1f}", "Units per Order"),
            ("Optimal Orders Frequency", f"{orders_yr:.1f}", "Orders / Year"),
            ("Average Cycle Duration", f"{cycle_time:.1f}", "Days between orders")
        ], ncols=3)

# 🛡️ MODULE: SAFETY STOCK & ROP
elif mod == "ss":
    st.markdown("### 🛡️ Safety Stock & Reorder Point Engine")
    st.markdown("Calculate strategic buffer levels to hedge against stochastic demand during supplier lead periods.")
    
    col1, col2 = st.columns(2)
    with col1:
        mu = st.number_input("Mean Daily Demand (μ)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Daily Demand (σ)", min_value=0.0, value=12.5, step=0.5)
    with col2:
        lead = st.number_input("Lead Time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Desired Service Level (Z-score)", options=[1.28, 1.65, 1.96, 2.33], index=1,
                         format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x])
    
    if st.button("Execute Safety Stock Evaluation"):
        sigma_L = sigma * np.sqrt(lead) if lead > 0 else 0
        ss_val = z * sigma_L
        demand_lt = mu * lead
        rop_val = demand_lt + ss_val
        
        cols_metrics([
            ("Lead Time Sigma", f"{sigma_L:.2f}", "Stochastic Deviation"),
            ("Safety Stock Buffer", f"{ss_val:.1f}", "Strategic Units"),
            ("Reorder Point (ROP)", f"{rop_val:.1f}", "Trigger Inventory Level")
        ], ncols=3)

# 💰 MODULE: TOTAL COST
elif mod == "tc":
    st.markdown("### 💰 Total System Inventory Cost Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        D = st.number_input("Annual Demand Volume", min_value=0.0, value=18250.0, step=100.0)
        Q = st.number_input("Current Order Size Quantity (Q)", min_value=1.0, value=3000.0, step=50.0)
        S = st.number_input("Setup/Ordering Cost (S)", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        H = st.number_input("Holding Cost per Unit/Yr (H)", min_value=0.0, value=20.0, step=1.0)
        sigma = st.number_input("Standard Deviation of Demand", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
    
    if st.button("Analyze System Cost Distribution"):
        hc = (Q / 2) * H
        oc = (D / Q) * S
        shc = 50.0 * sigma * 0.1 * (D / Q)
        tc_val = hc + oc + shc
        
        cols_metrics([
            ("Holding Premium", f"₦{hc:,.2f}", "Carrying Cost"),
            ("Ordering Overhead", f"₦{oc:,.2f}", "Procurement Cost"),
            ("Shortage Exposure", f"₦{shc:,.2f}", "Risk Cost"),
            ("Total Combined Cost", f"₦{tc_val:,.2f}", "Annual Matrix")
        ], ncols=4)

# 🚀 MODULE: ALL-IN-ONE MASTER COMPONENT
elif mod == "all":
    st.markdown("### 🚀 Calculate All")
    st.markdown("Enter all your core thresholds below to evaluate every single inventory metric at once.")

    # Input Fields Grid Split
    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        mu_all    = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Std deviation (σ)",     min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with icol2:
        lead_all  = st.number_input("Lead time (days, L)",   min_value=0,   value=5,    step=1,   key="all_lead")
        z_all     = st.selectbox("Service level",            options=[1.28, 1.65, 1.96, 2.33], index=1,
                                 format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x], key="all_z")
    with icol3:
        S_all     = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all     = st.number_input("Holding cost per unit/yr (₦)",min_value=0.0, value=20.0,  step=1.0,  key="all_H")
        SC_all    = st.number_input("Shortage cost per unit (₦)",  min_value=0.0, value=50.0,  step=1.0,  key="all_SC")

    calculate_all = st.button("Run Master Calculation", key="calc_all_run")

    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            # 1. Master Logic Compilations
            D_all = mu_all * 365
            sigma_L_all = sigma_all * np.sqrt(lead_all) if lead_all > 0 else 0
            ss_all = z_all * sigma_L_all
            demand_during_lt_all = mu_all * lead_all
            rop_all = demand_during_lt_all + ss_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all
            hc_all = (eoq_all / 2) * H_all
            oc_all = orders_all * S_all
            shc_all = SC_all * sigma_all * 0.1 * orders_all
            tc_all = hc_all + oc_all + shc_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]

            # 2. Primary Outputs Visual Panel
            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Economic Order Qty", f"{eoq_all:,.0f}", "units/order"),
                ("Safety Stock (SS)",  f"{ss_all:.1f}",   "units Buffer"),
                ("Reorder Point (ROP)",f"{rop_all:.1f}",  "inventory scale"),
                ("Total Annual Cost",  f"₦{tc_all:,.0f}", "combined system"),
            ], ncols=4)

            # 3. Operations Support Panel
            st.markdown('<div class="section-header">Operations Framework Breakdown</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Annual Demand Volume", f"{D_all:,.0f}",       "units/year"),
                ("Orders Placed",        f"{orders_all:.1f}",   "times/year"),
                ("Lead Time Demand",     f"{demand_during_lt_all:.1f}", "units"),
                ("Cycle Service Level",  f"{pct_all}%",         f"z={z_all}"),
            ], ncols=4)

            # 4. Merged Master Visualization Graphics
            st.markdown('<div class="section-header">System Optimization Visualizations</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                # Continuous Optimization Cost Curves
                q_range = np.linspace(eoq_all * 0.2, eoq_all * 3, 200)
                hc_line = (q_range / 2) * H_all
                oc_line = (D_all / q_range) * S_all
                tc_line = hc_line + oc_line + (SC_all * sigma_all * 0.1 * (D_all / q_range))
                fig_all = go.Figure()
                fig_all.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color":"#6366f1","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color":"#f472b6","width":2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total system", line={"color":"#34d399","width":3}, mode="lines"))
                fig_all.add_vline(x=eoq_all, line_dash="dash", line_color="#60a5fa", annotation_text=f"EOQ={eoq_all:,.0f}", annotation_font_color="#60a5fa")
                fig_all.update_layout(
                    title={"text":"Total Optimization Cost Curves","font":{"color":"#e2e8f0","size":15}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family":"Inter","color":"#94a3b8"},
                    yaxis={"title":"Cost (₦)","gridcolor":"#1e2235","color":"#64748b"},
                    xaxis={"title":"Order quantity Thresholds","color":"#64748b"},
                    legend={"bgcolor":"rgba(0,0,0,0)"},
                    height=320, margin=dict(t=50,b=20,l=20,r=20),
                )
                st.plotly_chart(fig_all, use_container_width=True)
            with c2:
                # Cascade Waterfall ROP
                fig_wf = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during LT", "Safety stock", "Reorder point"],
                    y=[demand_during_lt_all, ss_all, 0],
                    connector={"line": {"color": "#2d3555"}},
                    increasing={"marker": {"color": "#34d399"}},
                    totals={"marker": {"color": "#60a5fa"}},
                    text=[f"{demand_during_lt_all:.1f}", f"{ss_all:.1f}", f"{rop_all:.1f}"],
                    textposition="outside",
                    textfont={"color": "#e2e8f0"},
                ))
                fig_wf.update_layout(
                    title={"text": "Reorder Point (ROP) Structure Balance", "font": {"color": "#e2e8f0", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#94a3b8"},
                    yaxis={"gridcolor": "#1e2235", "color": "#64748b"},
                    xaxis={"color": "#64748b"},
                    height=320, margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_wf, use_container_width=True)

            # 5. Dropdown Audit Trail formulas 
            with st.expander("📖 View Consolidated Formula Audit Trail"):
                st.markdown(formula_html([
                    ("Annual Demand Volume (D)", f"{mu_all} × 365 = {D_all:,.0f} units/yr"),
                    ("EOQ Engine = √(2DS/H)", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                    ("Safety Stock Formula (SS)", f"{z_all} × ({sigma_all} × √{lead_all}) = {ss_all:.1f} units"),
                    ("Reorder Point Target (ROP)", f"{demand_during_lt_all:.1f} + {ss_all:.1f} = {rop_all:.1f} units"),
                    ("Consolidated Cost Matrix", f"HC (₦{hc_all:,.0f}) + OC (₦{oc_all:,.0f}) + SC (₦{shc_all:,.0f}) = ₦{tc_all:,.0f}/yr")
                ]), unsafe_allow_html=True)
    else:
       st.info("👈 Complete the global parameter values and click **Run Master Calculation** to get an instant snapshot of your entire optimization portfolio.")
