import pandas as pd

df = pd.read_csv('DataHead_01.csv')

columns_to_change = ['Ais1', 'Ais2', 'Ais3', 'Ais4', 'Ais5', 'Ais6']

# วนลูปแปลงเลข 9 → 0 ในคอลัมน์ที่กำหนด
for col in columns_to_change:
    df[col] = df[col].astype(str).str.replace('9', '0').astype(int)

 # บันทึกกลับเป็น CSV ใหม่
df.to_csv('DataHead_01output.csv', index=False)

print("✔️ บันทึกไฟล์ใหม่เป็น output.csv พร้อมแปลงเลข 9 → 0 แล้วเรียบร้อย")