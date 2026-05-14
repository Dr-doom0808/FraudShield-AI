import streamlit as st
import plotly.graph_objects as go
from app.ui.components import section_header, card

def show(api_client):
    st.markdown('<h1 class="hero-text">Explainable AI (XAI)</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 2rem;">Deep-dive into the "Why" behind AI decisions using SHAP (SHapley Additive exPlanations).</p>', unsafe_allow_html=True)

    if 'last_result' not in st.session_state:
        st.info("Run a Live Analysis first to see the model explanation.")
        return

    res = st.session_state.last_result
    if not res.get('explanation'):
        st.warning("SHAP explanation was not generated for the last analysis.")
        return

    section_header("Feature Contribution Analysis", "How each feature pushed the prediction towards Fraud vs. Safe")
    
    explanation = res['explanation']
    # Sort features by absolute impact
    sorted_features = sorted(explanation.items(), key=lambda x: abs(x[1]), reverse=True)
    
    top_features = sorted_features[:10]
    features, values = zip(*top_features)
    
    # Waterfall chart
    fig = go.Figure(go.Waterfall(
        name = "SHAP Impact", orientation = "h",
        measure = ["relative"] * len(features),
        y = features,
        x = values,
        connector = {"line":{"color":"rgba(63, 63, 63, 0.5)"}},
        increasing = {"marker":{"color":"#ef4444"}},
        decreasing = {"marker":{"color":"#10b981"}},
    ))

    fig.update_layout(
        title = "Top 10 Decision Drivers (SHAP Values)",
        template = "plotly_dark",
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
        font_family = "Inter",
        height = 600,
        yaxis = dict(autorange="reversed", automargin=True),
        margin = dict(l=150, r=20, t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    section_header("Human-Readable Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Positive Contributors (Fraud Risk)")
        pos_features = [f for f, v in sorted_features if v > 0][:3]
        for f in pos_features:
            st.markdown(f"- **{f}**: Elevated value increased suspicion.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Negative Contributors (Protective)")
        neg_features = [f for f, v in sorted_features if v < 0][:3]
        for f in neg_features:
            st.markdown(f"- **{f}**: Value suggests normal billing behavior.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);">
        <h4 style="color: #00d4ff;">AI Reasoning Summary</h4>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            The model identified high correlation between <b>{top_features[0][0]}</b> and known fraudulent patterns in the training set. 
            The high impact of <b>{top_features[1][0]}</b> further solidifies the risk classification of <b>{res['risk_level']}</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
