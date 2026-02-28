import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai
import os
import time

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="Vajra-Tech | Advanced AI Labs", layout="wide", page_icon="⚡")

# Gemini AI Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ API Key missing! Please set GEMINI_API_KEY in Render Environment Variables.")

# Persistent Session State
if "memories" not in st.session_state: st.session_state.memories = []
if "auth" not in st.session_state: st.session_state.auth = False

# --- 2. THEME & UI (MIND-BLOWING VERSION) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Orbitron:wght@400;700;900&family=Inter:wght@100;300;400;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ANIMATED BACKGROUND */
    .main {
        background: linear-gradient(-45deg, #0a0f1f, #1a1f3a, #0d1b2a, #1a0033);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        color: #e0e8ff;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* GLOWING PARTICLES EFFECT */
    .main::before {
        content: '';
        position: fixed;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        z-index: -1;
        background: 
            radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(50px, -50px) scale(1.1); }
    }
    
    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #00d9ff, #7c3aed, #ff006e);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: color-shift 8s ease infinite;
        filter: drop-shadow(0 0 20px rgba(0, 217, 255, 0.3));
    }
    
    @keyframes color-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* GLASSMORPHISM CARDS */
    .stMetric {
        background: rgba(20, 30, 60, 0.4) !important;
        backdrop-filter: blur(20px);
        padding: 24px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        box-shadow: 
            0 0 30px rgba(0, 217, 255, 0.2),
            inset 0 0 20px rgba(124, 58, 237, 0.1);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .stMetric:hover {
        border-color: rgba(0, 217, 255, 0.7) !important;
        box-shadow: 
            0 0 50px rgba(0, 217, 255, 0.4),
            inset 0 0 30px rgba(124, 58, 237, 0.2),
            0 0 100px rgba(0, 217, 255, 0.1) !important;
        transform: translateY(-8px) scale(1.02);
    }
    
    /* AGENT RESPONSE STYLING */
    .agent-response {
        background: rgba(16, 22, 48, 0.6) !important;
        backdrop-filter: blur(25px);
        padding: 28px !important;
        border-radius: 14px !important;
        border: 2px solid transparent;
        border-image: linear-gradient(135deg, #7C3AED, #00D9FF, #FF006E) 1;
        box-shadow: 
            0 0 40px rgba(124, 58, 237, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 20px 0 !important;
        position: relative;
        overflow: hidden;
        animation: pulse-border 4s ease-in-out infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { box-shadow: 0 0 40px rgba(124, 58, 237, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
        50% { box-shadow: 0 0 60px rgba(0, 217, 255, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15); }
    }
    
    .agent-response::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00D9FF, #7C3AED, transparent);
        animation: scan-line 3s linear infinite;
    }
    
    @keyframes scan-line {
        0% { top: 0%; }
        100% { top: 100%; }
    }
    
    /* BUTTONS */
    .stButton > button {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 12px;
        padding: 14px 32px !important;
        background: linear-gradient(135deg, #7C3AED, #00D9FF) !important;
        border: 2px solid #00D9FF !important;
        color: white !important;
        border-radius: 10px !important;
        box-shadow: 0 0 25px rgba(0, 217, 255, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 0 50px rgba(0, 217, 255, 0.6), 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        border-color: #7C3AED !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* INPUTS & TEXT AREAS */
    .stTextInput input, .stTextArea textarea, .stSelectSlider {
        font-family: 'Space Mono', monospace !important;
        background: rgba(30, 40, 70, 0.5) !important;
        border: 1.5px solid rgba(0, 217, 255, 0.3) !important;
        color: #e0e8ff !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00D9FF !important;
        box-shadow: 
            0 0 30px rgba(0, 217, 255, 0.4),
            inset 0 0 15px rgba(0, 217, 255, 0.1) !important;
        background: rgba(20, 40, 80, 0.7) !important;
    }
    
    /* SIDEBAR */
    .stSidebar {
        background: rgba(10, 15, 31, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(0, 217, 255, 0.2);
    }
    
    .stSidebar .stRadio {
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        background: rgba(20, 30, 60, 0.3);
        transition: all 0.3s ease;
    }
    
    .stSidebar .stRadio:hover {
        background: rgba(20, 30, 60, 0.6);
        border-color: rgba(0, 217, 255, 0.6);
    }
    
    /* SUCCESS/WARNING/ERROR */
    .stSuccess {
        background: rgba(5, 150, 105, 0.15) !important;
        border: 1.5px solid #10b981 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2) !important;
    }
    
    .stWarning {
        background: rgba(217, 119, 6, 0.15) !important;
        border: 1.5px solid #f59e0b !important;
        border-radius: 10px !important;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.2) !important;
    }
    
    .stError {
        background: rgba(220, 38, 38, 0.15) !important;
        border: 1.5px solid #ef4444 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.2) !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1.5px solid #3b82f6 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* HEADERS */
    h1, .stHeader {
        animation: glow-pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow-pulse {
        0%, 100% { filter: drop-shadow(0 0 15px rgba(0, 217, 255, 0.3)); }
        50% { filter: drop-shadow(0 0 30px rgba(124, 58, 237, 0.5)); }
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7C3AED, #00D9FF, #FF006E) !important;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.4);
    }
    
    /* DIVIDER */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.5), transparent);
        margin: 30px 0;
    }
    
    /* TEXT STYLING */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    code {
        background: rgba(30, 40, 70, 0.6) !important;
        color: #00d9ff !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 6px !important;
        font-family: 'Space Mono', monospace !important;
        padding: 4px 8px !important;
    }
    
    /* CAPTION TEXT */
    .stCaption {
        color: rgba(224, 232, 255, 0.7);
        font-family: 'Space Mono', monospace;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN GATE ---
if not st.session_state.auth:
    st.title("🔐 Vajra-Tech Secure Access")
    u = st.text_input("Admin ID")
    p = st.text_input("Passkey", type="password")
    if st.button("Authorize"):
        if u == "admin" and p == "vajra2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. NAVIGATION ---
st.sidebar.title("🚀 VAJRA-CONTROL")
menu = st.sidebar.radio("Active Research", [
    "🏠 Dashboard", "🛡️ Sentinel (Safety)", "🩺 Vital (Health)", 
    "💰 FinGuard (Finance)", "🛸 Sanchaar (Swarm)", 
    "🐘 Anunaad (Nature)", "🧬 Sanjeevani (Bio)", "🧠 Smriti (Cognitive)"
])

# --- 5. ADVANCED AGENTIC MODULES ---

if menu == "🏠 Dashboard":
    st.title("⚡ Vajra-Tech Intelligence Labs")
    cols = st.columns(4)
    cols[0].metric("Global Nodes", "128", "Active")
    cols[1].metric("Neural Sync", "94%", "+2.1%")
    cols[2].metric("Agent Autonomy", "Level 4", "High")
    cols[3].metric("Ethics Audit", "Passed", "Verified")
    
    st.subheader("🌐 Impact Visualization")
    df = pd.DataFrame(np.random.randn(20, 2) / [50, 50] + [17.38, 78.48], columns=['lat', 'lon'])
    st.map(df)

elif menu == "🛡️ Sentinel (Safety)":
    st.header("🛡️ Vajra-Sentinel: Industrial Guardian")
    status = st.select_slider("Simulate Risk Level", options=["Low", "Medium", "High", "Critical"])
    if st.button("Execute Safety Audit"):
        with st.spinner("Agent analyzing telemetry..."):
            prompt = f"As an industrial safety AI, give a 2-line directive for {status} risk level in a chemical plant."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='agent-response'><b>Sentinel AI:</b> {response.text}</div>", unsafe_allow_html=True)

elif menu == "🩺 Vital (Health)":
    st.header("🩺 Vajra-Vital: Agentic Diagnosis")
    data = st.text_area("Enter Symptoms or Vitals (e.g., Blood Sugar 200, fatigue)")
    if st.button("Analyze Health"):
        with st.spinner("Consulting Medical Knowledge Base..."):
            prompt = f"Analyze these vitals: {data}. Provide a brief assessment and one precaution. (Disclaimer: Simulation only)"
            response = model.generate_content(prompt)
            st.info(response.text)

elif menu == "💰 FinGuard (Finance)":
    st.header("💰 Vajra-FinGuard: Fraud Neutralizer")
    tx_amt = st.number_input("Transaction Value ($)", min_value=0)
    if st.button("Verify Integrity"):
        risk = "HIGH" if tx_amt > 50000 else "LOW"
        prompt = f"Explain why a ${tx_amt} transaction is flagged as {risk} risk and what authentication is needed."
        response = model.generate_content(prompt)
        st.warning(response.text)

elif menu == "🛸 Sanchaar (Swarm)":
    st.header("🛸 Vajra-Sanchaar: Swarm Intelligence")
    st.write("Coordinating 50+ Autonomous Drones")
    target = st.text_input("Target Area (e.g., Flood Relief Sector A)")
    if st.button("Deploy Swarm"):
        st.success(f"Swarm recalculating trajectory for {target}...")
        st.json({"Drones": 54, "Sync_Level": "99.2%", "Status": "En Route"})

elif menu == "🐘 Anunaad (Nature)":
    st.header("🐘 Vajra-Anunaad: Bio-Acoustic Hub")
    audio_sim = st.slider("Frequency (Hz)", 10, 20000, 500)
    if st.button("Translate Signal"):
        prompt = f"Translate a nature sound at {audio_sim} Hz into a human-understandable environmental alert."
        response = model.generate_content(prompt)
        st.success(f"Nature Agent: {response.text}")

elif menu == "🧬 Sanjeevani (Bio)":
    st.header("🧬 Vajra-Sanjeevani: Bio-Twin Simulator")
    dna_seq = st.text_input("Simulate DNA Marker", "ATCG-X22")
    if st.button("Run Simulation"):
        st.write(f"Predicting therapy response for marker {dna_seq}...")
        st.progress(88)
        st.write("Efficacy: 91.4% | Side-effect Risk: 2.1%")

elif menu == "🧠 Smriti (Cognitive)":
    st.header("🧠 Vajra-Smriti: Neural Continuity")
    thought = st.text_area("Ingest new memory or value:")
    if st.button("Archive to Vault"):
        st.session_state.memories.append({"time": time.ctime(), "content": thought})
        st.success("Memory block encrypted and added to Digital Legacy.")
    
    st.subheader("📜 Neural Vault History")
    for m in st.session_state.memories:
        st.caption(f"[{m['time']}] {m['content']}")

# --- FOOTER ---
st.sidebar.markdown("---")
if st.sidebar.button("System Shutdown"):
    st.session_state.auth = False
    st.rerun()
