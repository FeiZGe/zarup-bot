import os
import pandas as pd

# โหลดข้อมูล
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "../data/data-complain.csv")  # กำหนด path ให้ถูกต้อง
    df = pd.read_csv(file_path)

    # กรองข้อมูลที่เป็น 'ร้องเรียน/ร้องทุกข์' เท่านั้น
    data = df[df['Case_Objective'] == 'ร้องเรียน/ร้องทุกข์']
    return data

# แสดงประเภทปัญหาที่ซ้ำกัน
def problem_type(data):
    return data['Problem_Type'].drop_duplicates()

# แสดงข้อมูลตัวอย่าง
if __name__ == "__main__":
    data = load_data()
    print(data.head())  # แสดง 5 แถวแรก
    print(f"🔍 แต่ละคอลัมน์มีค่าว่างกี่ค่า:\n{data.isnull().sum()}\n=====================")
    print(f"🔄 มีข้อมูลซ้ำทั้งหมด: {data.duplicated().sum()} แถว")
    print(f"📌 ประเภทปัญหาที่พบ:\n{problem_type(data)}")
