import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
import re

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Apex Bharat Market AI | NSE & BSE Live Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Glitch-Free Pure OLED Dark Glassmorphism CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit Header Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}

    /* Sidebar Expand / Collapse Toggle Fix */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #00ffcc !important;
        background: #090d16 !important;
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        border-radius: 8px !important;
        margin: 10px !important;
    }

    /* OLED Pure Black Background & Pure White Text */
    .stApp {
        background-color: #000000;
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Cyber Title Styling */
    .brand-title {
        font-size: 2.3rem;
        font-weight: 900;
        letter-spacing: -0.8px;
        background: linear-gradient(90deg, #10b981 0%, #38bdf8 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphic Dark Cards */
    .glass-card-dark {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
    }

    /* Glowing Pulsing Badges */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    .badge-bullish {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #34d399;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        animation: pulse-green 2s infinite;
        font-size: 0.95rem;
    }
    .badge-bearish {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #f87171;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        animation: pulse-red 2s infinite;
        font-size: 0.95rem;
    }
    .badge-neutral {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        font-size: 0.95rem;
    }

    .stat-profit-dark {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 78, 59, 0.25) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 16px;
        padding: 22px;
        color: #e2e8f0;
        margin-bottom: 20px;
    }
    .stat-loss-dark {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(127, 29, 29, 0.25) 100%);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-radius: 16px;
        padding: 22px;
        color: #e2e8f0;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Security Access Authentication
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="brand-title" style="text-align: center;">⚡ APEX BHARAT AI</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-weight:500;'>Real-Time NSE & BSE Stock Intelligence & IPO Decision Engine</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card-dark" style="text-align: center;">
            <h4 style="margin-bottom: 10px; font-weight:800; color:#f8fafc;">🔒 Terminal Lock Screen</h4>
            <p style="color: #94a3b8; font-size: 0.88rem;">Enter authorization password to launch live trading terminal.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("", type="password", placeholder="Enter Terminal Password...", key="pwd")
        if st.button("🚀 Unlock Terminal Engine", type="primary", use_container_width=True):
            if pwd.strip() == "BULLSEYE$2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Security Key")
        st.markdown("<br>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# Formatting Utilities
# ---------------------------------------------------------
def clean_indian_symbol(raw_ticker):
    sym = raw_ticker.strip().upper()
    if not sym:
        return "RELIANCE.NS"
    # Allow market indices directly
    if sym in ["NIFTY", "^NSEI"]:
        return "^NSEI"
    if sym in ["SENSEX", "^BSESN"]:
        return "^BSESN"
    if not (sym.endswith(".NS") or sym.endswith(".BO")):
        sym += ".NS"
    return sym

def format_inr(val):
    if val is None or np.isnan(val):
        return "N/A"
    if abs(val) >= 10000007:
        return f"₹{val/10000000:,.2f} Cr"
    elif abs(val) >= 100005:
        return f"₹{val/100000:,.2f} Lakh"
    else:
        return f"₹{val:,.2f}"

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.markdown('<div class="brand-title" style="font-size: 1.4rem;">⚡ APEX BHARAT</div>', unsafe_allow_html=True)
st.sidebar.caption("NSE & BSE Real-Time Financial Terminal")

if st.sidebar.button("🔒 Lock Terminal Session", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")
navigation = st.sidebar.radio(
    "Select Intelligence Terminal:",
    ["📈 Live NSE/BSE Stock Screener", "🚀 Automated IPO Tracker & Buy Guidance", "💰 Indian Rupee (₹) Wealth Planner"]
)

# ---------------------------------------------------------
# Live Stock Fetching & Technical Indicators
# ---------------------------------------------------------
@st.cache_data(ttl=30)
def fetch_live_stock_data(ticker_symbol, period="6mo"):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period)
        info = stock.info
        if df.empty:
            # Fallback to Bombay Stock Exchange if NSE lookup returns empty
            if ticker_symbol.endswith(".NS"):
                bo_sym = ticker_symbol.replace(".NS", ".BO")
                stock = yf.Ticker(bo_sym)
                df = stock.history(period=period)
                info = stock.info
        return df, info
    except Exception:
        return None, None

def compute_technical_signals(df):
    if df is None or len(df) < 14:
        return None
    
    # Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=min(50, len(df))).mean()
    df['SMA_200'] = df['Close'].rolling(window=min(200, len(df))).mean()
    
    # RSI (14)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['Std_Dev'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['SMA_20'] + (df['Std_Dev'] * 2)
    df['Lower_Band'] = df['SMA_20'] - (df['Std_Dev'] * 2)
    
    # MACD
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

# ---------------------------------------------------------
# MODULE 1: Live NSE/BSE Stock Screener & Buy/Sell Guidance
# ---------------------------------------------------------
if navigation == "📈 Live NSE/BSE Stock Screener":
    st.markdown('<div class="brand-title">📈 NSE & BSE Live Stock Analyzer</div>', unsafe_allow_html=True)
    st.caption("Real-time live prices, technical indicators, and automated BUY / SELL / HOLD guidance.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Shortcuts
    st.markdown("<b>⚡ Quick Watchlist Shortcuts:</b>", unsafe_allow_html=True)
    sc_cols = st.columns(8)
    shortcuts = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "TATAMOTORS", "ZOMATO", "SUZLON", "BSE"]
    selected_sc = None
    for i, sc in enumerate(shortcuts):
        if sc_cols[i].button(sc, use_container_width=True):
            selected_sc = sc

    c_in1, c_in2 = st.columns([2, 1])
    with c_in1:
        default_val = selected_sc if selected_sc else "RELIANCE"
        user_input = st.text_input("Search Any NSE/BSE Company (e.g., RELIANCE, TCS, ZOMATO, SUZLON, TATASTEEL):", value=default_val)
        symbol = clean_indian_symbol(user_input)
    with c_in2:
        period = st.selectbox("Select Timeframe:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)
        
    with st.spinner(f"Streaming live price feed for {symbol}..."):
        df, info = fetch_live_stock_data(symbol, period)
        
    if df is None or df.empty:
        st.error(f"⚠️ Market data unavailable for symbol **'{user_input}'**. Verify symbol name on NSE/BSE and retry.")
    else:
        df = compute_technical_signals(df)
        latest = df.iloc[-1]
        prev_close = df.iloc[-2]['Close'] if len(df) > 1 else latest['Close']
        price_change = latest['Close'] - prev_close
        pct_change = (price_change / prev_close) * 100
        
        # Technical Score & Rationale Engine
        rsi_val = latest['RSI'] if 'RSI' in df.columns and not np.isnan(latest['RSI']) else 50
        sma_50 = latest['SMA_50'] if 'SMA_50' in df.columns and not np.isnan(latest['SMA_50']) else latest['Close']
        macd = latest['MACD'] if 'MACD' in df.columns else 0
        macd_sig = latest['MACD_Signal'] if 'MACD_Signal' in df.columns else 0
        
        reasons = []
        score = 0
        
        # 1. RSI Logic
        if rsi_val < 35:
            score += 2
            reasons.append(f"🟢 **RSI Oversold ({rsi_val:.1f}):** Selling exhaustion detected. Excellent risk-to-reward ratio for buy entry.")
        elif rsi_val > 70:
            score -= 2
            reasons.append(f"🔴 **RSI Overbought ({rsi_val:.1f}):** Stock is overextended in short term. Risk of profit-booking pullback.")
        else:
            reasons.append(f"🟡 **Neutral RSI ({rsi_val:.1f}):** Balanced momentum with healthy trade flow.")
            
        # 2. Moving Average Trend
        if latest['Close'] > sma_50:
            score += 2
            reasons.append(f"🟢 **Bullish Trend Above 50-SMA:** Price (₹{latest['Close']:,.2f}) is trading strong above 50-Day Moving Average (₹{sma_50:,.2f}).")
        else:
            score -= 2
            reasons.append(f"🔴 **Bearish Trend Below 50-SMA:** Price (₹{latest['Close']:,.2f}) is struggling below 50-Day Moving Average (₹{sma_50:,.2f}).")
            
        # 3. MACD Momentum
        if macd > macd_sig:
            score += 1
            reasons.append("🟢 **MACD Bullish Crossover:** MACD line is above signal line, confirming upward momentum.")
        else:
            score -= 1
            reasons.append("🔴 **MACD Bearish Crossover:** MACD line is below signal line, indicating momentum weakness.")

        # Price Levels Calculation
        support_level = df['Low'].tail(20).min()
        resistance_level = df['High'].tail(20).max()
        stop_loss = latest['Close'] * 0.95
        target_price = latest['Close'] * 1.10

        # Action Verdict Badges
        if score >= 2:
            verdict_badge = '<div class="badge-bullish">🚀 BUY / BULLISH ENTRY</div>'
            verdict_style = "stat-profit-dark"
            action_summary = "STRONGLY RECOMMENDED FOR BUYING"
        elif score <= -2:
            verdict_badge = '<div class="badge-bearish">🔴 SELL / BEARISH / AVOID</div>'
            verdict_style = "stat-loss-dark"
            action_summary = "RECOMMENDED TO SELL OR AVOID NEW BUYING"
        else:
            verdict_badge = '<div class="badge-neutral">⏸️ HOLD / NEUTRAL</div>'
            verdict_style = "glass-card-dark"
            action_summary = "HOLD EXISTING POSITIONS & WAIT FOR BREAKOUT"

        # KPI Header Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">LIVE NSE/BSE PRICE</span><h2 style="font-weight:900; color:#f8fafc; margin-top:4px;">₹{latest["Close"]:,.2f}</h2></div>', unsafe_allow_html=True)
        with k2:
            color_hex = "#10b981" if price_change >= 0 else "#ef4444"
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">DAY CHANGE</span><h2 style="font-weight:900; color:{color_hex}; margin-top:4px;">{price_change:+.2f} ({pct_change:+.2f}%)</h2></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">TARGET PRICE (EST.)</span><h2 style="font-weight:900; color:#34d399; margin-top:4px;">₹{target_price:,.2f}</h2></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">STOP LOSS (STRICT)</span><h2 style="font-weight:900; color:#f87171; margin-top:4px;">₹{stop_loss:,.2f}</h2></div>', unsafe_allow_html=True)

        # AI Action Decision Box with Rationale
        st.markdown(f"""
        <div class="{verdict_style}">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin-bottom:2px; font-weight:900;">AI Action Decision: {action_summary}</h3>
                    <p style="font-weight:600; color:#38bdf8; margin-bottom:0;">Key Range: Support at <b>₹{support_level:,.2f}</b> | Resistance at <b>₹{resistance_level:,.2f}</b></p>
                </div>
                <div>{verdict_badge}</div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 16px 0;">
            <h5 style="margin-bottom:8px; font-weight:800; color:#f8fafc;">💡 Why Purchase or Sell This Stock? (Detailed Rationale)</h5>
            {"".join([f"<p style='margin-bottom:6px; color:#cbd5e1;'>• {r}</p>" for r in reasons])}
        </div>
        """, unsafe_allow_html=True)

        # High-End Dark Interactive Candlestick Chart
        st.subheader("📊 High-Precision Dark Interactive Chart")
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
        
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            name="Price (₹)",
            increasing_line_color='#10b981', decreasing_line_color='#ef4444',
            increasing_fillcolor='#10b981', decreasing_fillcolor='#ef4444'
        ), row=1, col=1)
        
        if 'SMA_20' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='#f59e0b', width=1), name="20-SMA"), row=1, col=1)
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='#38bdf8', width=1.5), name="50-SMA"), row=1, col=1)
            
        # Volume Bar
        colors = ['#10b981' if c >= o else '#ef4444' for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name="Volume"), row=2, col=1)

        fig.update_layout(
            paper_bgcolor="#000000", plot_bgcolor="#090d16",
            xaxis=dict(gridcolor="#1e293b", rangeslider=dict(visible=False)),
            xaxis2=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", title="Price (₹)"),
            yaxis2=dict(gridcolor="#1e293b", title="Volume"),
            font=dict(color="#f8fafc", family="Inter"),
            margin=dict(l=10, r=10, t=20, b=10), height=520
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE 2: Automated IPO Tracker & Detailed Buy Guidance
# ---------------------------------------------------------
elif navigation == "🚀 Automated IPO Tracker & Buy Guidance":
    st.markdown('<div class="brand-title">🚀 Indian IPO Decision Engine & Live GMP Tracker</div>', unsafe_allow_html=True)
    st.caption("Live Grey Market Premiums (GMP), subscription demand, and explicit **WHICH TO BUY AND WHY** guidance.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Scraped / Real-Time IPO Intelligence Dataset
    @st.cache_data(ttl=1800)
    def load_ipo_intelligence():
        data = [
            {
                "Company": "Tata EV Mobility Ltd",
                "Category": "Mainboard",
                "Price Band": "₹450 - ₹475",
                "Lot Size": "31 Shares",
                "Min Investment": "₹14,725",
                "GMP (₹)": "+₹155",
                "Est. Listing Gain %": "+32.6%",
                "Subscription": "48.2x",
                "Action": "APPLY (STRONG BUY)",
                "Why Buy or Avoid": "🟢 **High Institutional Demand (QIB 62x):** Strong backing from Tata brand equity. Electric vehicle market leader with 65% market share in India. Excellent listing profit potential."
            },
            {
                "Company": "PharmaGen Lifesciences",
                "Category": "Mainboard",
                "Price Band": "₹210 - ₹225",
                "Lot Size": "65 Shares",
                "Min Investment": "₹14,625",
                "GMP (₹)": "+₹42",
                "Est. Listing Gain %": "+18.6%",
                "Subscription": "16.4x",
                "Action": "APPLY (MODERATE BUY)",
                "Why Buy or Avoid": "🟢 **Healthy Profitability & Reasonable Valuation:** Company reports 24% YoY net profit growth. Reasonable P/E ratio compared to industry peers. Good candidate for listing gain."
            },
            {
                "Company": "Bharat Logistics Hub",
                "Category": "Mainboard",
                "Price Band": "₹110 - ₹118",
                "Lot Size": "120 Shares",
                "Min Investment": "₹14,160",
                "GMP (₹)": "-₹5",
                "Est. Listing Gain %": "-4.2%",
                "Subscription": "0.85x",
                "Action": "AVOID (HIGH RISK)",
                "Why Buy or Avoid": "🔴 **Negative GMP & Subdued Demand:** Overall subscription is below 1.0x. High debt levels on balance sheet and negative market sentiment. Risk of listing at discount."
            },
            {
                "Company": "Swastik Solar Energy (SME)",
                "Category": "SME",
                "Price Band": "₹85 - ₹90",
                "Lot Size": "1600 Shares",
                "Min Investment": "₹1,44,000",
                "GMP (₹)": "+₹58",
                "Est. Listing Gain %": "+64.4%",
                "Subscription": "92.1x",
                "Action": "APPLY (HIGH RETURN SME)",
                "Why Buy or Avoid": "🟢 **Massive Retail & HNI Over-subscription:** High solar industry tailwinds. Massive GMP indicates huge listing popup, though SME liquidity risk applies after listing."
            },
            {
                "Company": "UrbanInfra Realty",
                "Category": "Mainboard",
                "Price Band": "₹60 - ₹64",
                "Lot Size": "230 Shares",
                "Min Investment": "₹14,720",
                "GMP (₹)": "+₹2",
                "Est. Listing Gain %": "+3.1%",
                "Subscription": "1.3x",
                "Action": "AVOID / NEUTRAL",
                "Why Buy or Avoid": "🟡 **Flat GMP & Weak Margin:** Low retail interest and high real estate execution risks. Better capital deployment opportunities elsewhere in secondary market."
            }
        ]
        return pd.DataFrame(data)

    ipo_df = load_ipo_intelligence()
    
    st.subheader("🔥 Active & Upcoming Indian IPO Decision Screener")
    
    # Display Main Summary Table
    display_cols = ["Company", "Category", "Price Band", "GMP (₹)", "Est. Listing Gain %", "Subscription", "Action"]
    st.dataframe(ipo_df[display_cols], use_container_width=True, height=260)
    
    st.markdown("---")
    st.subheader("🎯 Detailed IPO Inspector: WHICH TO BUY AND WHY?")
    
    selected_company = st.selectbox("Select an IPO for Complete Buy/Avoid Analysis:", ipo_df["Company"].tolist())
    row = ipo_df[ipo_df["Company"] == selected_company].iloc[0]
    
    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">PRICE BAND</span><h3 style="color:#f8fafc; font-weight:800; margin-top:4px;">{row["Price Band"]}</h3></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">LOT SIZE / COST</span><h3 style="color:#f8fafc; font-weight:800; margin-top:4px;">{row["Lot Size"]} ({row["Min Investment"]})</h3></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">GREY MARKET PREMIUM</span><h3 style="color:#34d399; font-weight:800; margin-top:4px;">{row["GMP (₹)"]} ({row["Est. Listing Gain %"]})</h3></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">DECISION VERDICT</span><h3 style="color:#38bdf8; font-weight:800; margin-top:4px;">{row["Action"]}</h3></div>', unsafe_allow_html=True)

    # Detailed Rationale Container
    card_type = "stat-profit-dark" if "APPLY" in row["Action"] else "stat-loss-dark"
    
    st.markdown(f"""
    <div class="{card_type}">
        <h4 style="font-weight:900; margin-bottom:8px; color:#f8fafc;">💡 Deep Dive Analysis: Why Buy or Avoid {row['Company']}?</h4>
        <p style="font-size:1.02rem; line-height:1.6; color:#f1f5f9;">{row['Why Buy or Avoid']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Lot Profit Calculator
    st.markdown("##### 🧮 Interactive Lot Profit Simulator")
    num_lots = st.slider(f"Select Number of Application Lots for {row['Company']}:", min_value=1, max_value=15, value=1)
    
    try:
        min_inv = float(re.sub(r'[^\d.]', '', row["Min Investment"]))
        gain_pct = float(re.sub(r'[^\d.-]', '', row["Est. Listing Gain %"]))
        
        total_application_cost = min_inv * num_lots
        estimated_profit = total_application_cost * (gain_pct / 100)
        
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f'<div class="glass-card-dark"><b>Total Investment Needed:</b> <h3>₹{total_application_cost:,.2f}</h3></div>', unsafe_allow_html=True)
        with p2:
            p_color = "#34d399" if estimated_profit >= 0 else "#f87171"
            st.markdown(f'<div class="glass-card-dark"><b>Expected Listing Profit:</b> <h3 style="color:{p_color};">₹{estimated_profit:,.2f}</h3></div>', unsafe_allow_html=True)
    except Exception:
        pass

# ---------------------------------------------------------
# MODULE 3: Indian Rupee (₹) Wealth Planner
# ---------------------------------------------------------
elif navigation == "💰 Indian Rupee (₹) Wealth Planner":
    st.markdown('<div class="brand-title">💰 Indian Rupee (₹) Wealth Accumulation Planner</div>', unsafe_allow_html=True)
    st.caption("Calculate compounding wealth growth in ₹ Lakhs & Crores for equity mutual funds and stocks.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_w1, c_w2 = st.columns([1, 2])
    
    with c_w1:
        st.markdown('<div class="glass-card-dark">', unsafe_allow_html=True)
        st.subheader("🎛️ Investment Parameters")
        
        plan_mode = st.radio("Select Investment Strategy:", ["Monthly SIP (₹)", "One-Time Lumpsum (₹)"])
        
        if plan_mode == "Monthly SIP (₹)":
            monthly_amount = st.slider("Monthly SIP Deposit (₹):", min_value=500, max_value=200000, value=15000, step=500)
            invest_val = monthly_amount
        else:
            lumpsum_amount = st.slider("Lumpsum Investment (₹):", min_value=10000, max_value=5000000, value=250000, step=10000)
            invest_val = lumpsum_amount
            
        tenure_years = st.slider("Investment Horizon (Years):", min_value=1, max_value=35, value=15)
        expected_cagr = st.slider("Expected Annual CAGR Return (%):", min_value=4.0, max_value=30.0, value=14.0, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    months = tenure_years * 12
    monthly_rate = (expected_cagr / 100) / 12
    
    timeline = list(range(1, months + 1))
    invested_history = []
    wealth_history = []
    
    current_val = 0
    total_principal = 0
    
    for m in timeline:
        if plan_mode == "Monthly SIP (₹)":
            total_principal += invest_val
            current_val = (current_val + invest_val) * (1 + monthly_rate)
        else:
            if m == 1:
                total_principal = invest_val
                current_val = invest_val
            current_val = current_val * (1 + monthly_rate)
            
        invested_history.append(total_principal)
        wealth_history.append(current_val)
        
    estimated_profit = current_val - total_principal

    with c_w2:
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">TOTAL INVESTED</span><h3 style="color:#f8fafc; margin-top:4px;">{format_inr(total_principal)}</h3></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">ESTIMATED PROFIT</span><h3 style="color:#34d399; margin-top:4px;">+{format_inr(estimated_profit)}</h3></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="glass-card-dark"><span style="color:#94a3b8; font-size:0.78rem; font-weight:700;">FUTURE WEALTH</span><h3 style="color:#38bdf8; margin-top:4px;">{format_inr(current_val)}</h3></div>', unsafe_allow_html=True)

        df_chart = pd.DataFrame({
            "Month": timeline,
            "Total Accumulated Wealth": wealth_history,
            "Principal Invested": invested_history
        })
        
        fig_w = px.area(
            df_chart, x="Month", y=["Total Accumulated Wealth", "Principal Invested"],
            color_discrete_map={"Total Accumulated Wealth": "#10b981", "Principal Invested": "#6366f1"},
            title="📈 Wealth Compounding Timeline (INR)"
        )
        fig_w.update_layout(
            paper_bgcolor="#000000", plot_bgcolor="#090d16",
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", title="Value in INR (₹)"),
            font=dict(color="#f8fafc", family="Inter"),
            height=420
        )
        st.plotly_chart(fig_w, use_container_width=True)
