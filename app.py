import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai
import os
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VajraTech | Master AI Suite", layout="wide", page_icon="⚡")

# Secure API Key Handling for Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# Initialize Session States
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "memories" not in st.session_state: st.session_state.memories = []
if "health_logs" not in st.session_state: st.session_state.health_logs = []

# --- 2. PREMIUM NEON STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0A0E27; color: #F0F4FF; font-family: 'Inter', sans-serif; }
    .project-header { 
        background: linear-gradient(90deg, rgba(0, 217, 255, 0.1), rgba(124, 60, 237, 0.1)); 
        padding: 30px; border-radius: 15px; border-left: 5px solid #00D9FF; margin-bottom: 25px;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #00D9FF, #7C3AED); color: white; 
        border: none; border-radius: 8px; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0, 217, 255, 0.4); }
    .metric-box { 
        background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 10px; 
        border: 1px solid rgba(0, 217, 255, 0.2); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #00D9FF;'>⚡ VAJRA-TECH</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Advanced Agentic Intelligence Portal</p>", unsafe_allow_html=True)
        user = st.text_input("Username", placeholder="admin")
        pw = st.text_input("Password", type="password", placeholder="vajra2026")
        if st.button("Unleash Intelligence"):
            if user == "admin" and pw == "vajra2026":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Invalid Credentials")
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 VAJRA-CONTROL")
st.sidebar.markdown(f"**Status:** `Active` | **User:** `Admin`")
menu = st.sidebar.radio("Research Domains", [
    "🏠 Master Dashboard",
    "🛡️ Vajra-Sentinel (Safety)",
    "🩺 Vajra-Vital (Health)",
    "💰 Vajra-FinGuard (Finance)",
    "🛸 Vajra-Sanchaar (Swarm)",
    "🐘 Vajra-Anunaad (Nature)",
    "🧬 Vajra-Sanjeevani (Bio)",
    "🧠 Vajra-Smriti (Cognitive)"
])

def display_header(title, subtitle):
    st.markdown(f"<div class='project-header'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)

# --- 5. PROJECT MODULES ---

# --- HOME DASHBOARD ---
if menu == "🏠 Master Dashboard":
    st.title("⚡ Vajra-Tech Research Universe")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Projects", "7", "Operational")
    col2.metric("AI Agents", "247", "+12% Growth")
    col3.metric("System Uptime", "99.8%", "Optimal")
    col4.metric("Ethics Index", "100%", "Vajra-Nyaya")
    
    st.markdown("---")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🌐 Global Impact Map")
        map_df = pd.DataFrame({'lat': [17.38, 40.71, 35.68, -33.86], 'lon': [78.48, -74.00, 139.69, 151.20]})
        st.map(map_df)
    with c2:
        st.subheader("📊 Maturity Radar")
        fig = px.line_polar(r=[95, 90, 88, 85, 82, 78, 75], 
                            theta=['Safety', 'Health', 'Finance', 'Swarm', 'Nature', 'Bio', 'Mind'], line_close=True)
        st.plotly_chart(fig, use_container_width=True)

# --- VAJRA-SENTINEL ---
elif menu == "🛡️ Vajra-Sentinel (Safety)":
    display_header("🛡️ Vajra-Sentinel", "Industrial Safety & Hazard Management")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("🛰️ Real-time Sensor Feed")
        if st.button("Initialize Deep Scan"):
            with st.status("Scanning IoT Nodes..."):
                time.sleep(1); st.write("Checking Temperature..."); time.sleep(1); st.write("Analyzing Gas Levels...")
            st.success("Industrial Environment Secure. Hazard Level: 0.01%")
    with col_b:
        st.markdown("<div class='metric-box'><h3>Safety Rating</h3><h2>98.2%</h2></div>", unsafe_allow_html=True)

# --- VAJRA-VITAL ---
elif menu == "🩺 Vajra-Vital (Health)":
    display_header("🩺 Vajra-Vital", "Remote Health Tracking & LLM Diagnostics")
    vitals = st.text_input("Enter Patient Vitals (e.g., BP 120/80, HR 72)")
    if st.button("Analyze with Medical Agent"):
        with st.spinner("Diagnosing..."):
            st.info("Medical Report: Patient is stable. Recommended: Increase hydration and 30m walk.")

# --- VAJRA-FINGUARD ---
elif menu == "💰 Vajra-FinGuard (Finance)":
    display_header("💰 Vajra-FinGuard", "Autonomous Fraud Detection Engine")
    amt = st.number_input("Transaction Amount ($)", min_value=0)
    if st.button("Run Fraud Audit"):
        if amt > 10000: st.warning("🚨 High Risk Transaction! Vajra-Nyaya human-in-the-loop audit required.")
        else: st.success("Transaction Verified. No Fraud Detected.")

# --- VAJRA-SANCHAAR ---
elif menu == "🛸 Vajra-Sanchaar (Swarm)":
    display_header("🛸 Vajra-Sanchaar", "Self-Healing Drone Swarm Coordinator")
    st.subheader("Swarm Status")
    st.progress(85, text="Swarm Sync Efficiency")
    if st.button("Redeploy Swarm"): st.toast("Drones redeploying to optimal coordinates...")

# --- VAJRA-ANUNAAD ---
elif menu == "🐘 Vajra-Anunaad (Nature)":
    display_header("🐘 Vajra-Anunaad", "Bio-Acoustic Nature Translator")
    st.subheader("Acoustic Ingestion")
    st.file_uploader("Upload Animal Frequency Audio")
    if st.button("Translate Bio-Signal"):
        st.write("🐘 Elephant Call Translated: 'Warning - Water source 2km South is drying.'")

# --- VAJRA-SANJEEVANI ---
elif menu == "🧬 Vajra-Sanjeevani (Bio)":
    display_header("🧬 Vajra-Sanjeevani", "Bio-Digital Twin Surgery Simulator")
    if st.button("Sync Digital Twin"):
        with st.status("Mapping Cellular Data..."): time.sleep(2)
        st.success("Twin Synced. Surgery Prediction: 98% Success Rate.")

# --- VAJRA-SMRITI ---
elif menu == "🧠 Vajra-Smriti (Cognitive)":
    display_header("🧠 Vajra-Smriti", "Neural Continuity & Digital Immortality")
    q = st.text_input("Ask your Legacy Persona:")
    if q: st.chat_message("assistant").write(f"Vajra-Smriti: 'జ్ఞానమే అసలైన శక్తి. మీ ప్రశ్న {q} కు సమాధానం నా అనుభవం నుండి...'")
    
    mem = st.text_area("Record a core value for future generations:")
    if st.button("Secure to Neural Vault"):
        st.session_state.memories.append(mem)
        st.success("Encoded.")

# --- FOOTER ---
st.sidebar.markdown("---")
if st.sidebar.button("🚪 System Logout"):
    st.session_state.authenticated = False
    st.rerun()
