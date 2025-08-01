# นำเข้าลไลบรารีที่จำเป็น
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# 1) โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv('output3.csv')  # <-- เปลี่ยนชื่อไฟล์ตามไฟล์ของคุณ

# 2) แยก feature (X) และ target (y)
X = df.drop('Dead', axis=1).values  # <-- เปลี่ยน 'target' เป็นชื่อคอลัมน์จริงของคุณ
y = df['Dead'].values

# 3) สร้าง Stratified K-Fold cross-validation
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 4) เตรียม list สำหรับเก็บค่าประสิทธิภาพในแต่ละ fold
all_metrics = []

# เริ่มวนลูปในแต่ละ fold
fold = 1
for train_idx, test_idx in kf.split(X, y):
    print(f"\n=== Fold {fold} ===")

    # 5) แบ่งข้อมูลเป็น train และ test ตาม index ที่ได้จาก kf.split
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # 6) สร้างและเทรนโมเดล Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 7) ทำนายผลบน test set
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]  # ความน่าจะเป็นของ class=1

    # 8) คำนวณค่าประสิทธิภาพต่างๆ
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)

    # เพิ่ม: คำนวณ recall แยกตามคลาส
    recall_per_class = recall_score(y_test, y_pred, average=None)

    # 9) แสดงผลลัพธ์ในแต่ละ fold
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall (overall / class=1): {recall:.4f}")
    print(f"Recall (class=0): {recall_per_class[0]:.4f}")
    print(f"Recall (class=1): {recall_per_class[1]:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"AUC: {auc:.4f}")
    print(f"Confusion Matrix:\n{cm}")

    # 10) เก็บผลลัพธ์ลงใน list
    all_metrics.append({
        'fold': fold,
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'recall_class_0': recall_per_class[0],
        'recall_class_1': recall_per_class[1],
        'f1_score': f1,
        'auc': auc
    })

    fold += 1



# 11) แปลงผลลัพธ์ทั้งหมดเป็น DataFrame
results_df = pd.DataFrame(all_metrics)

# 12) แสดงผลลัพธ์รวม
print("\n=== Summary ===")
print(results_df)

# 13) แสดงค่าเฉลี่ยของแต่ละ metric
print("\nMean metrics (ค่าเฉลี่ย):")
print(results_df.mean())

# 14) บันทึกผลลัพธ์เป็นไฟล์ CSV
results_df.to_csv('cv_summary_metrics2.csv', index=False)
print("\nบันทึกไฟล์ผลลัพธ์เป็น 'cv_summary_metrics2.csv' แล้วครับ!")
