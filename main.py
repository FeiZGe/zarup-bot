import discord
from discord.ext import commands
import requests
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
        response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับ
        soup = BeautifulSoup(response.text, 'html.parser')
        text = " ".join([p.text for p in soup.find_all('p')])

        # สรุปบทความ
        summary = summarize_article(text)
        await ctx.send(f"Summary:\n{summary}")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching the article: {str(e)}")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

bot.run(token)