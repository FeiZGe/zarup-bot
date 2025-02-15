import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder

# ✅ กำหนดฟอนต์ไทยสำหรับ Matplotlib
font_path = os.path.join(os.path.dirname(__file__), "../assets/fonts/Prompt-Regular.ttf")
font_prop = fm.FontProperties(fname=font_path)

# ✅ โฟลเดอร์สำหรับบันทึกรูปภาพ
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "../assets/graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

def cluster_frequent_problems(data, province, n_clusters=7):
    # จัดกลุ่มปัญหาที่พบบ่อยในจังหวัดที่เลือก โดยใช้ K-Means Clustering
    try:
        # ✅ คัดเลือกข้อมูลเฉพาะจังหวัดที่เลือก
        data = data[data["province"] == province]

        if data.empty:
            raise ValueError(f"❌ ไม่พบข้อมูลสำหรับจังหวัด {province}")

        # ✅ รวมจำนวนปัญหาแต่ละประเภท
        problem_counts = data.groupby("Problem_Type")["Total"].sum().reset_index()
        problem_counts = problem_counts.sort_values(by="Total", ascending=False)

        # ✅ ใช้ One-Hot Encoding
        encoder = OneHotEncoder(sparse_output=False)
        encoded_data = encoder.fit_transform(problem_counts[["Problem_Type"]])

        # ✅ ใช้ PCA ลดมิติข้อมูลเหลือ 2D
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(encoded_data)

        # ✅ ใช้ K-Means Clustering
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = model.fit_predict(reduced_data)

        # ✅ รวมผลลัพธ์
        problem_counts["Cluster"] = clusters

        # ✅ สร้าง Label ให้ Legend (ใช้ชื่อปัญหาหลายชื่อในแต่ละกลุ่ม)
        cluster_labels = {
            i: ", ".join(problem_counts[problem_counts["Cluster"] == i]["Problem_Type"].values)
            for i in range(n_clusters)
        }

        # ✅ วาดกราฟ
        plt.figure(figsize=(8, 6))
        scatter = sns.scatterplot(
            x=reduced_data[:, 0], 
            y=reduced_data[:, 1],  
            hue=[cluster_labels[c] for c in clusters], 
            palette="Set1",
            alpha=0.7
        )

        # ✅ เพิ่มชื่อปัญหาลงในกราฟ
        for i, txt in enumerate(problem_counts["Problem_Type"]):
            plt.annotate(txt, (reduced_data[i, 0], reduced_data[i, 1]), fontsize=10, alpha=0.75, fontproperties=font_prop)

        plt.title(f"🔍 กลุ่มปัญหาที่พบบ่อยใน {province}", fontproperties=font_prop)
        plt.xlabel("ปัจจัยหลักที่อธิบายข้อมูล", fontproperties=font_prop)
        plt.ylabel("ปัจจัยรองที่อธิบายข้อมูล", fontproperties=font_prop)
        plt.legend(prop=font_prop)

        # ✅ บันทึกกราฟ
        graph_path = os.path.join(GRAPH_DIR, f"cluster_{province}.png")
        plt.savefig(graph_path, dpi=100, bbox_inches="tight")
        plt.close()

        # ✅ เตรียมข้อมูลแสดงใน Embed
        top_problems = "\n".join(
            [f"**{row['Problem_Type']}**: {row['Total']} ครั้ง" for _, row in problem_counts.iterrows()]
        )

        return top_problems, graph_path
    
    except Exception as e:
        print(f"🔴 Error in cluster_frequent_problems: {e}")
        return None, None
