import streamlit as st
import plotly.express as px
import pandas as pd
from app.ui.components import section_header

def show(api_client):
    st.markdown('<h1 class="hero-text">Dataset Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 2rem;">Macro-level insights into healthcare fraud distribution and feature correlations.</p>', unsafe_allow_html=True)

    analytics = api_client.get_analytics()
    if not analytics:
        st.warning("Advanced analytics engine is still initializing...")
        return

    section_header("Correlation Analysis", "Discovering hidden relationships between claim metrics")
    
    if analytics.get('correlation'):
        corr_df = pd.DataFrame(analytics['correlation'])
        fig_heat = px.imshow(
            corr_df,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            template="plotly_dark",
            title="Metric Correlation Heatmap",
            height=500
        )
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=50, r=50, b=50)
        )
        st.plotly_chart(fig_heat, use_container_width=True, theme="streamlit")

    section_header("Distribution Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Risk level dist
        risk_dist = analytics.get('risk_distribution', {})
        if risk_dist:
            fig_bar = px.bar(
                x=list(risk_dist.keys()),
                y=list(risk_dist.values()),
                template="plotly_dark",
                labels={"x": "Risk Level", "y": "Frequency"},
                title="Risk Class Distribution",
                color=list(risk_dist.keys()),
                color_discrete_map={'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Statistical Summary")
        st.markdown(f"""
        - **Total Records Analyzed**: {analytics.get('total_predictions', 0)}
        - **Average Anomaly Score**: {analytics.get('avg_probability', 0):.4f}
        - **Critical Anomalies**: {analytics.get('high_risk_count', 0)}
        - **Dataset Coverage**: 100%
        """)
        st.markdown('</div>', unsafe_allow_html=True)
