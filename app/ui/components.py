import streamlit as st

def card(title, content, subtext=None, color=None):
    color_style = f"border-left: 4px solid {color};" if color else ""
    st.markdown(f"""
    <div class="glass-card" style="{color_style}">
        <p style="color: #94a3b8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">{title}</p>
        <p style="font-size: 1.8rem; font-weight: 700; margin-bottom: 4px;">{content}</p>
        {f'<p style="color: #475569; font-size: 0.75rem;">{subtext}</p>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    st.markdown(f'<div style="margin: 2rem 0 1rem 0;"><h2 style="font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px;">{title}</h2>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="color: #64748b; font-size: 0.9rem;">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown('<hr style="margin-top: 10px; border-color: rgba(255,255,255,0.05);"></div>', unsafe_allow_html=True)

def alert_banner(title, message, type="info"):
    colors = {
        "info": ("#00d4ff", "rgba(0, 212, 255, 0.1)"),
        "success": ("#10b981", "rgba(16, 185, 129, 0.1)"),
        "warning": ("#f59e0b", "rgba(245, 158, 11, 0.1)"),
        "danger": ("#ef4444", "rgba(239, 68, 68, 0.1)")
    }
    color, bg = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="background: {bg}; border: 1px solid {color}33; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <p style="color: {color}; font-weight: 700; margin-bottom: 4px;">{title}</p>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def risk_indicator(probability):
    if probability > 0.75:
        color, label = "#ef4444", "CRITICAL RISK"
    elif probability > 0.5:
        color, label = "#f59e0b", "ELEVATED RISK"
    else:
        color, label = "#10b981", "LOW RISK"
        
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
        <div style="width: 12px; height: 12px; border-radius: 50%; background: {color}; box-shadow: 0 0 10px {color}66;"></div>
        <span style="color: {color}; font-weight: 700; font-size: 0.9rem;">{label}</span>
    </div>
    """, unsafe_allow_html=True)
