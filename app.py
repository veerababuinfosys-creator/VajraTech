import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="VajraTech | Master AI Portfolio",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="auto"
)

# --- 2. SESSION STATE FOR AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Dummy credentials (replace with real auth in production)
VALID_CREDENTIALS = {
    "admin": "vajra2026",
    "researcher": "quantum001",
    "innovator": "lightning777"
}

# --- 3. PREMIUM THEME & STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Orbitron:wght@400;700;900&display=swap');
    
    :root {
        --primary: #00D9FF;
        --secondary: #7C3AED;
        --dark-bg: #0A0E27;
        --darker-bg: #050812;
        --accent: #FF006E;
        --text-main: #F0F4FF;
        --text-secondary: #A0B4D9;
        --electric: #00FFD9;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1a3e 50%, #0d0d2b 100%);
        color: var(--text-main);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* ELECTRIC GLOW EFFECT */
    .main-title {
        font-size: 72px;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, #00D9FF, #7C3AED, #FF006E);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 8s ease infinite;
        text-align: center;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
        margin: 30px 0;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-title {
        font-size: 18px;
        text-align: center;
        color: var(--electric);
        margin-bottom: 30px;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    /* PROJECT HEADER WITH NEON BORDER */
    .project-header {
        background: rgba(122, 60, 237, 0.08);
        padding: 30px;
        border-radius: 12px;
        border: 2px solid;
        border-image: linear-gradient(135deg, #00D9FF, #7C3AED, #FF006E) 1;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.15), inset 0 0 20px rgba(122, 60, 237, 0.1);
        margin-bottom: 30px;
    }
    
    .project-header h1 {
        color: var(--primary);
        font-family: 'Orbitron', monospace;
        font-size: 42px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .project-header p {
        color: var(--text-secondary);
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    
    /* CARDS WITH GLASSMORPHISM */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.1);
    }
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(13, 13, 43, 0.95) 100%);
        border-right: 2px solid rgba(0, 217, 255, 0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--primary);
    }
    
    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF, #7C3AED);
        color: #0A0E27;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        cursor: pointer;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 40px rgba(0, 217, 255, 0.6), 0 0 20px rgba(124, 60, 237, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* INPUT FIELDS */
    [data-testid="stTextInput"] input,
    [data-testid="stPasswordInput"] input,
    [data-testid="stSelectbox"] select {
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--text-main) !important;
        border: 1.5px solid rgba(0, 217, 255, 0.4) !important;
        border-radius: 8px;
        padding: 12px 15px;
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stPasswordInput"] input:focus,
    [data-testid="stSelectbox"] select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* RADIO & CHECKBOX */
    [data-testid="stRadio"] span {
        color: var(--text-secondary);
    }
    
    /* DIVIDER */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.4), transparent);
        margin: 30px 0;
    }
    
    /* TABS */
    [data-testid="stTabs"] [role="tab"] {
        color: var(--text-secondary);
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: var(--primary);
        border-bottom-color: var(--primary);
    }
    
    /* CUSTOM BADGE */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.2), rgba(124, 60, 237, 0.2));
        border: 1px solid var(--primary);
        color: var(--primary);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-right: 10px;
    }
    
    .status-active { color: #00FFD9; border-color: #00FFD9; }
    .status-warning { color: #FFB703; border-color: #FFB703; }
    .status-offline { color: #FF006E; border-color: #FF006E; }
    
    /* LOGIN PAGE CONTAINER */
    .login-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(-45deg, #0A0E27, #1a1a3e, #0d0d2b, #2a1a4e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .login-box {
        width: 100%;
        max-width: 420px;
        padding: 50px 40px;
        background: rgba(10, 14, 39, 0.8);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(0, 217, 255, 0.3);
        border-radius: 16px;
        box-shadow: 
            0 0 60px rgba(0, 217, 255, 0.2),
            0 0 40px rgba(124, 60, 237, 0.15),
            inset 0 0 20px rgba(0, 217, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .login-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 217, 255, 0.05) 50%,
            transparent 70%
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg) translateX(-100%); }
        100% { transform: rotate(0deg) translateX(100%); }
    }
    
    .login-title {
        font-family: 'Orbitron', monospace;
        font-size: 48px;
        background: linear-gradient(135deg, #00D9FF, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: 2px;
        font-weight: 900;
    }
    
    .login-subtitle {
        text-align: center;
        color: var(--electric);
        font-size: 13px;
        margin-bottom: 40px;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .login-input {
        width: 100%;
        padding: 14px 16px;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.08);
        border: 1.5px solid rgba(0, 217, 255, 0.4);
        border-radius: 10px;
        color: var(--text-main);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    
    .login-input:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .login-input::placeholder {
        color: rgba(160, 180, 217, 0.6);
    }
    
    .login-btn {
        width: 100%;
        padding: 14px;
        background: linear-gradient(135deg, #00D9FF, #7C3AED);
        color: #0A0E27;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Space Grotesk', sans-serif;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.4);
        margin-bottom: 20px;
        font-family: 'Orbitron', monospace;
    }
    
    .login-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 50px rgba(0, 217, 255, 0.6), 0 0 30px rgba(124, 60, 237, 0.4);
    }
    
    .login-btn:active {
        transform: translateY(-1px);
    }
    
    .error-msg {
        color: #FF006E;
        text-align: center;
        font-size: 13px;
        margin-bottom: 15px;
        padding: 10px;
        background: rgba(255, 0, 110, 0.1);
        border-left: 3px solid #FF006E;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .success-msg {
        color: #00FFD9;
        text-align: center;
        font-size: 13px;
        margin-bottom: 15px;
        padding: 10px;
        background: rgba(0, 255, 217, 0.1);
        border-left: 3px solid #00FFD9;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .login-footer {
        text-align: center;
        color: var(--text-secondary);
        font-size: 12px;
        margin-top: 20px;
        letter-spacing: 0.5px;
    }
    
    .lightning-icon {
        font-size: 60px;
        text-align: center;
        margin-bottom: 20px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* METRIC CARDS */
    .metric-card {
        background: rgba(122, 60, 237, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.2);
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--primary);
        margin: 10px 0;
        font-family: 'Orbitron', monospace;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 13px;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN PAGE ---
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="login-box">
                <div class="lightning-icon">⚡</div>
                <div class="login-title">VAJRA-TECH</div>
                <div class="login-subtitle">Advanced Agentic Intelligence Portal</div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_pass")
        
        col_a, col_b = st.columns(2)
        with col_a:
            login_btn = st.button("🔓 LOGIN", use_container_width=True, key="login_btn")
        with col_b:
            demo_btn = st.button("📊 DEMO", use_container_width=True, key="demo_btn")
        
        if login_btn:
            if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✨ Authentication successful! Redirecting...")
                st.rerun()
            else:
                st.markdown('<div class="error-msg">❌ Invalid credentials. Try admin/vajra2026</div>', unsafe_allow_html=True)
        
        if demo_btn:
            st.session_state.authenticated = True
            st.session_state.username = "Demo_User"
            st.rerun()
        
        st.markdown("""
                <div class="login-footer">
                    <p>🔐 Demo Credentials:</p>
                    <p><strong>admin</strong> / <strong>vajra2026</strong></p>
                    <p style="margin-top: 15px; font-size: 11px; opacity: 0.7;">© 2026 VajraTech Intelligence Labs</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MAIN APP ---
def show_main_app():
    # SIDEBAR NAVIGATION
    st.sidebar.title("🚀 VAJRA-TECH CONTROL")
    st.sidebar.markdown(f"**User:** `{st.session_state.username}`")
    st.sidebar.markdown("---")
    st.sidebar.info("7 విప్లవాత్మక ఏజెంటిక్ AI ప్రాజెక్టుల సమాహారం.")
    
    menu = st.sidebar.radio("Navigate Research Portfolio", [
        "🏠 Master Dashboard",
        "🛡️ Vajra-Sentinel (Industrial)",
        "🩺 Vajra-Vital (Health)",
        "💰 Vajra-FinGuard (Finance)",
        "🛸 Vajra-Sanchaar (Swarm AI)",
        "🐘 Vajra-Anunaad (Nature AI)",
        "🧬 Vajra-Sanjeevani (Bio-Twin)",
        "🧠 Vajra-Smriti (Cognitive)"
    ], label_visibility="collapsed")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    # HELPER FUNCTION
    def display_header(title, subtitle):
        st.markdown(f"<div class='project-header'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)
    
    # --- MASTER DASHBOARD ---
    if menu == "🏠 Master Dashboard":
        st.markdown("<div class='main-title'>⚡ VAJRA-TECH RESEARCH SUITE</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Advancing Humanity through Agentic Intelligence & Ethics</div>", unsafe_allow_html=True)
        
        # KEY METRICS
        st.markdown("### 📊 OPERATIONAL METRICS")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">ACTIVE PROJECTS</div>
                    <div class="metric-value">7</div>
                    <span class="badge status-active">OPERATIONAL</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">AI AGENTS</div>
                    <div class="metric-value">247</div>
                    <span class="badge status-active">ACTIVE</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">SYSTEM UPTIME</div>
                    <div class="metric-value">99.8%</div>
                    <span class="badge status-active">OPTIMAL</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">RESEARCH INDEX</div>
                    <div class="metric-value">94%</div>
                    <span class="badge status-warning">MATURE</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # GLOBAL IMPACT MAP
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌐 Global Impact Map")
            map_data = pd.DataFrame({
                'lat': [17.3850, 37.7749, 51.5074, 35.6762, -33.8688],
                'lon': [78.4867, -122.4194, -0.1278, 139.6503, 151.2093],
                'Project': ['Vajra-Vital', 'Vajra-Sentinel', 'Vajra-FinGuard', 'Vajra-Sanchaar', 'Vajra-Anunaad']
            })
            st.map(map_data)
        
        with col2:
            st.subheader("📈 Research Maturity Index")
            categories = ['Safety', 'Health', 'Finance', 'Robotics', 'Nature', 'Bio-Tech', 'Cognitive']
            values = [95, 90, 88, 85, 82, 78, 75]
            fig = px.line_polar(r=values, theta=categories, line_close=True)
            fig.update_traces(
                fill='toself',
                line_color='#00D9FF',
                fillcolor='rgba(0, 217, 255, 0.2)'
            )
            fig.update_layout(
                plot_bgcolor='rgba(10, 14, 39, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#A0B4D9',
                font_family='Space Grotesk',
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # PROJECT OVERVIEW
        st.markdown("### 🔬 ACTIVE PROJECTS OVERVIEW")
        
        projects_data = {
            '🛡️ Sentinel': {'Status': 'OPERATIONAL', 'Progress': 95, 'Focus': 'Industrial Safety'},
            '🩺 Vital': {'Status': 'OPERATIONAL', 'Progress': 90, 'Focus': 'Remote Health'},
            '💰 FinGuard': {'Status': 'OPERATIONAL', 'Progress': 88, 'Focus': 'Fraud Detection'},
            '🛸 Sanchaar': {'Status': 'TESTING', 'Progress': 85, 'Focus': 'Swarm Intelligence'},
            '🐘 Anunaad': {'Status': 'RESEARCH', 'Progress': 82, 'Focus': 'Bio-Acoustic AI'},
            '🧬 Sanjeevani': {'Status': 'DEVELOPMENT', 'Progress': 78, 'Focus': 'Bio-Digital Twin'},
            '🧠 Smriti': {'Status': 'CONCEPT', 'Progress': 75, 'Focus': 'Cognitive Continuity'},
        }
        
        for project, details in projects_data.items():
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.write(f"**{project}**")
            with col2:
                st.metric("Progress", f"{details['Progress']}%")
            with col3:
                st.write(f"Status: `{details['Status']}`")
    
    # --- PROJECT PAGES ---
    elif menu == "🛡️ Vajra-Sentinel (Industrial)":
        display_header("🛡️ Vajra-Sentinel", "Industrial Safety & Real-time IoT Monitoring")
        st.write("**Abstract:** పరిశ్రమల్లో ప్రమాదాలను సెకన్లలో గుర్తించి ఆటోమేటిక్ షట్‌డౌన్ చేసే AI ఏజెంట్ వ్యవస్థ.")
        st.markdown("---")
        st.markdown('<span class="badge status-active">LIVE DEPLOYMENT</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Sensors", "1,247")
        with col2:
            st.metric("Incidents Prevented", "3,847")
        st.button("🚀 Launch Full Sentinel Simulation")
    
    elif menu == "🩺 Vajra-Vital (Health)":
        display_header("🩺 Vajra-Vital", "Remote Health Tracking & LLM Diagnostics")
        st.write("**Abstract:** మారుమూల ప్రాంతాల్లో రోగుల ప్రాణాలను కాపాడే టెలి-మెడిసిన్ ఏజెంట్.")
        st.markdown("---")
        st.markdown('<span class="badge status-active">PILOT PHASE</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Patients Monitored", "5,432")
        with col2:
            st.metric("Early Diagnoses", "892")
    
    elif menu == "💰 Vajra-FinGuard (Finance)":
        display_header("💰 Vajra-FinGuard", "Autonomous Financial Fraud Prevention")
        st.write("**Abstract:** బ్యాంకింగ్ మోసాలను అడ్డుకునే నైతికత (Ethics) కలిగిన ఫైనాన్స్ ఏజెంట్.")
        st.markdown("---")
        st.markdown('<span class="badge status-active">PRODUCTION</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Transactions Analyzed", "847.2M")
        with col2:
            st.metric("Fraud Blocked", "$124.5B")
    
    elif menu == "🛸 Vajra-Sanchaar (Swarm AI)":
        display_header("🛸 Vajra-Sanchaar", "Self-Healing Drone Swarm Intelligence")
        st.write("**Abstract:** వందలాది డ్రోన్లు ఒకే లక్ష్యం కోసం సమన్వయంతో పనిచేసే ఆర్కిటెక్చర్.")
        st.markdown("---")
        st.markdown('<span class="badge status-warning">TESTING</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Drones Coordinated", "512")
        with col2:
            st.metric("Swarm Efficiency", "94.3%")
    
    elif menu == "🐘 Vajra-Anunaad (Nature AI)":
        display_header("🐘 Vajra-Anunaad", "Cross-Species Bio-Acoustic Translator")
        st.write("**Abstract:** జంతువుల భాషను అర్థం చేసుకుని ప్రకృతిని కాపాడే AI.")
        st.markdown("---")
        st.markdown('<span class="badge status-warning">RESEARCH</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Species Detected", "247")
        with col2:
            st.metric("Communication Decoded", "89.7%")
    
    elif menu == "🧬 Vajra-Sanjeevani (Bio-Twin)":
        display_header("🧬 Vajra-Sanjeevani", "Predictive Surgery & Bio-Digital Twin")
        st.write("**Abstract:** సర్జరీకి ముందే ఫలితాన్ని అంచనా వేసే డిజిటల్ ప్రతిరూపం.")
        st.markdown("---")
        st.markdown('<span class="badge status-warning">DEVELOPMENT</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Surgeries Simulated", "1,203")
        with col2:
            st.metric("Prediction Accuracy", "98.2%")
    
    elif menu == "🧠 Vajra-Smriti (Cognitive)":
        display_header("🧠 Vajra-Smriti", "Neural Continuity & Digital Legacy")
        st.write("**Abstract:** మానవ మేధస్సును మరియు వ్యక్తిత్వాన్ని అమరత్వానికి చేర్చే ప్రాజెక్ట్.")
        st.markdown("---")
        st.markdown('<span class="badge status-offline">CONCEPT</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Neural Maps Created", "47")
        with col2:
            st.metric("Continuity Index", "78.5%")
    
    # FOOTER
    st.markdown("---")
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        st.markdown("<p style='color: var(--text-secondary); font-size: 13px;'>© 2026 VajraTech Intelligence Labs | Private Research Portfolio</p>", unsafe_allow_html=True)
    with col_f2:
        st.markdown("<p style='color: var(--electric); font-size: 13px; text-align: right;'><strong>Status:</strong> ✅ OPERATIONAL</p>", unsafe_allow_html=True)

# --- 6. MAIN FLOW ---
if not st.session_state.authenticated:
    show_login()
else:
    show_main_app()
