import pandas as pd
import matplotlib.pyplot as plt

# สมมติว่ามี DataFrame ชื่อ df
df = pd.read_csv('output1.csv')

# นับจำนวน 0 (รอด) และ 1 (ตาย)
counts = df['Dead'].value_counts().sort_index()  # index 0=รอด, 1=ตาย

# labels ให้เข้าใจง่าย
labels = ['Alive', 'Dead']

plt.figure(figsize=(6, 4))
bars = plt.bar(labels, counts, color=['green', 'red'])
plt.title('จำนวนคนรอดและคนตาย')
plt.ylabel('จำนวน')

# ใส่จำนวนบนแท่ง
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, str(int(height)),
             ha='center', va='bottom', fontsize=12, color='black')

plt.show()
