import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# ชุดข้อมูลฝึกสอน 25 คุณลักษณะ (Features)
columns = [
    'age', 'salty_food', 'sweet_drinks', 'processed_snack', 'low_water', 
    'high_fat_diet', 'alcohol', 'nsaids', 'swelling', 'foamy_urine', 
    'fatigue', 'nocturia', 'skin_itching', 'flank_pain', 'muscle_cramps', 
    'loss_of_appetite', 'shortness_of_breath', 'metallic_taste', 'diabetes', 'high_bp', 
    'family_ckd', 'gout', 'smoking', 'exercise', 'sleep_problems'
]

# ข้อมูลตัวอย่างจำลองความสัมพันธ์ของความเสี่ยง
data = [
    [60, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1],
    [20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0],
    [45, 0.5, 0.5, 1.0, 0.5, 0.5, 0.0, 0.5, 0.0, 1.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.5, 0.0, 0.0, 0.5, 0.0, 1],
    [25, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0],
    [50, 1.0, 0.0, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0, 0.5, 1]
]

df = pd.DataFrame(data, columns=columns + ['risk'])

X = df.drop('risk', axis=1)
y = df['risk']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

with open('model_risk.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ อัปเดตโมเดลรองรับแบบประเมิน 25 ข้อเรียบร้อยแล้ว!")