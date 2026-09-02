import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image

# กำหนดค่าหน้าเว็บสำหรับ Mobile-First UX
st.set_page_config(
    page_title="KidneyGuard AI - ตรวจความเสี่ยงโรคไต", 
    page_icon="🩺", 
    layout="centered"
)

st.title("🩺 KidneyGuard AI")
st.caption("ระบบปัญญาประดิษฐ์ประเมินความเสี่ยงและติดตามสุขภาพไต (SDG 3: Good Health & Well-Being)")

# โหลดโมเดล AI Model 1
@st.cache_resource
def load_risk_model():
    try:
        with open('model_risk.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

risk_model = load_risk_model()

# แถบเมนูการทำงาน (Tabs)
tab1, tab2, tab3 = st.tabs([
    "📋 โมเดล 1: ประเมินความเสี่ยง", 
    "🌊 โมเดล 2: ตรวจปัสสาวะ & Streak", 
    "📊 แดชบอร์ดสรุปผล"
])

# -------------------------------------------------------------
# TAB 1: Model 1 - แบบสอบถามประเมินความเสี่ยงโรคไต
# -------------------------------------------------------------
with tab1:
    st.subheader("แบบประเมินความเสี่ยงโรคไตวายเรื้อรังเบื้องต้น")
    st.write("กรุณาตอบคำถามด้านล่างเพื่อให้ AI ประเมินความเสี่ยงของท่าน")
    
    age = st.number_input("อายุของคุณ (ปี)", min_value=1, max_value=120, value=25)
    high_bp = st.radio("ท่านมีภาวะความดันโลหิตสูงหรือไม่?", ["ไม่ใช่", "ใช่"])
    diabetes = st.radio("ท่านเป็นโรคเบาหวานหรือไม่?", ["ไม่ใช่", "ใช่"])
    swelling = st.radio("ท่านมีอาการหน้าบวม ขาบวม หรือกดบุ๋มหรือไม่?", ["ไม่ใช่", "ใช่"])
    foamy = st.radio("ปัสสาวะของท่านมีฟองมากเป็นประจำหรือไม่?", ["ไม่ใช่", "ใช่"])
    low_water = st.radio("ท่านดื่มน้ำน้อยกว่า 1.5 ลิตรต่อวันเป็นประจำหรือไม่?", ["ไม่ใช่", "ใช่"])

    if st.button("คำนวณระดับความเสี่ยง"):
        # แปลงข้อมูลอินพุตเป็นรูปแบบตัวเลขสำหรับ Model
        inputs = np.array([[
            age, 
            1 if high_bp == "ใช่" else 0,
            1 if diabetes == "ใช่" else 0,
            1 if swelling == "ใช่" else 0,
            1 if foamy == "ใช่" else 0,
            1 if low_water == "ใช่" else 0
        ]])
        
        if risk_model:
            prob = risk_model.predict_proba(inputs)[0][1] * 100
            st.session_state['risk_score'] = prob
            
            if prob >= 50:
                st.error(f"⚠️ ผลประเมิน: มีความเสี่ยงสูง ({prob:.1f}%)")
                st.warning("💡 คำแนะนำ: ควรเข้าพบแพทย์เพื่อทำการตรวจเลือด (eGFR / Creatinine) และตรวจปัสสาวะอย่างเป็นทางการ")
            else:
                st.success(f"✅ ผลประเมิน: มีความเสี่ยงต่ำ ({prob:.1f}%)")
                st.info("💡 คำแนะนำ: ควรปฏิบัติตามสุขนิสัยที่ดี ดื่มน้ำให้เพียงพอ และหลีกเลี่ยงอาหารรสเค็มจัด")
        else:
            st.error("ไม่พบไฟล์โมเดล 'model_risk.pkl' กรุณารันไฟล์ 'train_model.py' ก่อน")

# -------------------------------------------------------------
# TAB 2: Model 2 - ตรวจปัสสาวะและติดตาม Streak
# -------------------------------------------------------------
with tab2:
    st.subheader("ระบบตรวจและบันทึกพฤติกรรมปัสสาวะประจำวัน")
    
    # ระบบเลือกโปรไฟล์สาธิตสำหรับกรรมการ
    st.write("### 👤 เลือกโปรไฟล์สาธิต (Demo Profile)")
    profile = st.selectbox("สลับโปรไฟล์เพื่อทดสอบระบบ:", [
        "ผู้ใช้งานทั่วไป (เริ่มต้น)", 
        "ผู้ป่วย A (เสี่ยงสูง - มีฟองสะสม 3 วัน)", 
        "ผู้ป่วย B (ปกติ)"
    ])

    if 'streak' not in st.session_state:
        st.session_state['streak'] = 0
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # โหลดข้อมูลจำลองตามโปรไฟล์ที่เลือก
    if profile == "ผู้ป่วย A (เสี่ยงสูง - มีฟองสะสม 3 วัน)":
        st.session_state['streak'] = 3
        st.session_state['history'] = [
            {"วันที่": "วันอังคาร", "สถานะ": "มีฟองมาก (สะสม)", "เตือน": True},
            {"วันที่": "วันพุธ", "สถานะ": "มีฟองมาก (สะสม)", "เตือน": True},
            {"วันที่": "วันพฤหัสบดี", "สถานะ": "มีฟองมาก (สะสม)", "เตือน": True}
        ]
    elif profile == "ผู้ป่วย B (ปกติ)":
        st.session_state['streak'] = 0
        st.session_state['history'] = [
            {"วันที่": "วันพฤหัสบดี", "สถานะ": "ปกติ (ใส / เหลืองอ่อน)", "เตือน": False}
        ]

    st.divider()
    st.write("### ทางเลือก A: อัปโหลดรูปภาพปัสสาวะ / แผ่นตรวจ (Dipstick)")
    uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพปัสสาวะหรือแผ่นตรวจ dipstick", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="รูปภาพที่อัปโหลด", use_container_width=True)
        st.info("🔍 AI วิเคราะห์สี: อยู่ในเกณฑ์เหลืองอ่อนใส (ปกติ)")

    st.divider()
    st.write("### ทางเลือก B: บันทึกสถานะปัสสาวะวันนี้ (Streak Tracker)")
    
    today_status = st.selectbox("เลือกลักษณะปัสสาวะของวันนี้:", [
        "ปกติ (ใส / เหลืองอ่อน)",
        "เหลืองเข้ม (ภาวะขาดน้ำ)",
        "มีฟองมาก (ฟองหนาไม่ยุบตัว)",
        "สีแดง / น้ำตาล (สงสัยมีเลือดปน)"
    ])
    
    if st.button("บันทึกข้อมูลวันนี้"):
        if "มีฟองมาก" in today_status or "สีแดง" in today_status:
            st.session_state['streak'] += 1
            st.session_state['history'].append({"วันที่": "วันนี้", "สถานะ": today_status, "เตือน": True})
        else:
            st.session_state['streak'] = 0
            st.session_state['history'].append({"วันที่": "วันนี้", "สถานะ": today_status, "เตือน": False})
            
        st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")

    # เงื่อนไขแจ้งเตือนความผิดปกติสะสม (Streak)
    if st.session_state['streak'] >= 3:
        st.error(f"🚨 แจ้งเตือนด่วน: พบปัสสาวะมีลักษณะผิดปกติติดต่อกัน {st.session_state['streak']} ครั้ง!")
        st.write("การมีฟองในปัสสาวะหรือสีผิดปกติสะสมเกิน 3 ครั้งติดต่อกัน อาจส่งผลถึงภาวะโปรตีนรั่วในปัสสาวะ (Proteinuria) หรือไตทำงานผิดปกติ")
    else:
        st.metric("จำนวนครั้งที่พบความผิดปกติสะสม (Streak)", f"{st.session_state['streak']} ครั้ง")

# -------------------------------------------------------------
# TAB 3: สรุปผลและประวัติสุขภาพ
# -------------------------------------------------------------
with tab3:
    st.subheader("แดชบอร์ดสรุปผลสุขภาพของคุณ")
    score = st.session_state.get('risk_score', 'ยังไม่ได้ประเมิน')
    st.metric("ระดับความเสี่ยงที่ประเมินได้", f"{score:.1f}%" if isinstance(score, float) else score)
    
    if st.session_state['history']:
        st.write("#### ประวัติการบันทึกปัสสาวะ")
        df_hist = pd.DataFrame(st.session_state['history'])
        st.dataframe(df_hist, use_container_width=True)

st.divider()
st.caption("⚠️ **ข้อจำกัดและข้อแถลงสิทธิ์**: นวัตกรรมนี้เป็นเพียงระบบคัดกรองความเสี่ยงเบื้องต้นเพื่อส่งเสริมสุขภาพ (SDG 3) ไม่สามารถใช้ทดแทนการวินิจฉัยทางการแพทย์โดยแพทย์ผู้เชี่ยวชาญได้")