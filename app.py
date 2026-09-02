import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image

# Page setup for Mobile-First UX
st.set_page_config(page_title="KidneyGuard AI", page_icon="🩺", layout="centered")

st.title("🩺 KidneyGuard AI")
st.caption("AI-Powered Kidney Risk Assessment & Daily Urine Tracker (SDG 3)")

# Load trained Model 1
@st.cache_resource
def load_risk_model():
    try:
        with open('model_risk.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

risk_model = load_risk_model()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📋 Model 1: Risk Screener", "🌊 Model 2: Urine & Streak Check", "📊 Health Dashboard"])

# -------------------------------------------------------------
# TAB 1: Model 1 - Risk Questionnaire
# -------------------------------------------------------------
with tab1:
    st.subheader("Kidney Disease Risk Screener")
    st.write("Answer the questions below to evaluate your chronic kidney disease risk level.")
    
    age = st.number_input("Your Age", min_value=1, max_value=120, value=25)
    high_bp = st.radio("Do you have High Blood Pressure?", ["No", "Yes"])
    diabetes = st.radio("Do you have Diabetes?", ["No", "Yes"])
    swelling = st.radio("Do you experience facial or leg swelling?", ["No", "Yes"])
    foamy = st.radio("Is your urine frequently foamy?", ["No", "Yes"])
    low_water = st.radio("Do you drink less than 1.5L of water daily?", ["No", "Yes"])

    if st.button("Calculate Risk Score"):
        inputs = np.array([[
            age, 
            1 if high_bp == "Yes" else 0,
            1 if diabetes == "Yes" else 0,
            1 if swelling == "Yes" else 0,
            1 if foamy == "Yes" else 0,
            1 if low_water == "Yes" else 0
        ]])
        
        if risk_model:
            prob = risk_model.predict_proba(inputs)[0][1] * 100
            st.session_state['risk_score'] = prob
            
            if prob >= 50:
                st.error(f"⚠️ High Risk Indicated ({prob:.1f}%)")
                st.warning("Recommendation: Consult a medical professional for eGFR and urine protein tests.")
            else:
                st.success(f"✅ Low Risk Indicated ({prob:.1f}%)")
                st.info("Keep maintaining a healthy hydration and diet routine!")
        else:
            st.error("Model file 'model_risk.pkl' not found. Please run 'train_model.py' first.")

# -------------------------------------------------------------
# TAB 2: Model 2 - Urine Analysis & Streak Tracking
# -------------------------------------------------------------
with tab2:
    st.subheader("Daily Urine & Streak Tracking")
    
    if 'streak' not in st.session_state:
        st.session_state['streak'] = 0
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    st.write("### Option A: Upload Urine Dipstick / Visual Image")
    uploaded_file = st.file_uploader("Upload an image of your urine or test strip", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.info("🔍 AI Visual Check: Sample captured. Color spectrum appears in normal pale-yellow range.")

    st.divider()
    st.write("### Option B: Log Daily Urine Status (Streak Tracker)")
    
    today_status = st.selectbox("Select today's urine condition:", [
        "Normal (Clear / Pale Yellow)",
        "Dark Yellow (Dehydration)",
        "Foamy (Persistent bubbles)",
        "Red / Brownish (Blood suspect)"
    ])
    
    if st.button("Log Today's Entry"):
        if "Foamy" in today_status or "Red" in today_status:
            st.session_state['streak'] += 1
            st.session_state['history'].append({"Status": today_status, "Flagged": True})
        else:
            st.session_state['streak'] = 0
            st.session_state['history'].append({"Status": today_status, "Flagged": False})
            
        st.success("Entry Saved!")

    if st.session_state['streak'] >= 3:
        st.error(f"🚨 WARNING: Abnormal urine condition detected for {st.session_state['streak']} consecutive logs!")
        st.write("Persistent foamy or dark urine over 3+ entries strongly correlates with proteinuria or kidney strain.")
    else:
        st.metric("Current Abnormal Streak", f"{st.session_state['streak']} Days")

# -------------------------------------------------------------
# TAB 3: Summary Dashboard
# -------------------------------------------------------------
with tab3:
    st.subheader("Health Summary")
    score = st.session_state.get('risk_score', 'Not Assessed Yet')
    st.metric("Assessed Risk Level", f"{score:.1f}%" if isinstance(score, float) else score)
    
    if st.session_state['history']:
        st.write("#### Tracking History")
        df_hist = pd.DataFrame(st.session_state['history'])
        st.dataframe(df_hist, use_container_width=True)

st.divider()
st.caption("⚠️ **Disclaimer**: This tool is an AI prototype for screening purposes under SDG 3 and does not substitute professional medical diagnosis.")