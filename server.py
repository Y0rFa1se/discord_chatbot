from dotenv import dotenv_values
import discord
from discord.ext import commands

ENV_DICT = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.playing, name="hi")

    await bot.change_presence(activity=activity)


bot.run(ENV_DICT["SERVER_TOKEN"])