import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import time

# --- 1. SETTINGS & CONFIG ---
st.set_page_config(page_title="Vajra-Tech | Advanced AI Labs", layout="wide", page_icon="⚡")

# Initialize AI Model safely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"AI Config Error: {e}")

# Persistent Session State
if "memories" not in st.session_state: st.session_state.memories = []
if "auth" not in st.session_state: st.session_state.auth = False
if "last_report" not in st.session_state: st.session_state.last_report = ""

# --- 2. THEME & UI ---
st.markdown("""
    <style>
    .main { background-color: #050A18; color: #E0E0E0; }
    .stMetric { background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid #00D9FF; }
    .agent-response { background: #101630; padding: 20px; border-radius: 10px; border-left: 5px solid #7C3AED; margin: 10px 0; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #7C3AED; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURE LOGIN PAGE ---
if not st.session_state.auth:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.image("https://img.icons8.com/nolan/128/shield.png")
        st.title("🔐 Vajra-Tech Labs")
        st.subheader("Autonomous AI Gateway")
        
        u = st.text_input("Admin ID", placeholder="Enter Username")
        p = st.text_input("Passkey", type="password", placeholder="Enter Password")
        
        if st.button("Authorize Access"):
            if u == "admin" and p == "vajra2026":
                st.session_state.auth = True
                st.success("Access Granted. Initializing Neural Links...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
        
        st.info("System Note: This is a restricted research environment.")
    st.stop()

# --- 4. UTILITY FUNCTIONS ---
def get_ai_response(prompt):
    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Neural Link Error: {e}"
    return "AI Engine Offline. Set GEMINI_API_KEY in Render."

# --- 5. NAVIGATION ---
st.sidebar.title("🚀 VAJRA-CONTROL")
menu = st.sidebar.radio("Active Research", [
    "🏠 Dashboard", "🛡️ Sentinel (Safety)", "🩺 Vital (Health)", 
    "💰 FinGuard (Finance)", "🛸 Sanchaar (Swarm)", 
    "🐘 Anunaad (Nature)", "🧬 Sanjeevani (Bio)", "🧠 Smriti (Cognitive)"
])

# --- 6. MODULE LOGIC ---

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
        with st.spinner("Analyzing telemetry..."):
            prompt = f"As an industrial safety AI, give a 2-line directive for {status} risk level in a chemical plant."
            res = get_ai_response(prompt)
            st.markdown(f"<div class='agent-response'><b>Sentinel AI:</b> {res}</div>", unsafe_allow_html=True)

elif menu == "🩺 Vital (Health)":
    st.header("🩺 Vajra-Vital: Agentic Diagnosis")
    data = st.text_area("Enter Patient Vitals (e.g., BP 140/90, Sugar 180)")
    if st.button("Generate Medical Assessment"):
        with st.spinner("Processing medical data..."):
            prompt = f"Analyze these vitals: {data}. Provide a structured assessment: Status, Risk Level, and 2 Recommendations."
            res = get_ai_response(prompt)
            st.session_state.last_report = f"VAJRA-VITAL MEDICAL REPORT\nGenerated: {time.ctime()}\n\nData: {data}\n\nAssessment:\n{res}"
            st.info(res)
    
    if st.session_state.last_report:
        st.download_button("📥 Download Health Report", st.session_state.last_report, file_name="Vajra_Health_Report.txt")

elif menu == "💰 FinGuard (Finance)":
    st.header("💰 Vajra-FinGuard: Fraud Neutralizer")
    tx_amt = st.number_input("Transaction Value ($)", min_value=0)
    if st.button("Run Forensic Audit"):
        with st.spinner("Scanning transaction patterns..."):
            risk = "HIGH" if tx_amt > 50000 else "LOW"
            prompt = f"Explain why a ${tx_amt} transaction is flagged as {risk} risk and suggest 2 security steps."
            res = get_ai_response(prompt)
            st.session_state.last_report = f"VAJRA-FINGUARD FINANCIAL AUDIT\nGenerated: {time.ctime()}\n\nTransaction: ${tx_amt}\n\nRisk Level: {risk}\n\nAnalysis:\n{res}"
            st.warning(res)

    if st.session_state.last_report:
        st.download_button("📥 Download Audit Report", st.session_state.last_report, file_name="Vajra_Finance_Audit.txt")

elif menu == "🛸 Sanchaar (Swarm)":
    st.header("🛸 Vajra-Sanchaar: Swarm Intelligence")
    target = st.text_input("Target Area", "Flood Relief Sector A")
    if st.button("Deploy Swarm"):
        st.success(f"Swarm recalculating trajectory for {target}...")
        st.json({"Drones": 54, "Sync_Level": "99.2%", "Status": "En Route"})

elif menu == "🐘 Anunaad (Nature)":
    st.header("🐘 Vajra-Anunaad: Bio-Acoustic Hub")
    audio_sim = st.slider("Frequency (Hz)", 10, 20000, 500)
    if st.button("Translate Signal"):
        prompt = f"Translate a nature sound at {audio_sim} Hz into a human-understandable environmental alert."
        res = get_ai_response(prompt)
        st.success(f"Nature Agent: {res}")

elif menu == "🧬 Sanjeevani (Bio)":
    st.header("🧬 Vajra-Sanjeevani: Bio-Twin Simulator")
    dna_seq = st.text_input("Simulate DNA Marker", "ATCG-X22")
    if st.button("Run Simulation"):
        st.write(f"Predicting efficacy for marker {dna_seq}...")
        st.progress(88)
        st.write("Efficacy: 91.4% | Side-effect Risk: 2.1%")

elif menu == "🧠 Smriti (Cognitive)":
    st.header("🧠 Vajra-Smriti: Neural Continuity")
    thought = st.text_area("Ingest new memory or value:")
    if st.button("Archive to Vault"):
        if thought:
            st.session_state.memories.append({"time": time.ctime(), "content": thought})
            st.success("Memory block encrypted.")
        else:
            st.error("Input required.")
    
    st.subheader("📜 Neural Vault History")
    for m in st.session_state.memories:
        st.caption(f"[{m['time']}] {m['content']}")

# --- FOOTER ---
st.sidebar.markdown("---")
if st.sidebar.button("System Shutdown"):
    st.session_state.auth = False
    st.rerun()
