import sys, os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.ui.styles import apply_styles
from app.ui.api_client import APIClient
from app.ui.pages import overview, prediction, explainability, history, analytics

# Page Config
st.set_page_config(
    page_title="FraudShield AI | Enterprise Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "Overview Intelligence"

# Apply Custom CSS
apply_styles()

# Initialize API Client
api_client = APIClient()

# ── AUTHENTICATION ─────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; font-size: 2.2rem;">🛡️</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; margin-bottom: 0.5rem;">FraudShield AI</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Enterprise AI Audit Portal</p>', unsafe_allow_html=True)
        
        username = st.text_input("Access ID", placeholder="admin")
        password = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE ACCESS", use_container_width=True):
            if api_client.login(username, password):
                st.session_state.authenticated = True
                st.success("Authentication Successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
        
        st.markdown('<p style="text-align: center; color: #475569; font-size: 0.75rem; margin-top: 2rem;">Authorized Personnel Only • Secure 256-bit Encryption</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── MAIN DASHBOARD ─────────────────────────────────────────────────────────────
user_data = api_client.get_me()

with st.sidebar:
    st.markdown('<h2 style="color: #00d4ff; margin-bottom: 1.5rem;">FraudShield AI</h2>', unsafe_allow_html=True)
    
    if user_data:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px; margin-bottom: 2rem; border-left: 3px solid #00d4ff;">
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">Welcome back,</p>
            <p style="margin: 0; font-weight: 700; color: #f1f5f9;">{user_data['full_name']}</p>
            <p style="margin: 0; font-size: 0.7rem; color: #00d4ff;">{user_data['role'].upper()} ACCESS</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🛰️ NAVIGATION")
    choice = st.radio("", [
        "Overview Intelligence",
        "Live Fraud Analysis",
        "Explainable AI",
        "Audit Logs",
        "Network Analytics"
    ], index=["Overview Intelligence", "Live Fraud Analysis", "Explainable AI", "Audit Logs", "Network Analytics"].index(st.session_state.menu_choice))
    
    st.session_state.menu_choice = choice

    st.markdown("<br>" * 5, unsafe_allow_html=True)
    
    if st.button("LOCK SESSION", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.access_token = None
        st.rerun()

# ── PAGE ROUTING ───────────────────────────────────────────────────────────────
if choice == "Overview Intelligence":
    overview.show(api_client)
elif choice == "Live Fraud Analysis":
    prediction.show(api_client)
elif choice == "Explainable AI":
    explainability.show(api_client)
elif choice == "Audit Logs":
    history.show(api_client)
elif choice == "Network Analytics":
    analytics.show(api_client)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; border-top: 1px solid rgba(255,255,255,0.05); color: #475569; font-size: 0.8rem;">
    FraudShield AI Enterprise v2.5.0 • Developed for Healthcare Integrity Auditing
</div>
""", unsafe_allow_html=True)
