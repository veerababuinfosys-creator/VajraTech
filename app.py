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

# --- 2. THEME & UI ---
st.markdown("""
    <style>
    .main { background-color: #050A18; color: #E0E0E0; }
    .stMetric { background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid #00D9FF; }
    .agent-response { background: #101630; padding: 20px; border-radius: 10px; border-left: 5px solid #7C3AED; margin: 10px 0; }
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
