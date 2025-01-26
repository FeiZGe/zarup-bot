from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import pipeline

# ตั้งค่าโฟลเดอร์เก็บโมเดล
model_path = "./models/distilbart-cnn-12-6"

# ใช้โมเดลจาก path
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# ฟังก์ชันสำหรับสรุปข้อความ
def summarize_article(text):
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    # กำหนดขนาดสูงสุดของข้อความที่ต้องการ (max_length 100-200 ขึ้นอยู่กับความยาวของข้อความ)
    chunk_size = 1024  # ขนาดข้อความที่โมเดลรองรับ 1024
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]  # แบ่งข้อความเป็นส่วนๆ

    summaries = []
    for chunk in chunks:
        # ปรับ max_length ตามขนาดของข้อความที่ส่งเข้ามา
        chunk_length = len(chunk.split())  # นับคำในข้อความ
        if chunk_length <= 50:
            max_length = 50
        elif chunk_length <= 100:
            max_length = 100
        else:
            max_length = 200

        summary = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
        summaries.append(summary[0]["summary_text"])

    # รวมผลลัพธ์จากแต่ละส่วน
    final_summary = ' '.join(summaries)

    return final_summary