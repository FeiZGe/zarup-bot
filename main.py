import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load the token from the .env file
load_dotenv()
token = os.getenv("BOT_TOKEN")

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True  # เปิดให้บอทอ่านข้อความได้

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)