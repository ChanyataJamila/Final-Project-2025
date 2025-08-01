import pandas as pd

# โหลดไฟล์ (ตัวอย่าง: สมมติไฟล์ชื่อ data.csv)
df = pd.read_csv('output1.csv')

# สลับค่า: 0 -> 1, 1 -> 0
df['Dead'] = 1 - df['Dead']

# บันทึกไฟล์ใหม่เป็น CSV (ไม่เอา index)
df.to_csv('output3.csv', index=False)