import streamlit as st
import pandas as pd
from app.ui.components import section_header

def show(api_client):
    st.markdown('<h1 class="hero-text">Audit History</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 2rem;">Search, filter, and export past fraud analysis records.</p>', unsafe_allow_html=True)

    history = api_client.get_history(limit=1000)
    
    if history.empty:
        st.info("No audit history found in the system.")
        return

    # Filter UI
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            search = st.text_input("Search Provider ID", placeholder="e.g. PRV51001")
        with c2:
            risk_filter = st.multiselect("Risk Level", options=["High", "Medium", "Low"], default=["High", "Medium", "Low"])
        with c3:
            fraud_only = st.checkbox("Flagged Fraud Only")
        st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    df = history.copy()
    if search:
        df = df[df['Provider'].str.contains(search, case=False)]
    if risk_filter:
        df = df[df['risk_level'].isin(risk_filter)]
    if fraud_only:
        df = df[df['is_fraud'] == True]

    section_header(f"Records Found: {len(df)}")
    
    # Format for display
    display_df = df.copy()
    display_df['is_fraud'] = display_df['is_fraud'].apply(lambda x: "🚩 YES" if x else "✅ NO")
    display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
    display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "id": "Audit ID",
            "is_fraud": "Flagged",
            "probability": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1),
            "amount": "Claim Value",
            "created_at": "Timestamp"
        }
    )

    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD FULL REPORT (CSV)",
        data=csv,
        file_name=f"fraud_audit_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
        mime='text/csv',
        use_container_width=True
    )
