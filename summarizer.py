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

    # แบ่งข้อความออกเป็นส่วนๆ หากข้อความยาวเกินไป
    max_input_length = 1024  # ขนาดสูงสุดที่โมเดลสามารถรับได้
    text_tokens = tokenizer.encode(text, truncation=True, max_length=max_input_length)

    # แบ่งข้อความออกเป็นหลายๆ ชิ้นหากมีความยาวเกินไป
    chunks = [text[i:i+max_input_length] for i in range(0, len(text_tokens), max_input_length)]
    
    # สรุปแต่ละชิ้นส่วน
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=800, min_length=50, do_sample=False, length_penalty=2.0)
        summaries.append(summary[0]["summary_text"])

    # รวมสรุปทั้งหมด
    full_summary = " ".join(summaries)
    
    # คืนค่าผลลัพธ์ที่ได้
    return full_summary