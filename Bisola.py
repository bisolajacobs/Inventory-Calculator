import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Inventory Calculator",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%);
}

.main {
    background: transparent;
}

.hero-banner {
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.9);
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
    color: #475569 !important;
    font-size: 1rem;
    margin-top: 0.5rem;
}

.section-header {
    color: #000000 !important;
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    margin-top: 1.3rem;
}

.module-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 1.0rem 0.7rem;
    text-align: center;
    margin-bottom: 0.4rem;
}

.module-icon {
    font-size: 1.6rem;
    margin-bottom: 0.25rem;
}

.module-name {
    color: #000000 !important;
    font-weight: 700;
    font-size: 0.8rem;
    line-height: 1.2;
}

.module-desc {
    color: #000000 !important;
    font-size: 0.68rem;
    margin-top: 0.15rem;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 1rem 0.9rem;
    text-align: center;
}

.metric-label {
    color: #000000 !important;
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.35rem;
}

.metric-value {
    color: #0f172a !important;
    font-size: 1.7rem;
    font-weight: 800;
    line-height: 1.1;
}

.metric-unit {
    color: #475569 !important;
    font-size: 0.74rem;
    margin-top: 0.2rem;
}

.formula-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 1rem 1.1rem;
}

.formula-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.86rem;
}

.formula-row:last-child {
    border-bottom: none;
}

.formula-name {
    color: #000000 !important;
    font-family: monospace;
    font-weight: 700;
}

.formula-result {
    color: #000000 !important;
    font-weight: 700;
    text-align: right;
}

.info-box {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 1rem 1.1rem !important;
    margin-top: 0.55rem !important;
    margin-bottom: 1rem !important;
    color: #000000 !important;
}

.info-box * {
    color: #000000 !important;
    opacity: 1 !important;
}

.info-title {
    color: #000000 !important;
    font-size: 1.03rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.2rem !important;
}

.info-label {
    color: #000000 !important;
    font-size: 0.96rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.4rem !important;
}

.info-text {
    color: #000000 !important;
    font-size: 0.94rem !important;
    line-height: 1.55 !important;
    white-space: pre-wrap !important;
}

h1, h2, h3, h4, h5, h6,
h1 *, h2 *, h3 *, h4 *, h5 *, h6 *,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
    color: #000000 !important;
    opacity: 1 !important;
}

div[data-testid="stNumberInput"] label p,
div[data-testid="stTextInput"] label p,
div[data-testid="stSelectbox"] label p,
div[data-testid="stSlider"] label p,
div[data-testid="stTextArea"] label p {
    color: #000000 !important;
    font-weight: 700 !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100% !important;
}

