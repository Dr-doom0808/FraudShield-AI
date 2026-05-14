import streamlit as st

def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary: #00d4ff;
        --secondary: #0a192f;
        --accent: #64ffda;
        --bg-dark: #060b13;
        --card-bg: rgba(13, 25, 48, 0.7);
        --glass-border: rgba(0, 212, 255, 0.15);
        --text-main: #e2e8f0;
        --text-dim: #94a3b8;
        --safe: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    .main {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 212, 255, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(100, 255, 218, 0.05) 0px, transparent 50%);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass-card:hover {
        border-color: rgba(0, 212, 255, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #08101a !important;
        border-right: 1px solid var(--glass-border);
        width: 280px !important;
    }

    .stRadio > div {
        gap: 8px;
    }

    .stRadio label {
        background: transparent !important;
        border: none !important;
        color: var(--text-dim) !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        transition: all 0.2s;
    }

    .stRadio label:hover {
        color: var(--primary) !important;
        background: rgba(0, 212, 255, 0.05) !important;
    }

    /* KPI Metrics */
    [data-testid="stMetric"] {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 15px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #0083fe) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--text-main) !important;
        border-radius: 8px !important;
    }

    /* Success/Error boxes */
    .stAlert {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }

    /* Custom Titles */
    .hero-text {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #fff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }
</style>
""", unsafe_allow_html=True)
