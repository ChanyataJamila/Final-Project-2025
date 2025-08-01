import pandas as pd

# โหลดไฟล์
df = pd.read_csv('output1.csv')  # เปลี่ยนชื่อไฟล์ให้ถูก

# แสดงชื่อคอลัมน์เพื่อเช็กว่าตรงหรือไม่
print(df.columns.tolist())

# แปลงค่าคอลัมน์ให้เป็นตัวเลข (ถ้าเป็นข้อความ)
df['GCS'] = pd.to_numeric(df['GCS'], errors='coerce')
df['SBP_group'] = pd.to_numeric(df['SBP_group'], errors='coerce')
df['RR_group']  = pd.to_numeric(df['RR_group'], errors='coerce')

# เติม 0 ถ้าข้อมูลหาย
df[['GCS', 'SBP_group', 'RR_group']] = df[['GCS', 'SBP_group', 'RR_group']].fillna(0)

# คำนวณ RTS
df['RTS'] = (
    0.9368 * df['GCS'] +
    0.7326 * df['SBP_group'] +
    0.2908 * df['RR_group']
)

# ปัดทศนิยม (ถ้าต้องการ)
df['RTS'] = df['RTS'].round(2)

# บันทึกกลับไฟล์
df.to_csv('output1.csv', index=False)

print("✅ คำนวณ RTS เสร็จเรียบร้อย!")