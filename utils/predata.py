import pandas as pd

def load_data():
    df = pd.read_csv('data/data-complain.csv')
    data = df[df['Case_Objective'] == 'ร้องเรียน/ร้องทุกข์']
    return data

print(load_data().head()) # แสดงข้อมูล 5 แถวแรก
print(f"แต่ละคอลลัมน์มีค่าว่างกี่ค่า\n {load_data().isnull().sum()} \n=====================")
print(f"มีข้อมูลซ้ำ = {load_data().duplicated().sum()} แถว")