div[data-testid="stSelectbox"] > div {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    border-radius: 10px !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def metric_html(label, value, unit=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """

def formula_html(rows):
    inner = "".join(
        f'<div class="formula-row"><span class="formula-name">{a}</span><span class="formula-result">{b}</span></div>'
        for a, b in rows
    )
    return f'<div class="formula-box">{inner}</div>'

def info_html(title, label, explanation):
    return f"""
    <div class="info-box">
        <div class="info-title">{title}</div>
        <div class="info-label">{label}</div>
        <div class="info-text">{explanation}</div>
    </div>
    """

def show_metrics(items):
    cols = st.columns(len(items))
    for i, (label, value, unit) in enumerate(items):
        with cols[i]:
            st.markdown(metric_html(label, value, unit), unsafe_allow_html=True)

if "module" not in st.session_state:
    st.session_state.module = None

MODULES = [
    ("📊", "Mean, Variance & SD", "Sales Summary", "stats"),
    ("🛡️", "Safety Stock", "Extra goods kept", "ss"),
    ("🔄", "Reorder Point", "When to buy more", "rop"),
    ("📦", "EOQ", "How much more to buy", "eoq"),
    ("💰", "Total Cost", "Total cost of goods", "tc"),
    ("🎯", "Service Level", "Avoid running out", "sl"),
    ("🚀", "Calculate all", "Calculate everything", "all"),
]

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📦 Inventory Management Calculator</div>
    <div class="hero-sub">Stochastic demand modelling · EOQ · Safety stock · Reorder point · Total cost</div>
</div>
""", unsafe_allow_html=True)

show_help = st.toggle("Show detailed explanations", value=True)

st.markdown('<div class="section-header">Please choose what you want to calculate</div>', unsafe_allow_html=True)

cols = st.columns(len(MODULES))
for i, (icon, name, desc, mid) in enumerate(MODULES):
    with cols[i]:
        active = st.session_state.module == mid
        st.markdown(f"""
        <div class="module-card" style="border-color:{'#3b82f6' if active else '#cbd5e1'}; background:{'#eff6ff' if active else '#ffffff'};">
            <div class="module-icon">{icon}</div>
            <div class="module-name">{name}</div>
            <div class="module-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open", key=f"btn_{mid}", use_container_width=True):
            st.session_state.module = mid
            st.rerun()

st.markdown("---")
mod = st.session_state.module

if mod is None:
    st.markdown("""
    <div style="text-align:center; padding:4rem 0; color:#475569;">
        <div style="font-size:3rem; margin-bottom:1rem;">👆</div>
        <div style="font-size:1.1rem; font-weight:600; color:#000000;">Select a calculator above to begin</div>
        <div style="font-size:0.9rem; margin-top:0.5rem; color:#000000;">Each module calculates a specific inventory formula</div>
    </div>
    """, unsafe_allow_html=True)

elif mod == "stats":
    st.markdown('<h3 style="color:#000000 !important;">Mean, Variance & Standard Deviation</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html(
            "Mean, Variance & Standard Deviation",
            "What these numbers mean",
            """Mean (Average Sales)

Simple meaning:
The average number of items sold in a day.
Example:
If you sold 40, 50, and 60 bags in three days:
Average sales = (40 + 50 + 60) ÷ 3 = 50 bags

Variance (How Different Sales Are)
Simple meaning:
Shows how much sales change from day to day.
Example:
If you sell around 50 bags every day, variance is small.
If some days you sell 20 bags and other days 100 bags, variance is large.

Standard Deviation (Typical Change in Sales)
Simple meaning:
Shows how far sales usually move away from the average.
Think of it as:
Small number = sales are predictable.
Large number = sales go up and down a lot."""
        ), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        raw = st.text_area("Demand values (comma-separated)", value="40, 55, 60, 35, 70, 50, 65, 45, 80, 58, 42, 67", height=120)
        calculate = st.button("Calculate Statistics", key="calc_stats")

    with col2:
        if calculate:
            try:
                data = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if len(data) < 2:
                    st.error("Please enter at least 2 values.")
                else:
                    n = len(data)
                    mean = np.mean(data)
                    variance = np.var(data)
                    std_dev = np.std(data)
                    st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
                    show_metrics([
                        ("Mean", f"{mean:.2f}", "units/day"),
                        ("Variance", f"{variance:.2f}", "units²"),
                        ("Standard deviation", f"{std_dev:.2f}", "units/day"),
                        ("Observations", str(n), "data points"),
                    ])
                    st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
                    sample_str = " + ".join(f"{x:.0f}" for x in data[:4])
                    if n > 4:
                        sample_str += " + ..."
                    st.markdown(formula_html([
                        ("Mean = Σx / n", f"{sample_str} / {n} = {mean:.2f}"),
                        ("Variance = Σ(x−Mean)² / n", f"{variance:.4f}"),
                        ("Standard deviation = √Variance", f"√{variance:.2f} = {std_dev:.2f}"),
                        ("Demand follows", f"N({mean:.2f}, {variance:.2f})"),
                    ]), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error parsing values: {e}")
        else:
            st.info("👈 Enter your demand values and click **Calculate Statistics**")

elif mod == "ss":
    st.markdown('<h3 style="color:#000000 !important;">Safety Stock</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("Safety stocks", "Extra goods kept", "This is the extra inventory you keep aside so you do not run out when demand is higher than expected."), unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        sigma = st.number_input("Standard deviation", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Service level", options=[1.28, 1.65, 1.96, 2.33], index=1, format_func=lambda x: {1.28:"90% (z=1.28)", 1.65:"95% (z=1.65)", 1.96:"97.5% (z=1.96)", 2.33:"99% (z=2.33)"}[x])
        calculate = st.button("Calculate Safety stocks", key="calc_ss")
    with col2:
        if calculate:
            sigma_l = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_l
            pct = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z]
            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            show_metrics([
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("Standard deviation × √Lead time", f"{sigma_l:.2f}", "units"),
                ("Service level", f"{pct}%", ""),
            ])
            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Standard deviation × √lead time", f"{sigma} × √{lead} = {sigma_l:.2f}"),
                ("Safety stocks = z × Standard deviation × √lead time", f"{z} × {sigma_l:.2f} = {safety_stocks:.1f} units"),
            ]), unsafe_allow_html=True)

elif mod == "rop":
    st.markdown('<h3 style="color:#000000 !important;">Reorder Point</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("Reorder point", "When to buy more", "This is the stock level where you should place a new order before you run out."), unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        mu = st.number_input("Mean daily demand", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard deviation", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox("Service level", options=[1.28, 1.65, 1.96, 2.33], index=1, format_func=lambda x: {1.28:"90%", 1.65:"95%", 1.96:"97.5%", 2.33:"99%"}[x], key="rop_sl")
        calculate = st.button("Calculate Reorder point", key="calc_rop")
    with col2:
        if calculate:
            sigma_l = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_l
            demand_during_lead_time = mu * lead
            reorder_point = demand_during_lead_time + safety_stocks
            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            show_metrics([
                ("Reorder point", f"{reorder_point:.1f}", "units"),
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("Demand during lead time", f"{demand_during_lead_time:.1f}", "units"),
            ])
            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Demand during lead time", f"{mu} × {lead} = {demand_during_lead_time:.1f}"),
                ("Safety stocks", f"{z} × ({sigma} × √{lead}) = {safety_stocks:.1f}"),
                ("Reorder point", f"{demand_during_lead_time:.1f} + {safety_stocks:.1f} = {reorder_point:.1f} units"),
            ]), unsafe_allow_html=True)

elif mod == "eoq":
    st.markdown('<h3 style="color:#000000 !important;">Economic Order Quantity</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("Economic order quantity", "How much more to buy", "This is the best amount to order at one time so buying and storing costs stay balanced."), unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        d = st.number_input("Mean daily demand", min_value=0.0, value=50.0, step=1.0)
        S = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0)
        H = st.number_input("Holding cost per unit per year (₦)", min_value=0.0, value=20.0, step=1.0)
        calculate = st.button("Calculate Economic order quantity", key="calc_eoq")
    with col2:
        if calculate and H > 0:
            D = d * 365
            eoq = np.sqrt((2 * D * S) / H)
            orders = D / eoq
            holding_cost = (eoq / 2) * H
            ordering_cost = orders * S
            total_cost = holding_cost + ordering_cost
            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            show_metrics([
                ("Economic order quantity", f"{eoq:,.0f}", "units/order"),
                ("Annual demand", f"{D:,.0f}", "units/year"),
                ("Orders per year", f"{orders:.1f}", "orders"),
                ("Total cost", f"₦{total_cost:,.0f}", ""),
            ])
            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Annual demand", f"{d} × 365 = {D:,.0f}"),
                ("Economic order quantity", f"√(2 × {D:,.0f} × {S:,.0f} / {H}) = {eoq:,.1f}"),
                ("Holding cost", f"({eoq:,.0f} / 2) × {H} = ₦{holding_cost:,.0f}"),
                ("Ordering cost", f"({D:,.0f} / {eoq:,.0f}) × {S:,.0f} = ₦{ordering_cost:,.0f}"),
                ("Total cost", f"₦{holding_cost:,.0f} + ₦{ordering_cost:,.0f} = ₦{total_cost:,.0f}"),
            ]), unsafe_allow_html=True)

elif mod == "tc":
    st.markdown('<h3 style="color:#000000 !important;">Total Cost</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("Total cost of goods", "Total cost of goods", "This combines the cost of storing stock, ordering stock, and shortage losses."), unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        d = st.number_input("Mean daily demand", min_value=0.0, value=50.0, step=1.0)
        S = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0)
        H = st.number_input("Holding cost per unit per year (₦)", min_value=0.0, value=20.0, step=1.0)
        SC = st.number_input("Shortage cost per unit (₦)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Standard deviation", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
        calculate = st.button("Calculate Total cost", key="calc_tc")
    with col2:
        if calculate and H > 0:
            D = d * 365
            eoq = np.sqrt((2 * D * S) / H)
            orders = D / eoq if eoq != 0 else 0
            holding_cost = (eoq / 2) * H
            ordering_cost = orders * S
            shortage_cost = SC * sigma * 0.1 * orders
            total_cost = holding_cost + ordering_cost + shortage_cost
            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            show_metrics([
                ("Holding cost", f"₦{holding_cost:,.0f}", ""),
                ("Ordering cost", f"₦{ordering_cost:,.0f}", ""),
                ("Shortage cost", f"₦{shortage_cost:,.0f}", ""),
                ("Total cost", f"₦{total_cost:,.0f}", ""),
            ])
            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Economic order quantity", f"{eoq:,.0f} units"),
                ("Holding cost", f"₦{holding_cost:,.0f}"),
                ("Ordering cost", f"₦{ordering_cost:,.0f}"),
                ("Shortage cost", f"₦{shortage_cost:,.0f}"),
                ("Total cost", f"₦{total_cost:,.0f}"),
            ]), unsafe_allow_html=True)

elif mod == "sl":
    st.markdown('<h3 style="color:#000000 !important;">Service Level</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("Service level", "Avoid running out", "This shows how well your stock protects you from running out."), unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        z = st.slider("Service level factor (z)", min_value=1.0, max_value=3.0, value=1.65, step=0.01)
        sigma = st.number_input("Standard deviation", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
        calculate = st.button("Calculate Service level", key="calc_sl")
    with col2:
        if calculate:
            sigma_l = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_l
            if z >= 2.33:
                pct = 99
            elif z >= 1.96:
                pct = 97.5
            elif z >= 1.65:
                pct = 95
            else:
                pct = 90
            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            show_metrics([
                ("Service level", f"{pct}%", ""),
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("z factor", f"{z:.2f}", ""),
            ])
            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Safety stocks", f"{z} × ({sigma} × √{lead}) = {safety_stocks:.1f} units"),
                ("Service level", f"≈ {pct}%"),
            ]), unsafe_allow_html=True)

elif mod == "all":
    st.markdown('<h3 style="color:#000000 !important;">Calculate all</h3>', unsafe_allow_html=True)
    if show_help:
        st.markdown(info_html("All-in-one inventory dashboard", "Calculate everything", "Use this section to calculate all the main inventory values together."), unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        mu_all = st.number_input("Mean daily demand", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Standard deviation", min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with col2:
        lead_all = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1, key="all_lead")
        z_all = st.selectbox("Service level", options=[1.28, 1.65, 1.96, 2.33], index=1, format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x], key="all_z")
    with col3:
        S_all = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all = st.number_input("Holding cost per unit per year (₦)", min_value=0.0, value=20.0, step=1.0, key="all_H")
        SC_all = st.number_input("Shortage cost per unit (₦)", min_value=0.0, value=50.0, step=1.0, key="all_SC")
    calculate_all = st.button("Run Master Calculation", key="calc_all_run")
    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            D_all = mu_all * 365
            sigma_l_all = sigma_all * np.sqrt(lead_all)
            safety_stocks_all = z_all * sigma_l_all
            demand_during_lead_time_all = mu_all * lead_all
            reorder_point_all = demand_during_lead_time_all + safety_stocks_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all if eoq_all != 0 else 0
            holding_cost_all = (eoq_all / 2) * H_all
            ordering_cost_all = orders_all * S_all
            shortage_cost_all = SC_all * sigma_all * 0.1 * orders_all
            total_cost_all = holding_cost_all + ordering_cost_all + shortage_cost_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]
            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            show_metrics([
                ("Economic order quantity", f"{eoq_all:,.0f}", "units/order"),
                ("Safety stocks", f"{safety_stocks_all:.1f}", "units"),
                ("Reorder point", f"{reorder_point_all:.1f}", "units"),
                ("Total annual cost", f"₦{total_cost_all:,.0f}", ""),
            ])
            st.markdown('<div class="section-header">Operations Breakdown</div>', unsafe_allow_html=True)
            show_metrics([
                ("Annual demand volume", f"{D_all:,.0f}", "units/year"),
                ("Orders placed", f"{orders_all:.1f}", "times/year"),
                ("Demand during lead time", f"{demand_during_lead_time_all:.1f}", "units"),
                ("Cycle service level", f"{pct_all}%", f"z={z_all}"),
            ])
            st.markdown('<div class="section-header">Formula audit trail</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Annual demand volume", f"{mu_all} × 365 = {D_all:,.0f} units/year"),
                ("Economic order quantity", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                ("Safety stocks", f"{z_all} × ({sigma_all} × √{lead_all}) = {safety_stocks_all:.1f} units"),
                ("Reorder point", f"{demand_during_lead_time_all:.1f} + {safety_stocks_all:.1f} = {reorder_point_all:.1f} units"),
                ("Total cost matrix", f"Holding cost (₦{holding_cost_all:,.0f}) + Ordering cost (₦{ordering_cost_all:,.0f}) + Shortage cost (₦{shortage_cost_all:,.0f}) = ₦{total_cost_all:,.0f}/yr"),
            ]), unsafe_allow_html=True)
    else:
        st.info("👈 Complete the global parameter values and click **Run Master Calculation**.")
