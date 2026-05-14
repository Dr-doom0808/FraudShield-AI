import streamlit as st
import plotly.graph_objects as go
import time
from app.ui.components import section_header, risk_indicator, alert_banner

def show(api_client):
    st.markdown('<h1 class="hero-text">Live Fraud Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 2rem;">Real-time AI auditing for individual healthcare claims.</p>', unsafe_allow_html=True)

    # Load seeded data for selection
    seeded = api_client.get_seeded_claims()
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Investigation Input")
        
        if seeded:
            selected = st.selectbox("Quick Load: Select from sample claims", 
                                  options=[c['Provider'] for c in seeded],
                                  index=0)
            if st.button("Autofill Data"):
                claim_data = next(c for c in seeded if c['Provider'] == selected)
                st.session_state.claim_form = claim_data
                st.success(f"Data loaded for {selected}")

        # Form fields
        form_data = st.session_state.get('claim_form', {})
        
        c1, c2, c3 = st.columns(3)
        with c1:
            provider = st.text_input("Provider ID", value=form_data.get('Provider', 'PRV51001'))
            reimbursed = st.number_input("Claim Reimbursed ($)", value=float(form_data.get('InscClaimAmtReimbursed', 0.0)))
            total_reimb = st.number_input("Total Reimbursed ($)", value=float(form_data.get('TotalReimbursement', 0.0)))
        with c2:
            ip_reimb = st.number_input("IP Annual Reimb ($)", value=float(form_data.get('IPAnnualReimbursementAmt', 0.0)))
            ip_deduct = st.number_input("IP Annual Deduct ($)", value=float(form_data.get('IPAnnualDeductibleAmt', 0.0)))
            renal = st.selectbox("Renal Disease", [0, 1], index=int(form_data.get('RenalDiseaseIndicator', 0)))
        with c3:
            alzheimer = st.selectbox("Alzheimer", [0, 1], index=int(form_data.get('ChronicCond_Alzheimer', 0)))
            heart = st.selectbox("Heart Failure", [0, 1], index=int(form_data.get('ChronicCond_Heartfailure', 0)))
            diabetes = st.selectbox("Diabetes", [0, 1], index=int(form_data.get('ChronicCond_Diabetes', 0)))

        explain = st.checkbox("Generate Deep AI Explainability (SHAP)", value=True)
        
        if st.button("RUN AI AUDIT", use_container_width=True):
            full_data = {
                "Provider": provider,
                "InscClaimAmtReimbursed": reimbursed,
                "IPAnnualReimbursementAmt": ip_reimb,
                "IPAnnualDeductibleAmt": ip_deduct,
                "TotalReimbursement": total_reimb,
                "RenalDiseaseIndicator": renal,
                "ChronicCond_Alzheimer": alzheimer,
                "ChronicCond_Heartfailure": heart,
                "ChronicCond_Diabetes": diabetes,
                "ChronicCond_KidneyDisease": int(form_data.get('ChronicCond_KidneyDisease', 0)),
                "ChronicCond_Cancer": int(form_data.get('ChronicCond_Cancer', 0)),
                "ChronicCond_ObstrPulmonary": int(form_data.get('ChronicCond_ObstrPulmonary', 0)),
                "ChronicCond_Depression": int(form_data.get('ChronicCond_Depression', 0)),
                "ChronicCond_IschemicHeart": int(form_data.get('ChronicCond_IschemicHeart', 0)),
                "ChronicCond_Osteoporasis": int(form_data.get('ChronicCond_Osteoporasis', 0)),
                "ChronicCond_rheumatoidarthritis": int(form_data.get('ChronicCond_rheumatoidarthritis', 0)),
                "ChronicCond_stroke": int(form_data.get('ChronicCond_stroke', 0))
            }
            
            with st.spinner("AI Engine analyzing claim patterns..."):
                result = api_client.predict(full_data, explain=explain)
                
                if "error" in result:
                    st.error(f"Audit Failed: {result['error']}")
                else:
                    st.session_state.last_result = result
                    st.toast("Analysis Complete!", icon="🚀")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Show results
    if 'last_result' in st.session_state:
        res = st.session_state.last_result
        section_header("Audit Findings")
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            prob = res['probability']
            is_fraud = res['is_fraud']
            
            st.subheader("Fraud Probability Meter")
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00d4ff"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(16, 185, 129, 0.2)'},
                        {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [75, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 75
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Inter"},
                height=250, margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, theme="streamlit")
            risk_indicator(prob)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_res2:
            if is_fraud:
                alert_banner("CRITICAL ALERT", 
                           "This claim has been flagged as highly suspicious by the AI audit engine. Immediate review is recommended.",
                           "danger")
            else:
                alert_banner("CLEAN BILL", 
                           "No anomalous patterns detected. This claim aligns with standard healthcare provider behavior.",
                           "success")
            
            st.markdown(f"""
            <div class="glass-card">
                <h4>Analysis Details</h4>
                <p style="color: #94a3b8;">Risk Classification: <b>{res['risk_level']}</b></p>
                <p style="color: #94a3b8;">Confidence Score: <b>{prob:.4f}</b></p>
                <p style="color: #94a3b8;">Decision Engine: <b>XGBoost-V2</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if explain and res.get('explanation'):
                if st.button("View AI Explainability (SHAP)", use_container_width=True):
                    st.info("Redirecting to Explainability tab...")
                    # This would ideally switch the radio button
                    st.session_state.menu_choice = "Explainable AI"
                    st.rerun()
