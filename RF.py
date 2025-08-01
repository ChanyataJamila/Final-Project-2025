import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier 
import seaborn as sns
import matplotlib.pyplot as plt

# โหลดข้อมูล
df = pd.read_csv('output3.csv')
X = df.drop(columns=['Dead'])
y = df['Dead']
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier()
print("เริ่มเทรน RandomForestClassifier")
model.fit(X_train_scaled, y_train)
print("เทรนเสร็จแล้ว!")

y_pred = model.predict(X_test_scaled)

try:
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
except AttributeError:
    y_prob = model.decision_function(X_test_scaled)
    y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print("Accuracy:", acc)
print("ROC AUC:", auc)
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - RandomForestClassifier')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

print("เสร็จแล้ว!")