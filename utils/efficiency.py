import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# กำหนดฟอนต์ไทยสำหรับ Matplotlib
font_path = os.path.join(os.path.dirname(__file__), "../assets/fonts/Prompt-Regular.ttf")
font_prop = fm.FontProperties(fname=font_path)

# โฟลเดอร์สำหรับบันทึกรูปภาพ
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "../assets/graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

def evaluate_efficiency(data, province):
    try:
        # คัดเลือกข้อมูลเฉพาะจังหวัดที่เลือก
        province_data = data[data["province"] == province]
        
        if province_data.empty:
            raise ValueError(f"❌ ไม่พบข้อมูลสำหรับจังหวัด {province}")
        
        # นับจำนวน Case_Status ในแต่ละปี
        status_counts = province_data.groupby(["work_year", "Case_Status"]).size().reset_index(name="count")
        
        # สร้างกราฟ boxplot เปรียบเทียบการกระจายของจำนวนเคส
        plt.figure(figsize=(10, 6))
        sns.barplot(data=status_counts, x="work_year", y="count", hue="Case_Status", ci=None)

        plt.title(f"📊 ประสิทธิภาพการแก้ปัญหาใน {province}", fontproperties=font_prop)
        plt.xlabel("ปี", fontproperties=font_prop)
        plt.ylabel("จำนวนเคส", fontproperties=font_prop)
        plt.legend(title="สถานะ", prop=font_prop)
        
        # บันทึกกราฟ
        graph_path = os.path.join(GRAPH_DIR, f"efficiency_{province}_boxplot.png")
        plt.savefig(graph_path, dpi=100, bbox_inches="tight")
        plt.close()
        
        # สรุปผลลัพธ์
        summary_text = ""
        # ใช้ข้อมูลจาก status_counts ที่ได้ทำการคำนวณไว้แล้ว
        for year in status_counts["work_year"].unique():
            year_data = status_counts[status_counts["work_year"] == year]
            # นับจำนวนเคสที่ยุติและรอผลการพิจารณาในแต่ละปี
            ended_count = year_data[year_data["Case_Status"] == "ยุติเรื่อง"]["count"].sum()
            pending_count = year_data[year_data["Case_Status"] == "รอผลการพิจารณา"]["count"].sum()
            
            # แสดงผลในรูปแบบข้อความ
            summary_text += f"ปี {year}: ยุติเรื่อง {ended_count} เคส, รอผลการพิจารณา {pending_count} เคส\n"
        
        return graph_path, summary_text
    
    except Exception as e:
        print(f"🔴 Error in evaluate_efficiency: {e}")
        return None, None
