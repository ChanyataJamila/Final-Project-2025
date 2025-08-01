import pandas as pd

# โหลดไฟล์ CSV
df = pd.read_csv('output1.csv')  # เปลี่ยนชื่อไฟล์ตามจริง

# แปลง SBP เป็นตัวเลข (เผื่อมีข้อมูลเป็นข้อความ)
df['RR'] = pd.to_numeric(df['RR'], errors='coerce')

# สร้างคอลัมน์ใหม่ SBP_group ตามช่วงที่กำหนด
def map_rr(rr):
    if pd.isna(rr) or rr == 0:
        return 0
    elif 1 <= rr <= 5:
        return 1
    elif 6 <= rr <= 9:
        return 2
    elif 10 <= rr <= 29:
        return 3
    elif rr > 29:
        return 4
    else:
        return None  # สำหรับกรณีที่ไม่เข้าช่วงใดเลย

df['RR_group'] = df['RR'].apply(map_rr)

# บันทึกผลลัพธ์เป็นไฟล์ใหม่
df.to_csv('output1.csv', index=False)

print("✅ สร้างคอลัมน์ SBP_group เรียบร้อยแล้ว และบันทึกลงไฟล์ with_sbp_group.csv")