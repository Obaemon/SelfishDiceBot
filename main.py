import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import re
import random

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

def parseStringToDiceroll(content: str):
    _DICE_RE = re.compile(r"(\d+)[dD](\d+)")
    return _DICE_RE.fullmatch(content)

def parseStringToPickroll(content: str):
    _PICK_RE = re.compile(r"(\d+)[cC](\d+)")
    return _PICK_RE.fullmatch(content)

def diceroll(count: int, number: int) -> list[int]:
    result = [random.randint(1, number) for _ in range(count)]
    result.sort()
    return result

def pickroll(count: int, number: int) -> list[int]:
    result = random.sample(range(1, number + 1), count)
    result.sort()
    return result

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} LOGIN")

@bot.tree.command(name="ping", description="もしもーし？")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Hello?")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    content = message.content.strip()
    print(message)
    print(content)
    if parsedString := parseStringToDiceroll(content):
        print("Diceroll detected")
        reply = diceroll(int(parsedString.group(1)), int(parsedString.group(2)))
        await message.reply(reply)

    elif parsedString := parseStringToPickroll(content):
        print("Pickroll detected")
        reply = pickroll(int(parsedString.group(1)), int(parsedString.group(2)))
        await message.reply(reply)

    await bot.process_commands(message)

bot.run(TOKEN)