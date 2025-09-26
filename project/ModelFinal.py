# K=10
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# โหลดข้อมูล
df = pd.read_csv('data_selected.csv')  
X = df.drop('Dead', axis=1).values 
y = df['Dead'].values

# สร้าง Stratified K-Fold
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# กำหนดโมเดลที่ต้องการเทรน
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
}

# เก็บผลลัพธ์ทั้งหมด
all_results = []

# เริ่ม loop cross-validation
fold = 1
for train_idx, test_idx in kf.split(X, y):
    print(f"\n=== Fold {fold} ===")

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    for model_name, model in models.items():
        print(f"\n----- {model_name} -----")

        # เทรนโมเดล
        model.fit(X_train, y_train)

        # ทำนาย
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:,1]  # probability ของ class=1

        # คำนวณ metric
        acc = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        recall_per_class = recall_score(y_test, y_pred, average=None)

        # แสดงผล
        print(f"Accuracy: {acc:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall (class=1): {recall:.4f}")
        print(f"Recall (class=0): {recall_per_class[0]:.4f}")
        print(f"Recall (class=1): {recall_per_class[1]:.4f}")
        print(f"F1-score: {f1:.4f}")
        print(f"AUC: {auc:.4f}")
        print(f"Confusion Matrix:\n{cm}")

        # เก็บผลลัพธ์
        all_results.append({
            'fold': fold,
            'model': model_name,
            'accuracy': acc,
            'precision': precision,
            'recall': recall,
            'recall_class_0': recall_per_class[0],
            'recall_class_1': recall_per_class[1],
            'f1_score': f1,
            'auc': auc
        })

    fold += 1

# แปลงเป็น DataFrame
results_df = pd.DataFrame(all_results)

# แสดงผลลัพธ์รวม
print("\n=== Summary ===")
print(results_df)

# แสดงค่าเฉลี่ยของแต่ละโมเดล
mean_metrics = results_df.groupby('model').mean()
print("\n=== Mean metrics by model ===")
print(mean_metrics)

import joblib

# หลังจากเทรนเสร็จ ใช้โมเดลตัวสุดท้าย
final_model = RandomForestClassifier(n_estimators=100, random_state=42)
final_model.fit(X, y)

# บันทึกโมเดล
joblib.dump(final_model, "survival_model.pkl")