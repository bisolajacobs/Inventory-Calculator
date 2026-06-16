import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

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

.main {
    background: #f8fafc;
}
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%);
}

.hero-banner {
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    background: rgba(255,255,255,0.8);
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

.module-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
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

.section-header {
    color: #475569;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}

.info-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    color: #000000 !important;
    line-height: 1.6;
    margin-top: 0.6rem;
    margin-bottom: 1rem;
}
.info-box * {
    color: #000000 !important;
}
.info-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.info-label {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.45rem;
}

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

div[data-testid="stSelectbox"] > div {
    background: #ffffff !important;
    border-color: #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

hr { border-color: #e2e8f0 !important; }

details {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}

span[data-testid="stTag"] {
    background: #eff6ff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 20px !important;
}

.stAlert {
    border-radius: 12px !important;
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
    </div>"""

def formula_html(rows):
    inner = "".join(
        f'<div class="formula-row"><span class="formula-name">{n}</span><span class="formula-result">{v}</span></div>'
        for n, v in rows
    )
    return f'<div class="formula-box">{inner}</div>'

def info_html(title, label, explanation):
    return f"""
    <div class="info-box">
        <div class="info-title">{title}</div>
        <div class="info-label">{label}</div>
        <div>{explanation}</div>
    </div>
    """

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
    fig.add_vline(
        x=mean, line_dash="dash", line_color="#059669",
        annotation_text=f"Mean = {mean:.1f}", annotation_font_color="#059669"
    )
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

if "module" not in st.session_state:
    st.session_state.module = None

MODULES = [
    ("📊", "Mean, Variance & SD", "Demand statistics", "stats"),
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

st.markdown('<div class="section-header">Please choose what you want to calculate</div>', unsafe_allow_html=True)

cols = st.columns(7)
for i, (icon, name, desc, mid) in enumerate(MODULES):
    with cols[i]:
        active = st.session_state.module == mid
        st.markdown(f"""
        <div class="module-card {'active' if active else ''}">
            <div class="module-icon">{icon}</div>
            <div class="module-name">{name}</div>
            <div class="module-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Open", key=f"btn_{mid}", use_container_width=True):
            st.session_state.module = mid
            st.rerun()

st.markdown("---")
mod = st.session_state.module

if mod is None:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 0; color: #64748b;">
        <div style="font-size:3rem; margin-bottom:1rem">👆</div>
        <div style="font-size:1.1rem; font-weight:500; color:#475569">Select a calculator above to begin</div>
        <div style="font-size:0.85rem; margin-top:0.5rem; color:#64748b">Each module calculates a specific inventory formula</div>
    </div>
    """, unsafe_allow_html=True)

elif mod == "stats":
    st.markdown("### 📊 Mean, Variance & Standard Deviation")
    st.markdown("Enter your demand observations to compute key statistical measures.")

    col1, col2 = st.columns([1, 2])
    with col1:
        raw = st.text_area(
            "Demand values (comma-separated)",
            value="40, 55, 60, 35, 70, 50, 65, 45, 80, 58, 42, 67",
            height=120,
            help="Type or paste daily demand values separated by commas",
        )
        calculate = st.button("Calculate Statistics", key="calc_stats")

    with col2:
        if calculate:
            try:
                data = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if len(data) < 2:
                    st.error("Please enter at least 2 values.")
                else:
                    n = len(data)
                    mu = np.mean(data)
                    variance = np.var(data)
                    sigma = np.std(data)

                    st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
                    cols_metrics([
                        ("Mean (μ)", f"{mu:.2f}", "units/day"),
                        ("Variance (σ²)", f"{variance:.2f}", "units²"),
                        ("Std deviation (σ)", f"{sigma:.2f}", "units/day"),
                        ("Observations (n)", str(n), "data points"),
                    ])

                    st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
                    sample_str = " + ".join(f"{x:.0f}" for x in data[:4])
                    if n > 4:
                        sample_str += " + ..."
                    st.markdown(formula_html([
                        ("μ = Σx / n", f"{sample_str} / {n} = {mu:.2f}"),
                        ("σ² = Σ(x−μ)² / n", f"{variance:.4f}"),
                        ("σ = √σ²", f"√{variance:.2f} = {sigma:.2f}"),
                        ("Demand follows", f"N({mu:.2f}, {variance:.2f})"),
                    ]), unsafe_allow_html=True)

                    st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.plotly_chart(hist_chart(data, mu, "Demand distribution"), use_container_width=True)
                    with c2:
                        sessions = list(range(1, n + 1))
                        cum_mean = [np.mean(data[:i]) for i in range(1, n + 1)]
                        st.plotly_chart(
                            line_chart(sessions, {"Cumulative mean": cum_mean}, "Convergence of mean", "Mean demand"),
                            use_container_width=True
                        )
            except Exception as e:
                st.error(f"Error parsing values: {e}")
        else:
            st.info("👈 Enter your demand values and click **Calculate Statistics**")

elif mod == "ss":
    st.markdown("### 🛡️ Safety Stock")
    st.markdown(info_html(
        "Safety Stocks",
        "Extra Goods Kept",
        "Extra stock kept for emergencies."
    ), unsafe_allow_html=True)
    st.markdown("If you normally sell 100 loaves of bread, you may keep 20 extra loaves in case more customers come than expected.")

    col1, col2 = st.columns([1, 2])
    with col1:
        sigma = st.number_input("Std deviation (σ)", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox(
            "Service level",
            options=[1.28, 1.65, 1.96, 2.33],
            index=1,
            format_func=lambda x: {1.28:"90% (z=1.28)", 1.65:"95% (z=1.65)", 1.96:"97.5% (z=1.96)", 2.33:"99% (z=2.33)"}[x],
        )
        calculate = st.button("Calculate Safety Stocks", key="calc_ss")

    with col2:
        if calculate:
            sigma_L = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_L
            pct = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z]

            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("σ√L", f"{sigma_L:.2f}", "units"),
                ("Service level", f"{pct}%", ""),
                ("Lead time", str(lead), "days"),
            ])

            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("σ√L", f"{sigma} × √{lead} = {sigma_L:.2f}"),
                ("Safety stocks = z·σ√L", f"{z} × {sigma_L:.2f} = {safety_stocks:.1f} units"),
            ]), unsafe_allow_html=True)

            st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(color_gauge(safety_stocks, max(safety_stocks * 2, 1), "Safety stocks (units)", "#6366f1"), use_container_width=True)
            with c2:
                z_vals = [1.28, 1.65, 1.96, 2.33]
                ss_vals = [zv * sigma * np.sqrt(lead) for zv in z_vals]
                lbls = ["90%", "95%", "97.5%", "99%"]
                clrs = ["#6366f1" if zv == z else "#cbd5e1" for zv in z_vals]
                st.plotly_chart(bar_chart(lbls, ss_vals, clrs, "Safety stocks by service level", "Units"), use_container_width=True)
        else:
            st.info("👈 Fill the inputs and click **Calculate Safety Stocks**")

elif mod == "rop":
    st.markdown("### 🔄 Reorder Point")
    st.markdown(info_html(
        "Reorder Point",
        "When to Buy More",
        "The stock level at which you should place a new order."
    ), unsafe_allow_html=True)
    st.markdown("If your reorder point is 50 cartons, you should order more stock once you have only 50 cartons left.")

    col1, col2 = st.columns([1, 2])
    with col1:
        mu = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Std deviation (σ)", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1)
        z = st.selectbox(
            "Service level",
            options=[1.28, 1.65, 1.96, 2.33],
            index=1,
            format_func=lambda x: {1.28:"90%", 1.65:"95%", 1.96:"97.5%", 2.33:"99%"}[x],
            key="rop_sl",
        )
        calculate = st.button("Calculate Reorder Point", key="calc_rop")

    with col2:
        if calculate:
            sigma_L = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_L
            demand_during_lt = mu * lead
            reorder_point = demand_during_lt + safety_stocks

            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Reorder point", f"{reorder_point:.1f}", "units"),
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("Demand during lead time", f"{demand_during_lt:.1f}", "units"),
                ("Lead time", str(lead), "days"),
            ])

            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("Demand during lead time", f"{mu} × {lead} = {demand_during_lt:.1f}"),
                ("Safety stocks = z·σ√L", f"{z} × {sigma_L:.2f} = {safety_stocks:.1f}"),
                ("Reorder point = Demand during lead time + Safety stocks", f"{demand_during_lt:.1f} + {safety_stocks:.1f} = {reorder_point:.1f} units"),
            ]), unsafe_allow_html=True)

            st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during lead time", "Safety stocks", "Reorder point"],
                    y=[demand_during_lt, safety_stocks, 0],
                    connector={"line": {"color": "#cbd5e1"}},
                    increasing={"marker": {"color": "#059669"}},
                    totals={"marker": {"color": "#2563eb"}},
                    text=[f"{demand_during_lt:.1f}", f"{safety_stocks:.1f}", f"{reorder_point:.1f}"],
                    textposition="outside",
                    textfont={"color": "#0f172a"},
                ))
                fig.update_layout(
                    title={"text": "Reorder point composition", "font": {"color": "#0f172a", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"gridcolor": "#e2e8f0", "color": "#64748b"},
                    xaxis={"color": "#64748b"},
                    height=300,
                    margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                lead_range = list(range(0, 16))
                rops = [mu * l + z * sigma * np.sqrt(l) for l in lead_range]
                st.plotly_chart(line_chart(lead_range, {"Reorder point": rops}, "Reorder point vs lead time", "Units"), use_container_width=True)
        else:
            st.info("👈 Fill the inputs and click **Calculate Reorder Point**")

elif mod == "eoq":
    st.markdown("### 📦 Economic Order Quantity (EOQ)")
    st.markdown(info_html(
        "Economic Order Quantity (EOQ)",
        "How Much More to Buy",
        "The best amount of stock to order at one time."
    ), unsafe_allow_html=True)
    st.markdown("Ordering too little causes frequent trips to suppliers. Ordering too much may lead to spoilage. EOQ helps find a balance.")

    col1, col2 = st.columns([1, 2])
    with col1:
        d = st.number_input("Mean daily demand (d)", min_value=0.0, value=50.0, step=1.0)
        S = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0)
        H = st.number_input("Holding cost per unit/yr (₦)", min_value=0.0, value=20.0, step=1.0)
        calculate = st.button("Calculate EOQ", key="calc_eoq")

    with col2:
        if calculate:
            if H == 0:
                st.error("Holding cost cannot be zero.")
            else:
                D = d * 365
                eoq = np.sqrt((2 * D * S) / H)
                orders = D / eoq
                hc = (eoq / 2) * H
                oc = orders * S
                tc = hc + oc

                st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
                cols_metrics([
                    ("Economic order quantity", f"{eoq:,.0f}", "units/order"),
                    ("Annual demand", f"{D:,.0f}", "units/year"),
                    ("Orders per year", f"{orders:.1f}", "orders"),
                    ("Minimum total cost", f"₦{tc:,.0f}", ""),
                ])

                st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
                st.markdown(formula_html([
                    ("D = d × 365", f"{d} × 365 = {D:,.0f}"),
                    ("EOQ = √(2DS/H)", f"√(2×{D:,.0f}×{S:,.0f}/{H}) = {eoq:,.1f}"),
                    ("Holding cost = (Q/2)×H", f"({eoq:,.0f}/2)×{H} = ₦{hc:,.0f}"),
                    ("Ordering cost = (D/Q)×S", f"({D:,.0f}/{eoq:,.0f})×{S:,.0f} = ₦{oc:,.0f}"),
                    ("Total cost = Holding cost + Ordering cost", f"₦{hc:,.0f} + ₦{oc:,.0f} = ₦{tc:,.0f}"),
                ]), unsafe_allow_html=True)

                st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    q_range = np.linspace(max(eoq * 0.2, 1e-6), eoq * 3, 200)
                    hc_line = (q_range / 2) * H
                    oc_line = (D / q_range) * S
                    tc_line = hc_line + oc_line
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color": "#6366f1", "width": 2}, mode="lines"))
                    fig.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color": "#db2777", "width": 2}, mode="lines"))
                    fig.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total cost", line={"color": "#059669", "width": 3}, mode="lines"))
                    fig.add_vline(x=eoq, line_dash="dash", line_color="#2563eb", annotation_text=f"EOQ={eoq:,.0f}", annotation_font_color="#2563eb")
                    fig.update_layout(
                        title={"text": "Cost vs order quantity", "font": {"color": "#0f172a", "size": 15}, "x": 0},
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"family": "Inter", "color": "#475569"},
                        yaxis={"title": "Cost (₦)", "gridcolor": "#e2e8f0", "color": "#64748b"},
                        xaxis={"title": "Order quantity", "color": "#64748b"},
                        legend={"bgcolor": "rgba(0,0,0,0)"},
                        height=320,
                        margin=dict(t=50, b=20, l=20, r=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    st.plotly_chart(bar_chart(["Holding cost", "Ordering cost"], [hc, oc], ["#6366f1", "#db2777"], "Cost breakdown", "₦"), use_container_width=True)
        else:
            st.info("👈 Fill the inputs and click **Calculate EOQ**")

elif mod == "tc":
    st.markdown("### 💰 Total Inventory Cost")
    st.markdown(info_html(
        "Total Cost of Goods",
        "Total Cost of Goods",
        "The overall cost of managing inventory."
    ), unsafe_allow_html=True)
    st.markdown("It combines the cost of storing stock, ordering stock, and losses from stock shortages.")

    col1, col2 = st.columns([1, 2])
    with col1:
        d = st.number_input("Mean daily demand (d)", min_value=0.0, value=50.0, step=1.0)
        S = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0)
        H = st.number_input("Holding cost per unit/yr (₦)", min_value=0.0, value=20.0, step=1.0)
        SC = st.number_input("Shortage cost per unit (₦)", min_value=0.0, value=50.0, step=1.0)
        sigma = st.number_input("Std deviation (σ)", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
        calculate = st.button("Calculate Total Cost", key="calc_tc")

    with col2:
        if calculate:
            if H == 0:
                st.error("Holding cost cannot be zero.")
            else:
                D = d * 365
                eoq = np.sqrt((2 * D * S) / H)
                orders = D / eoq if eoq != 0 else 0
                holding_cost = (eoq / 2) * H
                ordering_cost = orders * S
                shortage_cost = SC * sigma * 0.1 * orders
                total_cost = holding_cost + ordering_cost + shortage_cost

                st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
                cols_metrics([
                    ("Holding cost", f"₦{holding_cost:,.0f}", ""),
                    ("Ordering cost", f"₦{ordering_cost:,.0f}", ""),
                    ("Shortage cost", f"₦{shortage_cost:,.0f}", ""),
                    ("Total cost", f"₦{total_cost:,.0f}", ""),
                ])

                st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
                st.markdown(formula_html([
                    ("Economic order quantity", f"{eoq:,.0f} units"),
                    ("Holding cost = (Q/2)×H", f"₦{holding_cost:,.0f}"),
                    ("Ordering cost = (D/Q)×S", f"₦{ordering_cost:,.0f}"),
                    ("Shortage cost estimate", f"₦{shortage_cost:,.0f}"),
                    ("Total cost = Holding cost + Ordering cost + Shortage cost", f"₦{total_cost:,.0f}"),
                ]), unsafe_allow_html=True)

                st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    fig = go.Figure(go.Pie(
                        labels=["Holding cost", "Ordering cost", "Shortage cost"],
                        values=[holding_cost, ordering_cost, shortage_cost],
                        hole=0.55,
                        marker={"colors": ["#6366f1", "#db2777", "#ea580c"], "line": {"color": "#ffffff", "width": 2}},
                        textfont={"color": "#0f172a"},
                    ))
                    fig.add_annotation(text=f"₦{total_cost:,.0f}", x=0.5, y=0.5, showarrow=False, font={"size": 14, "color": "#0f172a"})
                    fig.update_layout(
                        title={"text": "Cost breakdown", "font": {"color": "#0f172a", "size": 15}},
                        paper_bgcolor="rgba(0,0,0,0)",
                        font={"family": "Inter", "color": "#475569"},
                        legend={"bgcolor": "rgba(0,0,0,0)"},
                        height=320,
                        margin=dict(t=50, b=10, l=10, r=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    q_range = np.linspace(max(eoq * 0.2, 1e-6), eoq * 3, 200)
                    tc_line = (q_range/2)*H + (D/q_range)*S + SC*sigma*0.1*(D/q_range)
                    fig2 = go.Figure(go.Scatter(
                        x=q_range, y=tc_line,
                        line={"color": "#059669", "width": 2.5},
                        mode="lines",
                        name="Total cost"
                    ))
                    fig2.add_vline(
                        x=eoq,
                        line_dash="dash",
                        line_color="#2563eb",
                        annotation_text=f"EOQ={eoq:,.0f}",
                        annotation_font_color="#2563eb"
                    )
                    fig2.update_layout(
                        title={"text": "Total cost curve", "font": {"color": "#0f172a", "size": 15}},
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"family": "Inter", "color": "#475569"},
                        yaxis={"title": "₦", "gridcolor": "#e2e8f0", "color": "#64748b"},
                        xaxis={"title": "Order qty", "color": "#64748b"},
                        height=320,
                        margin=dict(t=50, b=20, l=20, r=20),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("👈 Fill the inputs and click **Calculate Total Cost**")

elif mod == "sl":
    st.markdown("### 🎯 Service Level")
    st.markdown(info_html(
        "Service Level",
        "Avoid Running Out",
        "This shows how well your stock protects you from running out."
    ), unsafe_allow_html=True)
    st.markdown("A higher service level means you are less likely to run out of stock.")

    col1, col2 = st.columns([1, 2])
    with col1:
        z = st.slider("Service level factor (z)", min_value=1.0, max_value=3.0, value=1.65, step=0.01)
        sigma = st.number_input("Std deviation (σ)", min_value=0.0, value=12.5, step=0.5)
        lead = st.number_input("Lead time (days)", min_value=0, value=5, step=1)
        calculate = st.button("Calculate Service Level", key="calc_sl")

    with col2:
        if calculate:
            if z >= 2.33:
                pct = 99
            elif z >= 1.96:
                pct = 97.5
            elif z >= 1.65:
                pct = 95
            elif z >= 1.28:
                pct = 90
            else:
                pct = round(50 + z * 30, 1)

            sigma_L = sigma * np.sqrt(lead)
            safety_stocks = z * sigma_L

            st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Service level", f"{pct}%", ""),
                ("Safety stocks", f"{safety_stocks:.1f}", "units"),
                ("z factor", f"{z:.2f}", ""),
                ("Stock-out risk", f"{100-pct:.1f}%", ""),
            ])

            st.markdown('<div class="section-header">Formula trace</div>', unsafe_allow_html=True)
            st.markdown(formula_html([
                ("z value", str(z)),
                ("Service level", f"≈ {pct}%"),
                ("Safety stocks = z·σ√L", f"{z} × {sigma_L:.2f} = {safety_stocks:.1f} units"),
                ("Stock-out risk", f"~{100-pct:.1f}%"),
            ]), unsafe_allow_html=True)

            st.markdown('<div class="section-header">Charts</div>', unsafe_allow_html=True)
            st.plotly_chart(color_gauge(safety_stocks, max(safety_stocks * 2, 1), "Safety stocks allocation", "#059669"), use_container_width=True)
        else:
            st.info("👈 Adjust the slider and click **Calculate Service Level**")

elif mod == "all":
    st.markdown("### 🚀 Master Inventory Dashboard (All-in-One)")
    st.markdown("Enter all your core thresholds below to evaluate every single inventory metric at once.")

    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        mu_all = st.number_input("Mean daily demand (μ)", min_value=0.0, value=50.0, step=1.0, key="all_mu")
        sigma_all = st.number_input("Std deviation (σ)", min_value=0.0, value=12.5, step=0.5, key="all_sigma")
    with icol2:
        lead_all = st.number_input("Lead time (days, L)", min_value=0, value=5, step=1, key="all_lead")
        z_all = st.selectbox(
            "Service level",
            options=[1.28, 1.65, 1.96, 2.33],
            index=1,
            format_func=lambda x: {1.28:"90% (z=1.28)",1.65:"95% (z=1.65)",1.96:"97.5% (z=1.96)",2.33:"99% (z=2.33)"}[x],
            key="all_z",
        )
    with icol3:
        S_all = st.number_input("Ordering cost per order (₦)", min_value=0.0, value=5000.0, step=100.0, key="all_S")
        H_all = st.number_input("Holding cost per unit/yr (₦)", min_value=0.0, value=20.0, step=1.0, key="all_H")
        SC_all = st.number_input("Shortage cost per unit (₦)", min_value=0.0, value=50.0, step=1.0, key="all_SC")

    calculate_all = st.button("Run Master Calculation", key="calc_all_run")

    if calculate_all:
        if H_all == 0:
            st.error("Holding cost cannot be zero for full metric simulation.")
        else:
            D_all = mu_all * 365
            sigma_L_all = sigma_all * np.sqrt(lead_all)
            safety_stocks_all = z_all * sigma_L_all
            demand_during_lt_all = mu_all * lead_all
            reorder_point_all = demand_during_lt_all + safety_stocks_all
            eoq_all = np.sqrt((2 * D_all * S_all) / H_all)
            orders_all = D_all / eoq_all if eoq_all != 0 else 0
            holding_cost_all = (eoq_all / 2) * H_all
            ordering_cost_all = orders_all * S_all
            shortage_cost_all = SC_all * sigma_all * 0.1 * orders_all
            total_cost_all = holding_cost_all + ordering_cost_all + shortage_cost_all
            pct_all = {1.28:90, 1.65:95, 1.96:97.5, 2.33:99}[z_all]

            st.markdown('<div class="section-header">Primary Optimization Metrics</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Economic order quantity", f"{eoq_all:,.0f}", "units/order"),
                ("Safety stocks", f"{safety_stocks_all:.1f}", "units"),
                ("Reorder point", f"{reorder_point_all:.1f}", "units"),
                ("Total annual cost", f"₦{total_cost_all:,.0f}", ""),
            ], ncols=4)

            st.markdown('<div class="section-header">Operations Framework Breakdown</div>', unsafe_allow_html=True)
            cols_metrics([
                ("Annual demand volume", f"{D_all:,.0f}", "units/year"),
                ("Orders placed", f"{orders_all:.1f}", "times/year"),
                ("Demand during lead time", f"{demand_during_lt_all:.1f}", "units"),
                ("Cycle service level", f"{pct_all}%", f"z={z_all}"),
            ], ncols=4)

            st.markdown('<div class="section-header">System Optimization Visualizations</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                q_range = np.linspace(max(eoq_all * 0.2, 1e-6), eoq_all * 3, 200)
                hc_line = (q_range / 2) * H_all
                oc_line = (D_all / q_range) * S_all
                tc_line = hc_line + oc_line + (SC_all * sigma_all * 0.1 * (D_all / q_range))
                fig_all = go.Figure()
                fig_all.add_trace(go.Scatter(x=q_range, y=hc_line, name="Holding cost", line={"color": "#6366f1", "width": 2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=oc_line, name="Ordering cost", line={"color": "#db2777", "width": 2}, mode="lines"))
                fig_all.add_trace(go.Scatter(x=q_range, y=tc_line, name="Total system", line={"color": "#059669", "width": 3}, mode="lines"))
                fig_all.add_vline(x=eoq_all, line_dash="dash", line_color="#2563eb", annotation_text=f"EOQ={eoq_all:,.0f}", annotation_font_color="#2563eb")
                fig_all.update_layout(
                    title={"text": "Total Optimization Cost Curves", "font": {"color": "#0f172a", "size": 15}},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"title": "Cost (₦)", "gridcolor": "#e2e8f0", "color": "#64748b"},
                    xaxis={"title": "Order quantity Thresholds", "color": "#64748b"},
                    legend={"bgcolor": "rgba(0,0,0,0)"},
                    height=320,
                    margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_all, use_container_width=True)
            with c2:
                fig_wf = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Demand during lead time", "Safety stocks", "Reorder point"],
                    y=[demand_during_lt_all, safety_stocks_all, 0],
                    connector={"line": {"color": "#cbd5e1"}},
                    increasing={"marker": {"color": "#059669"}},
                    totals={"marker": {"color": "#2563eb"}},
                    text=[f"{demand_during_lt_all:.1f}", f"{safety_stocks_all:.1f}", f"{reorder_point_all:.1f}"],
                    textposition="outside",
                    textfont={"color": "#0f172a"},
                ))
                fig_wf.update_layout(
                    title={"text": "Reorder point structure balance", "font": {"color": "#0f172a", "size": 16}},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"family": "Inter", "color": "#475569"},
                    yaxis={"gridcolor": "#e2e8f0", "color": "#64748b"},
                    xaxis={"color": "#64748b"},
                    height=320,
                    margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_wf, use_container_width=True)

            with st.expander("📖 View Consolidated Formula Audit Trail"):
                st.markdown(formula_html([
                    ("Annual demand volume", f"{mu_all} × 365 = {D_all:,.0f} units/yr"),
                    ("Economic order quantity", f"√(2 × {D_all:,.0f} × {S_all:,.0f} / {H_all}) = {eoq_all:,.1f} units"),
                    ("Safety stocks formula", f"{z_all} × ({sigma_all} × √{lead_all}) = {safety_stocks_all:.1f} units"),
                    ("Reorder point target", f"{demand_during_lt_all:.1f} + {safety_stocks_all:.1f} = {reorder_point_all:.1f} units"),
                    ("Total cost matrix", f"Holding cost (₦{holding_cost_all:,.0f}) + Ordering cost (₦{ordering_cost_all:,.0f}) + Shortage cost (₦{shortage_cost_all:,.0f}) = ₦{total_cost_all:,.0f}/yr")
                ]), unsafe_allow_html=True)
    else:
        st.info("👈 Complete the global parameter values and click **Run Master Calculation** to get an instant snapshot of your entire optimization portfolio.")
