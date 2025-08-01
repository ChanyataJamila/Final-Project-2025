import pandas as pd

df = pd.read_csv('DataHead_01output.csv')

columns_to_compare = ['Ais1', 'Ais2', 'Ais3', 'Ais4', 'Ais5', 'Ais6']

# หา 3 ค่าที่มากที่สุดในแต่ละแถว → ยกกำลัง 2 → บวกกัน
df['ISS'] = df[columns_to_compare].apply(
    lambda row: sum([x**2 for x in sorted(row, reverse=True)[:3]]),
    axis=1
)

# บันทึกกลับลงในไฟล์ CSV เดิม หรือชื่อใหม่
df.to_csv('output1.csv', index=False)

print("✔️ คำนวณเสร็จแล้ว ใส่ผลลัพธ์ลงในคอลัมน์ 'result' ที่มีอยู่เรียบร้อย")