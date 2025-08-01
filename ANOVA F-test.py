import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif

# --------------------
# 1) โหลดข้อมูล
df = pd.read_csv('output3.csv')

# สมมติ target column ชื่อ 'Dead'
X = df.drop('Dead', axis=1)
y = df['Dead']

# --------------------
# 2) ใช้ ANOVA F-test เพื่อหา p-value
selector = SelectKBest(score_func=f_classif, k='all')
selector.fit(X, y)

p_values = selector.pvalues_

# --------------------
# 3) รวมชื่อฟีเจอร์และ p-value
results = pd.DataFrame({
    'Feature': X.columns,
    'p-value': p_values
}).sort_values('p-value')

print("ผลลัพธ์ p-value:")
print(results)

# --------------------
# 4) เลือกเฉพาะฟีเจอร์ที่ p-value <= 0.05
significant_features = results[results['p-value'] <= 0.05]['Feature'].tolist()
print("\nฟีเจอร์ที่เหลือ:", significant_features)

# --------------------
# 5) สร้าง DataFrame ใหม่ที่มีเฉพาะฟีเจอร์สำคัญ + target
df_selected = df[significant_features + ['Dead']]

# --------------------
# 6) บันทึกเป็นไฟล์ CSV
df_selected.to_csv('data_selected.csv', index=False)
print("\nบันทึกไฟล์ data_selected.csv เรียบร้อยแล้ว!")
