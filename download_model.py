from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# กำหนดโฟลเดอร์โปรเจคที่ต้องการเก็บ
model_path = "./models/sshleifer-distilbart-cnn-12-6"

# ดาวน์โหลดและบันทึกโมเดล
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6", cache_dir=model_path)
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6", cache_dir=model_path)

print(f"Model and tokenizer saved to {model_path}")