import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from statsmodels.tsa.arima.model import ARIMA

# กำหนดฟอนต์ไทยสำหรับ Matplotlib
font_path = os.path.join(os.path.dirname(__file__), "../assets/fonts/Prompt-Regular.ttf")
font_prop = fm.FontProperties(fname=font_path)

# โฟลเดอร์สำหรับบันทึกรูปภาพ
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "../assets/graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

def predict_future_complaints(data, problem_type, province):
    # พยากรณ์จำนวนเรื่องร้องทุกข์ในอนาคต (รายปี) พร้อมสร้างและบันทึกกราฟ

    try:
        if "work_year" not in data.columns:
            raise ValueError("❌ DataFrame ไม่มีคอลัมน์ 'work_year'!")

        # กรองข้อมูล
        filtered_data = data[(data["Problem_Type"] == problem_type) & (data["province"] == province)]
        if filtered_data.empty:
            raise ValueError(f"❌ ไม่มีข้อมูลสำหรับประเภท '{problem_type}' ในจังหวัด '{province}'")

        # รวมค่ารายปี
        filtered_data = (
            filtered_data.groupby("work_year")["Total"]
            .sum()
            .reset_index()
        )

        # ตั้งค่า index เป็น datetime และใช้ความถี่รายปี
        filtered_data["date"] = pd.to_datetime(filtered_data["work_year"].astype(str) + "-12-31")
        filtered_data.set_index("date", inplace=True)
        filtered_data = filtered_data.asfreq("YE")  

        if len(filtered_data) < 5:  
            raise ValueError("❌ ข้อมูลมีขนาดเล็กเกินไปสำหรับ ARIMA (ต้องมีอย่างน้อย 5 ปี)")

        # ใช้ ARIMA พยากรณ์
        model = ARIMA(filtered_data["Total"], order=(2, 1, 0))  
        model_fit = model.fit()
        prediction = model_fit.forecast(steps=1)
        predicted_value = round(prediction.iloc[0])  

        # กำหนดชื่อไฟล์แบบเฉพาะเจาะจง
        filename = f"complaints_{problem_type}_{province}.png".replace(" ", "_")
        filepath = os.path.join(GRAPH_DIR, filename)

        # ตรวจสอบว่ารูปมีอยู่แล้วหรือไม่
        if os.path.exists(filepath):
            return predicted_value, filepath

        # สร้างกราฟ
        plt.figure(figsize=(8, 5))
        plt.plot(filtered_data.index, filtered_data["Total"], marker="o", linestyle="-", label="ข้อมูลจริง", color="blue")
        plt.axvline(filtered_data.index[-1], color="gray", linestyle="--", label="จุดพยากรณ์")
        plt.scatter(pd.to_datetime(f"{filtered_data.index[-1].year + 1}-12-31"), predicted_value, color="red", label=f"พยากรณ์: {predicted_value}")
        plt.xlabel("ปี", fontproperties=font_prop)
        plt.ylabel("จำนวนร้องทุกข์", fontproperties=font_prop)
        plt.title(f"📊 พยากรณ์เรื่องร้องเรียน ({problem_type} - {province})", fontproperties=font_prop)
        plt.legend(prop=font_prop)
        plt.grid(True)

        # บันทึกภาพลงไฟล์
        plt.savefig(filepath, format="png", dpi=100, bbox_inches="tight")
        plt.close()

        return predicted_value, filepath

    except Exception as e:
        print(f"🔴 Error in predict_future_complaints: {e}")
        return None, None
