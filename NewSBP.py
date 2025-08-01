import pandas as pd

# โหลดไฟล์ CSV
df = pd.read_csv('output1.csv')  # เปลี่ยนชื่อไฟล์ตามจริง

# แปลง SBP เป็นตัวเลข (เผื่อมีข้อมูลเป็นข้อความ)
df['SBP'] = pd.to_numeric(df['SBP'], errors='coerce')

# สร้างคอลัมน์ใหม่ SBP_group ตามช่วงที่กำหนด
def map_sbp(sbp):
    if pd.isna(sbp) or sbp == 0:
        return 0
    elif 1 <= sbp <= 49:
        return 1
    elif 50 <= sbp <= 75:
        return 2
    elif 76 <= sbp <= 89:
        return 3
    elif sbp > 89:
        return 4
    else:
        return None  # สำหรับกรณีที่ไม่เข้าช่วงใดเลย

df['SBP_group'] = df['SBP'].apply(map_sbp)

# บันทึกผลลัพธ์เป็นไฟล์ใหม่
df.to_csv('output1.csv', index=False)

print("✅ สร้างคอลัมน์ SBP_group เรียบร้อยแล้ว และบันทึกลงไฟล์ with_sbp_group.csv")