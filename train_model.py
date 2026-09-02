import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# ชุดข้อมูลฝึกสอน (Features: Age, High_BP, Diabetes, Swelling, Foamy_Urine, Low_Water -> Risk)
data = pd.DataFrame([
    [55, 1, 1, 1, 1, 1, 1],
    [22, 0, 0, 0, 0, 0, 0],
    [60, 1, 1, 1, 1, 0, 1],
    [28, 0, 0, 0, 0, 1, 0],
    [45, 1, 0, 1, 0, 1, 1],
    [35, 0, 0, 0, 0, 0, 0],
    [50, 0, 1, 0, 1, 1, 1],
    [20, 0, 0, 0, 0, 0, 0]
], columns=['age', 'high_bp', 'diabetes', 'swelling', 'foamy_urine', 'low_water', 'risk'])

X = data.drop('risk', axis=1)
y = data['risk']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

with open('model_risk.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ ฝึกสอนโมเดล 1 เรียบร้อยและบันทึกไฟล์เป็น 'model_risk.pkl'")