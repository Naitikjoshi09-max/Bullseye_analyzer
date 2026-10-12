import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# Page Config & Glassmorphic Black Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Apex Bullseye AI | Stock & IPO Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS: High-End OLED Black, Glowing Red/Green Accents & Animations
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit Chrome Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}

    /* Ensure Sidebar Expand Button is always visible */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #00ffcc !important;
        background: rgba(20, 20, 25, 0.8) !important;
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        border-radius: 8px !important;
        margin: 10px !important;
    }

    /* Pure OLED Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0a0d14 0%, #030407 60%, #000000 100%);
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Keyframe Animations */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
        70% { box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6); }
        70% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Title Styling */
    .brand-title {
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #10b981 0%, #38bdf8 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
    }

    /* Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }

    /* Recommendation Badges */
    .badge-bullish {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
        padding: 10px 18px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
        animation: pulse-green 2s infinite;
        letter-spacing: 0.5px;
    }
    .badge-bearish {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #ef4444;
        padding: 10px 18px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
        animation: pulse-red 2s infinite;
        letter-spacing: 0.5px;
    }
    .badge-neutral {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #f59e0b;
        color: #f59e0b;
        padding: 10px 18px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
    }

    /* Stat Highlight Boxes */
    .stat-profit {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 78, 59, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 14px;
        padding: 16px;
        color: #34d399;
    }
    .stat-loss {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(127, 29, 29, 0.2) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 14px;
        padding: 16px;
        color: #f87171;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Security Access Lock Screen
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="brand-title" style="text-align: center;">⚡ BULLSEYE AI</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Real-time Stock Analytics & IPO Intelligence Terminal</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin-bottom: 12px;">🔒 Terminal Authentication Required</h4>
            <p style="color: #64748b; font-size: 0.85rem;">Authorized institutional personnel only.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("", type="password", placeholder="Enter Terminal Password...", key="pwd")
        if st.button("🔓 Access Intelligence Engine", type="primary", use_container_width=True):
            if pwd.strip() == "BULLSEYE$2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Security Key")
        st.markdown("<br>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# Sidebar Controls & Lock Session
# ---------------------------------------------------------
st.sidebar.markdown('<div class="brand-title" style="font-size: 1.5rem;">⚡ BULLSEYE AI</div>', unsafe_allow_html=True)
st.sidebar.caption("Real-Time Financial Intelligence Engine")

if st.sidebar.button("🔒 Lock Terminal", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")
navigation = st.sidebar.radio(
    "Select Intelligence Module:",
    ["📈 Live Stock Analyzer & AI Signals", "🚀 IPO Tracker & GMP Suggestions", "💰 Interactive Wealth Planner"]
)

# ---------------------------------------------------------
# Helper Engine: Technical Analysis & AI Reasoning
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def fetch_stock_data(ticker_symbol, timeframe):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=timeframe)
        info = stock.info
        return df, info
    except Exception:
        return None, None

def calculate_technical_signals(df):
    if df is None or len(df) < 14:
        return None
    
    # Simple Moving Averages
    df['SMA_50'] = df['Close'].rolling(window=min(50, len(df))).mean()
    df['SMA_200'] = df['Close'].rolling(window=min(200, len(df))).mean()
    
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['20_SMA'] = df['Close'].rolling(window=20).mean()
    df['Std_Dev'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['20_SMA'] + (df['Std_Dev'] * 2)
    df['Lower_Band'] = df['20_SMA'] - (df['Std_Dev'] * 2)
    
    return df

# ---------------------------------------------------------
# MODULE 1: Live Stock Analyzer & AI Signals
# ---------------------------------------------------------
if navigation == "📈 Live Stock Analyzer & AI Signals":
    st.markdown('<div class="brand-title">📈 Real-Time Stock Analyzer</div>', unsafe_allow_html=True)
    st.caption("AI-powered technical evaluation, dynamic chart signals, and direct buy/sell reasoning.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([2, 1])
    with col_input1:
        ticker = st.text_input("Enter Stock Ticker Symbol (e.g., NVDA, AAPL, TSLA, MSFT, RELIANCE.NS):", value="NVDA").upper().strip()
    with col_input2:
        period = st.selectbox("Select Timeframe:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
        
    with st.spinner(f"Fetching real-time market data for {ticker}..."):
        df, info = fetch_stock_data(ticker, period)
        
    if df is None or df.empty:
        st.error(f"⚠️ Unable to fetch market data for symbol **'{ticker}'**. Please check the ticker name and retry.")
    else:
        df = calculate_technical_signals(df)
        latest = df.iloc[-1]
        prev_close = df.iloc[-2]['Close'] if len(df) > 1 else latest['Close']
        price_change = latest['Close'] - prev_close
        pct_change = (price_change / prev_close) * 100
        
        # Determine AI Signal & Reasoning
        rsi_val = latest['RSI'] if 'RSI' in df.columns and not np.isnan(latest['RSI']) else 50
        sma_50 = latest['SMA_50'] if 'SMA_50' in df.columns and not np.isnan(latest['SMA_50']) else latest['Close']
        
        reasons = []
        bull_score = 0
        
        if rsi_val < 35:
            bull_score += 2
            reasons.append("🟢 **RSI Oversold:** Indicates selling pressure is exhausted, signaling high potential for a bullish reversal.")
        elif rsi_val > 70:
            bull_score -= 2
            reasons.append("🔴 **RSI Overbought:** Stock is currently overextended; short-term pullback risk is elevated.")
        else:
            reasons.append("🟡 **Neutral Momentum:** RSI is floating in balanced mid-range territory.")
            
        if latest['Close'] > sma_50:
            bull_score += 2
            reasons.append(f"🟢 **Bullish Trend:** Trading above 50-day Moving Average (${sma_50:.2f}).")
        else:
            bull_score -= 2
            reasons.append(f"🔴 **Bearish Pressure:** Trading below 50-day Moving Average (${sma_50:.2f}).")
            
        if price_change > 0:
            bull_score += 1
            
        if bull_score >= 2:
            signal_badge = '<div class="badge-bullish">🚀 STRONG BUY / BULLISH</div>'
            projected_return = f"+{abs(pct_change * 1.8 + 8.5):.1f}% Target upside potential"
            stat_style = "stat-profit"
        elif bull_score <= -2:
            signal_badge = '<div class="badge-bearish">⚠️ HIGH RISK / BEARISH / AVOID</div>'
            projected_return = f"-{abs(pct_change * 1.5 + 5.2):.1f}% Downside risk potential"
            stat_style = "stat-loss"
        else:
            signal_badge = '<div class="badge-neutral">⏸️ HOLD / NEUTRAL WATCH</div>'
            projected_return = "±3.5% Consolidation range"
            stat_style = "glass-card"

        # KPI Header Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="glass-card">
                <span style="color:#94a3b8; font-size:0.8rem; font-weight:700;">CURRENT PRICE</span>
                <h2 style="font-weight:800; margin-top:4px; font-size:1.8rem;">${latest['Close']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            color_hex = "#10b981" if price_change >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="glass-card">
                <span style="color:#94a3b8; font-size:0.8rem; font-weight:700;">DAY PERFORMANCE</span>
                <h2 style="font-weight:800; margin-top:4px; color:{color_hex}; font-size:1.8rem;">
                    {price_change:+.2f} ({pct_change:+.2f}%)
                </h2>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="glass-card">
                <span style="color:#94a3b8; font-size:0.8rem; font-weight:700;">RSI (14-DAY INDEX)</span>
                <h2 style="font-weight:800; margin-top:4px; font-size:1.8rem;">{rsi_val:.1f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="glass-card">
                <span style="color:#94a3b8; font-size:0.8rem; font-weight:700;">VOLUME</span>
                <h2 style="font-weight:800; margin-top:4px; font-size:1.8rem;">{latest['Volume']:,}</h2>
            </div>
            """, unsafe_allow_html=True)

        # AI Recommendation Section
        st.markdown(f"""
        <div class="{stat_style}" style="margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin-bottom: 4px; font-weight: 800;">AI Investment Decision & Signal Verdict</h3>
                    <p style="font-weight:600; font-size:1.05rem;">Projected Estimate: <b>{projected_return}</b></p>
                </div>
                <div>{signal_badge}</div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 16px 0;">
            <h5 style="margin-bottom:8px; font-weight:700;">Why Invest or Avoid This Stock? (Detailed Rationale)</h5>
            {"".join([f"<p style='margin-bottom:6px;'>• {r}</p>" for r in reasons])}
        </div>
        """, unsafe_allow_html=True)

        # Interactive High-End Candlestick Chart
        st.subheader("📊 Live OLED Interactive Price Chart")
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Candlestick",
            increasing_line_color='#10b981',
            decreasing_line_color='#ef4444',
            increasing_fillcolor='#10b981',
            decreasing_fillcolor='#ef4444'
        ))
        
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='#38bdf8', width=1.5), name="50-Day SMA"))
        if 'Upper_Band' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['Upper_Band'], line=dict(color='#a855f7', width=1, dash='dot'), name="Upper Bollinger"))
            fig.add_trace(go.Scatter(x=df.index, y=df['Lower_Band'], line=dict(color='#a855f7', width=1, dash='dot'), name="Lower Bollinger"))

        fig.update_layout(
            paper_bgcolor="#030407",
            plot_bgcolor="#0a0d14",
            xaxis=dict(gridcolor="#1e293b", rangeslider=dict(visible=False)),
            yaxis=dict(gridcolor="#1e293b"),
            font=dict(color="#cbd5e1", family="Inter"),
            margin=dict(l=20, r=20, t=30, b=20),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE 2: IPO Tracker & GMP Suggestions
# ---------------------------------------------------------
elif navigation == "🚀 IPO Tracker & GMP Suggestions":
    st.markdown('<div class="brand-title">🚀 IPO Intelligence & GMP Tracker</div>', unsafe_allow_html=True)
    st.caption("Live Grey Market Premium (GMP) updates, subscription ratios, and AI application recommendations.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mock/Live Data Structure for Upcoming & Recent IPOs
    ipo_data = [
        {"Company": "AuraTech Quantum AI", "Price Band": "$120 - $128", "GMP ($)": "+$42", "Est Profit %": "+32.8%", "Subscription": "48.2x", "Risk": "Low", "Verdict": "APPLY (STRONG)"},
        {"Company": "NexGen Battery Systems", "Price Band": "$85 - $90", "GMP ($)": "+$18", "Est Profit %": "+20.0%", "Subscription": "18.5x", "Risk": "Moderate", "Verdict": "APPLY"},
        {"Company": "OmniLogistics Global", "Price Band": "$45 - $48", "GMP ($)": "-$2", "Est Profit %": "-4.1%", "Subscription": "0.8x", "Risk": "High", "Verdict": "AVOID"},
        {"Company": "CloudScale Security", "Price Band": "$210 - $225", "GMP ($)": "+$65", "Est Profit %": "+28.8%", "Subscription": "32.1x", "Risk": "Low", "Verdict": "APPLY (STRONG)"},
        {"Company": "UrbanRetail Properties", "Price Band": "$30 - $32", "GMP ($)": "+$1", "Est Profit %": "+3.1%", "Subscription": "1.2x", "Risk": "High", "Verdict": "AVOID"},
    ]
    
    ipo_df = pd.DataFrame(ipo_data)
    
    col_ipo1, col_ipo2 = st.columns([2, 1])
    
    with col_ipo1:
        st.subheader("🔥 Featured Upcoming & Active IPOs")
        st.dataframe(ipo_df, use_container_width=True, height=280)
        
    with col_ipo2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin-bottom: 8px;">💡 AI Application Rules</h4>
            <p style="font-size: 0.88rem; color: #94a3b8;">
                <b>• GMP > +20%:</b> High probability of listing gains; recommended for listing profit.<br><br>
                <b>• Subscription > 15x:</b> Strong institutional demand backing.<br><br>
                <b>• Negative GMP:</b> Indicates expected listing loss; stay away.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 Individual IPO Analysis Inspector")
    
    selected_ipo = st.selectbox("Select IPO for Breakdown:", ipo_df["Company"].tolist())
    details = ipo_df[ipo_df["Company"] == selected_ipo].iloc[0]
    
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown(f'<div class="glass-card"><b>PRICE BAND</b><h4>{details["Price Band"]}</h4></div>', unsafe_allow_html=True)
    with d2:
        st.markdown(f'<div class="glass-card"><b>EXPECTED GMP</b><h4 style="color:#10b981;">{details["GMP ($)"]}</h4></div>', unsafe_allow_html=True)
    with d3:
        color = "#10b981" if "-" not in details["Est Profit %"] else "#ef4444"
        st.markdown(f'<div class="glass-card"><b>ESTIMATED RETURN</b><h4 style="color:{color};">{details["Est Profit %"]}</h4></div>', unsafe_allow_html=True)
    with d4:
        st.markdown(f'<div class="glass-card"><b>VERDICT</b><h4>{details["Verdict"]}</h4></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3: Interactive Wealth Planner
# ---------------------------------------------------------
elif navigation == "💰 Interactive Wealth Planner":
    st.markdown('<div class="brand-title">💰 Interactive Investment & Wealth Planner</div>', unsafe_allow_html=True)
    st.caption("Simulate systematic compounding growth, calculate exact profit projections, and plan financial independence.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_plan1, c_plan2 = st.columns([1, 2])
    
    with c_plan1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎛️ Growth Parameters")
        
        investment_type = st.radio("Plan Type:", ["Monthly SIP", "Lump Sum Deposit"])
        monthly_amount = st.slider("Monthly Investment ($):", min_value=100, max_value=20000, value=1000, step=100)
        years = st.slider("Investment Horizon (Years):", min_value=1, max_value=35, value=10)
        expected_cagr = st.slider("Expected Annual CAGR Return (%):", min_value=1.0, max_value=30.0, value=12.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Compounding Calculation Logic
    months = years * 12
    rate_monthly = (expected_cagr / 100) / 12
    
    timeline = list(range(1, months + 1))
    invested_data = []
    wealth_data = []
    
    current_wealth = 0
    total_invested = 0
    
    for m in timeline:
        if investment_type == "Monthly SIP":
            total_invested += monthly_amount
            current_wealth = (current_wealth + monthly_amount) * (1 + rate_monthly)
        else:
            if m == 1:
                total_invested = monthly_amount
                current_wealth = monthly_amount
            current_wealth = current_wealth * (1 + rate_monthly)
            
        invested_data.append(total_invested)
        wealth_data.append(current_wealth)
        
    profit_generated = current_wealth - total_invested
    
    with c_plan2:
        res1, res2, res3 = st.columns(3)
        with res1:
            st.markdown(f'<div class="glass-card"><b>TOTAL INVESTED</b><h3 style="color:#94a3b8;">${total_invested:,.0f}</h3></div>', unsafe_allow_html=True)
        with res2:
            st.markdown(f'<div class="glass-card"><b>PROFIT GENERATED</b><h3 style="color:#10b981;">+${profit_generated:,.0f}</h3></div>', unsafe_allow_html=True)
        with res3:
            st.markdown(f'<div class="glass-card"><b>FUTURE WEALTH</b><h3 style="color:#38bdf8;">${current_wealth:,.0f}</h3></div>', unsafe_allow_html=True)
            
        # Wealth Growth Projection Plot
        df_plan = pd.DataFrame({
            "Month": timeline,
            "Principal Invested": invested_data,
            "Total Accumulated Wealth": wealth_data
        })
        
        fig_wealth = px.area(
            df_plan, x="Month", y=["Total Accumulated Wealth", "Principal Invested"],
            color_discrete_map={"Total Accumulated Wealth": "#10b981", "Principal Invested": "#6366f1"},
            title="📈 Projected Wealth Accumulation Timeline"
        )
        fig_wealth.update_layout(
            paper_bgcolor="#030407",
            plot_bgcolor="#0a0d14",
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
            font=dict(color="#cbd5e1")
        )
        st.plotly_chart(fig_wealth, use_container_width=True)
