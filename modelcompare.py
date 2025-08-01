import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier  # <-- เพิ่ม Neural Network

# ==== STEP 1: โหลดข้อมูล ====
df = pd.read_csv('output1.csv')
print("ตัวอย่างข้อมูล:")
print(df.head())

# ==== STEP 2: เตรียมข้อมูล ====
X = df.drop(columns=['ID','Dead'])  # Features
y = df['Dead']                 # Target


X = pd.get_dummies(X)  # One-hot encode
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==== STEP 3: สร้างโมเดล 
models = {
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Support Vector Machine': SVC(probability=True),
    'Gradient Boosting': GradientBoostingClassifier(),
    'Neural Network (MLP)': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
}

results = {}

# ==== STEP 4: เทรนและประเมินทุกโมเดล ====
for name, model in models.items():
    print(f"\n⏳ Training model: {name} ...")  # ช่วยดูว่าเริ่มเทรนอะไรแล้ว

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    try:
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
    except AttributeError:
        y_prob = model.decision_function(X_test_scaled)
        y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    results[name] = {
        'model': model,
        'accuracy': acc,
        'roc_auc': auc
    }

    print(f"\n==== {name} ====")
    print("Accuracy:", acc)
    print("ROC AUC:", auc)
    print(classification_report(y_test, y_pred))

    # วาด confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
    plt.close()  # <- สำคัญ ถ้าใช้ script ธรรมดา

# ==== STEP 5: สรุปผล ====
summary_df = pd.DataFrame({
    model: [res['accuracy'], res['roc_auc']]
    for model, res in results.items()
}, index=['Accuracy', 'ROC AUC'])

print("\n=== เปรียบเทียบโมเดลทั้งหมด ===")
print(summary_df.T.sort_values(by='ROC AUC', ascending=False))
