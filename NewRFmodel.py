# ติดตั้งไลบรารีถ้ายังไม่ได้
# pip install pandas scikit-learn imbalanced-learn

import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

# ----------------------
# 1) Load data
df = pd.read_csv('output3.csv')

# แยก feature และ target
X = df.drop(columns=['Dead'],axis=1)
y = df['Dead']

# ----------------------
# 2) แบ่ง train/test (เช่น 80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Before oversampling:")
print(y_train.value_counts())

# ----------------------
# 3) Oversample เฉพาะ training set
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("After oversampling:")
print(pd.Series(y_train_resampled).value_counts())

# ----------------------
# 4) Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_resampled, y_train_resampled)

# ----------------------
# 5) Evaluate
y_pred = model.predict(X_test)

print("\n=== Evaluation on test set ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ----------------------
# (Optional) บันทึกโมเดลด้วย joblib ถ้าอยากนำไปใช้ภายหลัง
# from joblib import dump
# dump(model, 'rf_model.joblib')

df_train_balanced = pd.concat([
    pd.DataFrame(X_train_resampled, columns=X_train.columns),
    pd.Series(y_train_resampled, name='Dead')
], axis=1)

# บันทึกเป็น CSV
df_train_balanced.to_csv('train_balanced.csv', index=False)

print("บันทึกไฟล์ train_balanced.csv เรียบร้อย!")

# โหลด train_balanced.csv
df_balanced = pd.read_csv('train_balanced.csv')

X_train_balanced = df_balanced.drop(columns=['Dead'],axis=1)
y_train_balanced = df_balanced['Dead']

# Train โมเดลใหม่ เช่น Logistic Regression
from sklearn.linear_model import LogisticRegression

model2 = LogisticRegression(random_state=42)
model2.fit(X_train_balanced, y_train_balanced)

# Evaluate กับ test set เดิม
y_pred2 = model2.predict(X_test)

from sklearn.metrics import classification_report
print("\n=== Evaluation on test set ===")
print("Accuracy:", accuracy_score(y_test, y_pred2))
print("F1 Score:", f1_score(y_test, y_pred2))
print(classification_report(y_test, y_pred2))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred2))
