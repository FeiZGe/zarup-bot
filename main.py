import discord
from discord.ext import commands
import asyncio

import os
from dotenv import load_dotenv

# Load the token from the .env file
load_dotenv()
token = os.getenv("BOT_TOKEN")

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # เปิดให้บอทอ่านข้อความได้
intents.messages = True  # เปิดให้บอทอ่านข้อความได้

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# โหลด cogs จากโฟลเดอร์ cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")  # ใช้ await กับ load_extension
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

async def main():
    try:
        async with bot:
            await load_cogs()
            await bot.start(token)
    except Exception as e:
        print(f"Unexpected error: {e}")

# รันบอท
try:
    asyncio.run(main()) # บอทเริ่มทำงาน
except KeyboardInterrupt: # จัดการ KeyboardInterrupt ^C เพื่อหยุดการทำงานของโปรแกรม ที่นี่
    print("\nBot is shutting down...")  # แสดงข้อความเมื่อหยุดโปรแกรม