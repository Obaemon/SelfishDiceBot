import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not found.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"{bot.user} LOGIN")

@bot.command()
async def ping(ctx):
    await ctx.send("Hello?")

bot.run(TOKEN)