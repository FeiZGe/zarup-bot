import discord
from discord.ext import commands
import requests
import re
from bs4 import BeautifulSoup

from summarizer import summarize_article  # ฟังก์ชันสรุปจาก summarizer.py

import os
from dotenv import load_dotenv

# Load the token from the .env file
load_dotenv()
token = os.getenv("BOT_TOKEN")

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # เปิดให้บอทอ่านข้อความได้

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD = int(os.getenv("GUILD_ID"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="summarize", description="สรุปบทความจาก <URL>", guild=GUILD)
async def summarize(ctx, url: str):
    if ctx.author == bot.user:
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
        sentence_endings = re.compile(r'(?<=[.!?])\s+')  # กำหนดให้ตัดข้อความหลังเครื่องหมาย . , ? , !
        sentences = sentence_endings.split(summary)  # แยกข้อความเป็นประโยค

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

bot.run(token)