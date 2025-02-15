import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os

# ✅ กำหนดฟอนต์ไทยสำหรับ Matplotlib
font_path = os.path.join(os.path.dirname(__file__), "../assets/fonts/Prompt-Regular.ttf")
font_prop = fm.FontProperties(fname=font_path)

# ✅ โฟลเดอร์สำหรับบันทึกรูปภาพ
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "../assets/graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

def generate_problem_heatmap(data, province):
    """สร้าง Heatmap แสดงจำนวนปัญหาที่พบบ่อยในจังหวัดที่เลือก"""
    try:
        # คัดเลือกข้อมูลเฉพาะจังหวัดที่เลือก
        data = data[data["province"] == province]

        if data.empty:
            raise ValueError(f"❌ ไม่พบข้อมูลสำหรับจังหวัด {province}")

        # รวมจำนวนปัญหาแต่ละประเภทและเรียงลำดับ
        problem_counts = data.groupby("Problem_Type")["Total"].sum().reset_index()
        problem_counts = problem_counts.sort_values(by="Total", ascending=False).reset_index(drop=True)

        # สรุปข้อมูลโดยใช้ Pivot Table
        summary_data = data.pivot_table(index="Problem_Type", columns="work_year", values="Total", aggfunc="sum").fillna(0)

        # สร้าง Heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(summary_data, cmap="crest", annot=True, fmt=".0f", annot_kws={"size": 16})
        plt.title(f"🔍 การร้องเรียนแต่ละประเภทใน {province}", fontproperties=font_prop)
        plt.xlabel("ปี", fontproperties=font_prop)
        plt.ylabel("ประเภทปัญหา", fontproperties=font_prop)

        # แสดงฟอนต์ไทย แกน y
        plt.yticks(fontproperties=font_prop)
        
        # บันทึกกราฟ
        graph_path = os.path.join(GRAPH_DIR, f"heatmap_{province}.png")
        plt.savefig(graph_path, dpi=100, bbox_inches="tight")
        plt.close()

        # เตรียมข้อมูลแสดงใน Embed
        top_problems = "\n".join(
            [f"{i+1}. **{row['Problem_Type']}**: {row['Total']} ครั้ง" for i, row in problem_counts.iterrows()]
        )

        return top_problems, graph_path
    
    except Exception as e:
        print(f"🔴 Error in generate_problem_heatmap: {e}")
        return None
