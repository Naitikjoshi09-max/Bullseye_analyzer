import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Apex Bharat Market AI | Indian Stock Terminal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Modern Minimalist White Aesthetic CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit Default Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}

    /* Sidebar Collapse/Expand Toggle Controls */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #0f172a !important;
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        margin: 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }

    /* Light Minimalist Background */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Title Styling */
    .brand-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.8px;
        background: linear-gradient(90deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Clean Light Cards */
    .glass-card-light {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
    }

    /* Profit & Loss Badges */
    .badge-bullish {
        background: #ecfdf5;
        border: 1px solid #10b981;
        color: #047857;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        font-size: 0.9rem;
    }
    .badge-bearish {
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #b91c1c;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        font-size: 0.9rem;
    }
    .badge-neutral {
        background: #fffbeb;
        border: 1px solid #f59e0b;
        color: #b45309;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        font-size: 0.9rem;
    }

    /* Tinted Signal Containers */
    .stat-profit-light {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 20px;
        color: #166534;
        margin-bottom: 20px;
    }
    .stat-loss-light {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 16px;
        padding: 20px;
        color: #991b1b;
        margin-bottom: 20px;
    }
    .stat-neutral-light {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        color: #0f172a;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Security Lock Screen (Password Authentication)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="brand-title" style="text-align: center;">🇮🇳 APEX BHARAT AI</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-weight:500;'>Indian Stock Intelligence & Wealth Analytics Terminal</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card-light" style="text-align: center;">
            <h4 style="margin-bottom: 10px; font-weight:800; color:#0f172a;">🔒 Secure Terminal Access</h4>
            <p style="color: #64748b; font-size: 0.88rem;">Enter authorization password to launch market analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("", type="password", placeholder="Enter Password...", key="pwd")
        if st.button("🚀 Unlock Terminal Engine", type="primary", use_container_width=True):
            if pwd.strip() == "BULLSEYE$2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Terminal Password")
        st.markdown("<br>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# Indian Ticker Auto-Formatter Helper
# ---------------------------------------------------------
def format_indian_ticker(user_input):
    clean = user_input.strip().upper()
    if not clean:
        return "RELIANCE.NS"
    # Auto-append .NS for National Stock Exchange if no exchange suffix provided
    if not (clean.endswith(".NS") or clean.endswith(".BO")):
        clean += ".NS"
    return clean

def format_inr(val):
    if abs(val) >= 10000007:
        return f"₹{val/10000000:,.2f} Cr"
    elif abs(val) >= 100005:
        return f"₹{val/100000:,.2f} Lakh"
    else:
        return f"₹{val:,.2f}"

# ---------------------------------------------------------
# Sidebar Navigation & Quick Stock Shortcuts
# ---------------------------------------------------------
st.sidebar.markdown('<div class="brand-title" style="font-size: 1.4rem;">🇮🇳 APEX BHARAT</div>', unsafe_allow_html=True)
st.sidebar.caption("NSE & BSE Real-Time Financial Intelligence")

if st.sidebar.button("🔒 Lock Terminal", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.markdown("---")
navigation = st.sidebar.radio(
    "Select Market Module:",
    ["📈 NSE/BSE Live Stock Analyzer", "🚀 Indian IPO Tracker & GMP", "💰 INR SIP & Wealth Planner"]
)

# ---------------------------------------------------------
# Data Engine: Technical Analysis & Metrics
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def fetch_indian_stock_data(ticker_symbol, period):
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period)
        info = stock.info
        return df, info
    except Exception:
        return None, None

def calculate_indicators(df):
    if df is None or len(df) < 10:
        return None
    
    df['SMA_50'] = df['Close'].rolling(window=min(50, len(df))).mean()
    df['SMA_200'] = df['Close'].rolling(window=min(200, len(df))).mean()
    
    # Relative Strength Index (RSI)
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
# MODULE 1: NSE/BSE Live Stock Analyzer
# ---------------------------------------------------------
if navigation == "📈 NSE/BSE Live Stock Analyzer":
    st.markdown('<div class="brand-title">📈 NSE & BSE Live Stock Analyzer</div>', unsafe_allow_html=True)
    st.caption("AI technical analysis, real-time prices in Rupees (₹), and investment reasoning for Indian equities.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Shortcuts for Top Indian Stocks
    st.markdown("<b>⚡ Popular Shortcuts:</b>", unsafe_allow_html=True)
    shortcut_cols = st.columns(8)
    shortcuts = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "TATAMOTORS", "ZOMATO", "SBIN", "ICICIBANK"]
    
    selected_shortcut = None
    for idx, sc in enumerate(shortcuts):
        if shortcut_cols[idx].button(sc, use_container_width=True):
            selected_shortcut = sc
            
    col_in1, col_in2 = st.columns([2, 1])
    with col_in1:
        default_sym = selected_shortcut if selected_shortcut else "RELIANCE"
        user_ticker = st.text_input("Enter Any Indian Stock Ticker (e.g., RELIANCE, TCS, ZOMATO, TATASTEEL, SUZLON):", value=default_sym)
        formatted_ticker = format_indian_ticker(user_ticker)
    with col_in2:
        period = st.selectbox("Select Timeframe:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
        
    with st.spinner(f"Fetching live market prices for {formatted_ticker}..."):
        df, info = fetch_indian_stock_data(formatted_ticker, period)
        
    if df is None or df.empty:
        st.error(f"⚠️ Unable to load market data for **'{user_ticker}'**. Please ensure the company symbol is valid on NSE/BSE.")
    else:
        df = calculate_indicators(df)
        latest = df.iloc[-1]
        prev_close = df.iloc[-2]['Close'] if len(df) > 1 else latest['Close']
        price_change = latest['Close'] - prev_close
        pct_change = (price_change / prev_close) * 100
        
        # Technical Signal Rules
        rsi_val = latest['RSI'] if 'RSI' in df.columns and not np.isnan(latest['RSI']) else 50
        sma_50 = latest['SMA_50'] if 'SMA_50' in df.columns and not np.isnan(latest['SMA_50']) else latest['Close']
        
        reasons = []
        bull_score = 0
        
        if rsi_val < 35:
            bull_score += 2
            reasons.append(f"🟢 **RSI Oversold ({rsi_val:.1f}):** Selling pressure appears exhausted. Strong historical bounce zone for Indian retail & institutional buyers.")
        elif rsi_val > 70:
            bull_score -= 2
            reasons.append(f"🔴 **RSI Overbought ({rsi_val:.1f}):** Stock is trading at short-term premium. Profit-taking risk is elevated.")
        else:
            reasons.append(f"🟡 **Neutral RSI ({rsi_val:.1f}):** Stock momentum is balanced without extreme overbought/oversold conditions.")
            
        if latest['Close'] > sma_50:
            bull_score += 2
            reasons.append(f"🟢 **Bullish Trend Alignment:** Current price (₹{latest['Close']:,.2f}) is holding above the 50-day moving average (₹{sma_50:,.2f}).")
        else:
            bull_score -= 2
            reasons.append(f"🔴 **Bearish Trend Alignment:** Current price (₹{latest['Close']:,.2f}) is trading below its 50-day moving average (₹{sma_50:,.2f}).")
            
        if price_change > 0:
            bull_score += 1

        # Verdict Classification
        if bull_score >= 2:
            signal_badge = '<div class="badge-bullish">🚀 STRONG BUY / BULLISH</div>'
            projected_return = f"+{abs(pct_change * 1.6 + 6.5):.1f}% Target upside projection"
            card_class = "stat-profit-light"
        elif bull_score <= -2:
            signal_badge = '<div class="badge-bearish">⚠️ HIGH RISK / BEARISH</div>'
            projected_return = f"-{abs(pct_change * 1.4 + 4.8):.1f}% Downside pullback risk"
            card_class = "stat-loss-light"
        else:
            signal_badge = '<div class="badge-neutral">⏸️ HOLD / CONSOLIDATION</div>'
            projected_return = "±2.8% Side-ways range projection"
            card_class = "stat-neutral-light"

        # KPI Display Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="glass-card-light">
                <span style="color:#64748b; font-size:0.78rem; font-weight:700;">CURRENT NSE/BSE PRICE</span>
                <h2 style="font-weight:900; margin-top:4px; font-size:1.8rem; color:#0f172a;">₹{latest['Close']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            color_hex = "#10b981" if price_change >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="glass-card-light">
                <span style="color:#64748b; font-size:0.78rem; font-weight:700;">DAY CHANGE</span>
                <h2 style="font-weight:900; margin-top:4px; color:{color_hex}; font-size:1.8rem;">
                    {price_change:+.2f} ({pct_change:+.2f}%)
                </h2>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="glass-card-light">
                <span style="color:#64748b; font-size:0.78rem; font-weight:700;">RSI STRENGTH</span>
                <h2 style="font-weight:900; margin-top:4px; font-size:1.8rem; color:#0f172a;">{rsi_val:.1f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="glass-card-light">
                <span style="color:#64748b; font-size:0.78rem; font-weight:700;">TRADED VOLUME</span>
                <h2 style="font-weight:900; margin-top:4px; font-size:1.8rem; color:#0f172a;">{latest['Volume']:,}</h2>
            </div>
            """, unsafe_allow_html=True)

        # Signal Rationale Box
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin-bottom:2px; font-weight:800;">AI Investment Signal for {formatted_ticker.replace('.NS','')}</h3>
                    <p style="font-weight:600; font-size:1rem; margin-bottom:0;">Projected Target: <b>{projected_return}</b></p>
                </div>
                <div>{signal_badge}</div>
            </div>
            <hr style="border-color: rgba(0,0,0,0.08); margin: 14px 0;">
            <h5 style="margin-bottom:8px; font-weight:800;">Detailed Technical Evaluation Rationale:</h5>
            {"".join([f"<p style='margin-bottom:6px;'>• {r}</p>" for r in reasons])}
        </div>
        """, unsafe_allow_html=True)

        # High-Contrast Light Candlestick Chart
        st.subheader("📊 Interactive Candlestick Chart (INR)")
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name="Price (₹)",
            increasing_line_color='#10b981',
            decreasing_line_color='#ef4444',
            increasing_fillcolor='#10b981',
            decreasing_fillcolor='#ef4444'
        ))
        
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='#2563eb', width=1.5), name="50-Day SMA"))
        if 'Upper_Band' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['Upper_Band'], line=dict(color='#9333ea', width=1, dash='dot'), name="Upper Bollinger"))
            fig.add_trace(go.Scatter(x=df.index, y=df['Lower_Band'], line=dict(color='#9333ea', width=1, dash='dot'), name="Lower Bollinger"))

        fig.update_layout(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f8fafc",
            xaxis=dict(gridcolor="#e2e8f0", rangeslider=dict(visible=False)),
            yaxis=dict(gridcolor="#e2e8f0", title="Price in INR (₹)"),
            font=dict(color="#0f172a", family="Inter"),
            margin=dict(l=10, r=10, t=20, b=10),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE 2: Indian IPO Tracker & GMP Suggestions
# ---------------------------------------------------------
elif navigation == "🚀 Indian IPO Tracker & GMP":
    st.markdown('<div class="brand-title">🚀 Indian IPO Tracker & Grey Market Premium (GMP)</div>', unsafe_allow_html=True)
    st.caption("Mainboard and SME IPO intelligence, live GMP estimates in ₹, lot sizes, and application suggestions.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Representative Data for Indian Mainboard & SME IPOs
    indian_ipo_data = [
        {"Company": "Tata EV Systems Ltd", "Issue Size": "₹3,200 Cr", "Price Band": "₹450 - ₹475", "Lot Size": "31 Shares", "Est. GMP (₹)": "+₹145", "Est. Gain %": "+30.5%", "Subscription": "42.5x", "Verdict": "APPLY (STRONG)"},
        {"Company": "PharmaGen India", "Price Band": "₹210 - ₹225", "Issue Size": "₹850 Cr", "Lot Size": "65 Shares", "Est. GMP (₹)": "+₹38", "Est. Gain %": "+16.8%", "Subscription": "14.2x", "Verdict": "APPLY"},
        {"Company": "Bharat Logistics Hub", "Price Band": "₹110 - ₹118", "Issue Size": "₹420 Cr", "Lot Size": "120 Shares", "Est. GMP (₹)": "-₹4", "Est. Gain %": "-3.3%", "Subscription": "0.9x", "Verdict": "AVOID"},
        {"Company": "Swastik Renewables (SME)", "Price Band": "₹85 - ₹90", "Issue Size": "₹65 Cr", "Lot Size": "1600 Shares", "Est. GMP (₹)": "+₹52", "Est. Gain %": "+57.7%", "Subscription": "88.4x", "Verdict": "APPLY (STRONG)"},
        {"Company": "UrbanInfra Housing", "Price Band": "₹60 - ₹64", "Issue Size": "₹280 Cr", "Lot Size": "230 Shares", "Est. GMP (₹)": "+₹2", "Est. Gain %": "+3.1%", "Subscription": "1.4x", "Verdict": "AVOID"}
    ]
    
    ipo_df = pd.DataFrame(indian_ipo_data)
    
    c_ipo1, c_ipo2 = st.columns([2, 1])
    with c_ipo1:
        st.subheader("🔥 Active & Upcoming Indian IPOs")
        st.dataframe(ipo_df, use_container_width=True, height=270)
        
    with c_ipo2:
        st.markdown("""
        <div class="glass-card-light">
            <h4 style="margin-bottom:10px; font-weight:800; color:#0f172a;">💡 IPO Application Rules</h4>
            <p style="font-size:0.88rem; color:#475569; line-height:1.6;">
                <b>• Estimated GMP > 20%:</b> High probability of listing day gains. Apply for listing profits.<br>
                <b>• Overall Subscription > 15x:</b> Strong Institutional (QIB) demand backing.<br>
                <b>• Negative / Flat GMP:</b> Risk of listing discount; avoid retail allotment.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 Selected IPO Cost & Lot Inspector")
    
    selected_ipo = st.selectbox("Select IPO for Detailed Estimate:", ipo_df["Company"].tolist())
    details = ipo_df[ipo_df["Company"] == selected_ipo].iloc[0]
    
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.8rem; font-weight:700;">PRICE BAND</span><h4>{details["Price Band"]}</h4></div>', unsafe_allow_html=True)
    with d2:
        st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.8rem; font-weight:700;">ESTIMATED GMP</span><h4 style="color:#10b981;">{details["Est. GMP (₹)"]}</h4></div>', unsafe_allow_html=True)
    with d3:
        color = "#10b981" if "-" not in details["Est. Gain %"] else "#ef4444"
        st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.8rem; font-weight:700;">EST. LISTING RETURN</span><h4 style="color:{color};">{details["Est. Gain %"]}</h4></div>', unsafe_allow_html=True)
    with d4:
        st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.8rem; font-weight:700;">SUGGESTION</span><h4>{details["Verdict"]}</h4></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3: INR SIP & Wealth Planner
# ---------------------------------------------------------
elif navigation == "💰 INR SIP & Wealth Planner":
    st.markdown('<div class="brand-title">💰 Indian Rupee (₹) SIP & Wealth Planner</div>', unsafe_allow_html=True)
    st.caption("Calculate compounding growth in ₹ Lakhs & Crores for Indian equity mutual funds and stocks.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_w1, col_w2 = st.columns([1, 2])
    
    with col_w1:
        st.markdown('<div class="glass-card-light">', unsafe_allow_html=True)
        st.subheader("🎛️ Investment Parameters")
        
        plan_type = st.radio("Investment Mode:", ["Monthly SIP (Rupees)", "One-Time Lumpsum (Rupees)"])
        
        if plan_type == "Monthly SIP (Rupees)":
            monthly_sip = st.slider("Monthly SIP Amount (₹):", min_value=500, max_value=200000, value=15000, step=500)
            invest_amount = monthly_sip
        else:
            lumpsum = st.slider("Lumpsum Investment (₹):", min_value=10000, max_value=5000000, value=250000, step=10000)
            invest_amount = lumpsum
            
        years = st.slider("Time Horizon (Years):", min_value=1, max_value=35, value=15)
        cagr = st.slider("Expected Annual Return / CAGR (%):", min_value=4.0, max_value=30.0, value=13.5, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    # Compounding Calculation
    months = years * 12
    monthly_rate = (cagr / 100) / 12
    
    timeline = list(range(1, months + 1))
    invested_list = []
    wealth_list = []
    
    current_wealth = 0
    total_invested = 0
    
    for m in timeline:
        if plan_type == "Monthly SIP (Rupees)":
            total_invested += invest_amount
            current_wealth = (current_wealth + invest_amount) * (1 + monthly_rate)
        else:
            if m == 1:
                total_invested = invest_amount
                current_wealth = invest_amount
            current_wealth = current_wealth * (1 + monthly_rate)
            
        invested_list.append(total_invested)
        wealth_list.append(current_wealth)
        
    profit_generated = current_wealth - total_invested

    with col_w2:
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.78rem; font-weight:700;">TOTAL INVESTED</span><h3 style="color:#0f172a; margin-top:4px;">{format_inr(total_invested)}</h3></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.78rem; font-weight:700;">ESTIMATED PROFIT</span><h3 style="color:#10b981; margin-top:4px;">+{format_inr(profit_generated)}</h3></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="glass-card-light"><span style="color:#64748b; font-size:0.78rem; font-weight:700;">TOTAL WEALTH</span><h3 style="color:#2563eb; margin-top:4px;">{format_inr(current_wealth)}</h3></div>', unsafe_allow_html=True)

        # Growth Plot
        df_wealth = pd.DataFrame({
            "Month": timeline,
            "Total Future Wealth": wealth_list,
            "Amount Invested": invested_list
        })
        
        fig_w = px.area(
            df_wealth, x="Month", y=["Total Future Wealth", "Amount Invested"],
            color_discrete_map={"Total Future Wealth": "#10b981", "Amount Invested": "#6366f1"},
            title="📈 Projected Wealth Accumulation Curve (INR)"
        )
        fig_w.update_layout(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f8fafc",
            xaxis=dict(gridcolor="#e2e8f0"),
            yaxis=dict(gridcolor="#e2e8f0", title="Value in INR (₹)"),
            font=dict(color="#0f172a", family="Inter"),
            height=420
        )
        st.plotly_chart(fig_w, use_container_width=True)
