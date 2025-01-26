import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

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

class SummarizeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="summarize", description="สรุปบทความจาก <URL>")
    async def summarize(self, ctx, url: str):
        if ctx.author == self.bot.user:
            return

        try:
            # ดึงบทความจาก URL
            response = requests.get(url)
            response.encoding = 'utf-8'
            response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับ
            soup = BeautifulSoup(response.text, 'html.parser')
            text = " ".join([p.text for p in soup.find_all('p')])

            # แสดงข้อความว่า "กำลังสรุป..."
            message = await ctx.send("กำลังสรุป...")

            # สรุปบทความ
            summary = summarize_article(text)

            # แบ่งข้อความสรุปเป็นประโยค โดยใช้ regex เพื่อตัดที่จุดสิ้นสุดของประโยค
            sentence_endings = re.compile(r'(?<=[.!?])\s+')
            sentences = sentence_endings.split(summary)

            # ใช้ textwrap เพื่อตัดข้อความเป็นหลายส่วนที่มีความยาวไม่เกิน 2000 ตัวอักษร
            chunked_summary = []
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk + sentence) > 2000:
                    chunked_summary.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += " " + sentence

            if current_chunk:
                chunked_summary.append(current_chunk.strip())

            # ส่งข้อความสรุปภาษาอังกฤษ
            for part in chunked_summary:
                embed = discord.Embed(
                    title="Summary in English",
                    description=part,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

            await message.delete()

        except requests.exceptions.RequestException as e:
            await ctx.send(f"Error fetching the article: {str(e)}")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
async def setup(bot):
    await bot.add_cog(SummarizeCog(bot))