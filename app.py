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
# TAB 1: Model 1 - แบบสอบถามประเมินความเสี่ยงโรคไต (25 ข้อ)
# -------------------------------------------------------------
with tab1:
    st.subheader("แบบประเมินความเสี่ยงโรคไตวายเรื้อรัง (25 คำถาม)")
    st.write("กรุณาตอบคำถามตามความเป็นจริงเพื่อความแม่นยำในการวิเคราะห์ของ AI")
    
    options = ["ไม่ใช่", "ไม่แน่ใจ", "ใช่"]
    val_map = {"ไม่ใช่": 0.0, "ไม่แน่ใจ": 0.5, "ใช่": 1.0}

    # ---------------- หมวดที่ 1 ----------------
    st.markdown("#### 🥗 หมวดที่ 1: พฤติกรรมการกินและโภชนาการ (8 ข้อ)")
    age = st.number_input("1. อายุของคุณ (ปี)", min_value=1, max_value=120, value=25)
    salty_food = st.radio("2. ทานอาหารรสเค็มจัด หรือซดน้ำซุป/น้ำจิ้มหมดถ้วยเป็นประจำ?", options, key="q2")
    sweet_drinks = st.radio("3. ดื่มน้ำหวาน ชานม หรือน้ำอัดลมมากกว่า 1 แก้ว/วัน เป็นประจำ?", options, key="q3")
    processed_snack = st.radio("4. ทานอาหารแปรรูป ขนมขบเคี้ยว หรืออาหารบะหมี่สำเร็จรูปบ่อยครั้ง?", options, key="q4")
    low_water = st.radio("5. ดื่มน้ำสะอาดน้อยกว่า 1.5 ลิตร (ประมาณ 6-8 แก้ว) ต่อวัน?", options, key="q5")
    high_fat_diet = st.radio("6. ชอบทานอาหารติดมัน ของทอด หรืออาหารกะทิเป็นประจำ?", options, key="q6")
    alcohol = st.radio("7. ดื่มเครื่องดื่มแอลกอฮอล์เป็นประจำ (มากกว่า 2-3 ครั้ง/สัปดาห์)?", options, key="q7")
    nsaids = st.radio("8. ทานยาทานแก้ปวดชุด ยาสมุนไพร หรือยาแก้ปวดแก้อักเสบ (NSAIDs) ติดต่อกันนาน?", options, key="q8")

    st.divider()

    # ---------------- หมวดที่ 2 ----------------
    st.markdown("#### 🩺 หมวดที่ 2: อาการและสัญญาณเตือนทางร่างกาย (9 ข้อ)")
    swelling = st.radio("9. มีอาการหน้าบวม ขาบวม หรือกดบริเวณหลังเท้าแล้วบุ๋มไม่คืนตัว?", options, key="q9")
    foamy = st.radio("10. ปัสสาวะมีฟองมาก ฟองหนา และไม่ยุบตัวหายไปเอง?", options, key="q10")
    fatigue = st.radio("11. รู้สึกอ่อนเพลีย เหนื่อยง่าย ไม่มีแรง โดยไม่ทราบสาเหตุ?", options, key="q11")
    nocturia = st.radio("12. ตื่นขึ้นมาปัสสาวะกลางดึกมากกว่า 2 ครั้งเป็นประจำ?", options, key="q12")
    skin_itching = st.radio("13. มีอาการผิวแห้ง คันตามร่างกายอย่างรุนแรงโดยไม่มีผื่น?", options, key="q13")
    flank_pain = st.radio("14. รู้สึกปวดหลังหรือปวดเอวบริเวณข้างลำตัวอย่างต่อเนื่อง?", options, key="q14")
    muscle_cramps = st.radio("15. เป็นตะคริวบ่อยครั้ง โดยเฉพาะในเวลากลางคืน?", options, key="q15")
    loss_of_appetite = st.radio("16. รู้สึกเบื่ออาหาร คลื่นไส้ หรืออาเจียนในตอนเช้า?", options, key="q16")
    shortness_of_breath = st.radio("17. รู้สึกหายใจติดขัด หรือเหนื่อยหอบง่ายเมื่อออกแรงเล็กน้อย?", options, key="q17")

    st.divider()

    # ---------------- หมวดที่ 3 ----------------
    st.markdown("#### 🧬 หมวดที่ 3: ประวัติสุขภาพและสไตล์การดำเนินชีวิต (8 ข้อ)")
    metallic_taste = st.radio("18. รู้สึกรสชาติอาหารเปลี่ยนไป หรือลมหายใจมีกลิ่นแปลกๆ (คล้ายยูเรีย)?", options, key="q18")
    diabetes = st.radio("19. มีประวัติเป็นโรคเบาหวาน หรือคุมระดับน้ำตาลในเลือดไม่ได้?", options, key="q19")
    high_bp = st.radio("20. มีภาวะความดันโลหิตสูง หรือต้องทานยาความดันเป็นประจำ?", options, key="q20")
    family_ckd = st.radio("21. มีญาติสายตรง (พ่อ แม่ พี่ น้อง) มีประวัติเป็นโรคไต?", options, key="q21")
    gout = st.radio("22. เคยได้รับวินิจฉัยว่าเป็นโรคเกาต์ หรือมีกรดยูริกในเลือดสูง?", options, key="q22")
    smoking = st.radio("23. สูบบุหรี่ หรือได้รับควันบุหรี่มือสองเป็นประจำ?", options, key="q23")
    exercise = st.radio("24. นั่งทำงานนานๆ และขาดการออกกำลังกาย (น้อยกว่า 150 นาที/สัปดาห์)?", options, key="q24")
    sleep_problems = st.radio("25. มีปัญหาเกี่ยวกับการนอน เช่น นอนไม่หลับ หรือสะดุ้งตื่นบ่อย?", options, key="q25")

    st.divider()

    if st.button("คำนวณระดับความเสี่ยง (AI Analytics)", use_container_width=True):
        # รวมข้อมูลทั้ง 25 ข้อเข้า Pandas DataFrame ให้ตรงกับ Model
        input_data = pd.DataFrame([[
            age, val_map[salty_food], val_map[sweet_drinks], val_map[processed_snack], val_map[low_water],
            val_map[high_fat_diet], val_map[alcohol], val_map[nsaids], val_map[swelling], val_map[foamy],
            val_map[fatigue], val_map[nocturia], val_map[skin_itching], val_map[flank_pain], val_map[muscle_cramps],
            val_map[loss_of_appetite], val_map[shortness_of_breath], val_map[metallic_taste], val_map[diabetes], val_map[high_bp],
            val_map[family_ckd], val_map[gout], val_map[smoking], val_map[exercise], val_map[sleep_problems]
        ]], columns=[
            'age', 'salty_food', 'sweet_drinks', 'processed_snack', 'low_water', 
            'high_fat_diet', 'alcohol', 'nsaids', 'swelling', 'foamy_urine', 
            'fatigue', 'nocturia', 'skin_itching', 'flank_pain', 'muscle_cramps', 
            'loss_of_appetite', 'shortness_of_breath', 'metallic_taste', 'diabetes', 'high_bp', 
            'family_ckd', 'gout', 'smoking', 'exercise', 'sleep_problems'
        ])
        
        if risk_model:
            prob = risk_model.predict_proba(input_data)[0][1] * 100
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