from dotenv import dotenv_values
import discord
from discord.ext import commands
import asyncio
import aiohttp
import json

from modules.gpt import (
    openai_init,
    render_requests,
    render_image,
    render_responses,
    gpt_request
)

MODELS = json.load(open("models.json", "r"))
print(MODELS)

ENV_DICT = dotenv_values(".env")

gpt_client = openai_init(ENV_DICT["GPT_API"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

CHUNK_SIZE = int(ENV_DICT["CHUNK_SIZE"])

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.playing, name="hi")

    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    MODEL = str(message.channel.category).lower()

    print(f"Message from {message.author}: {message.content} in {MODEL}")

    if MODEL == "test":
        await message.channel.send("test")
        return
    
    if MODEL not in MODELS:
        return

    if message.author.bot:
        return

    if message.attachments:
        return # TODO: handle attachments
    
    if message.content:
        requests = message.content
        history = render_requests(requests)
        print(history)
        responses = gpt_request(gpt_client, MODEL, history)

        msg = await message.channel.send("Typing...")
        collected = ""

        for idx, chunk in enumerate(responses):
            try:
                collected += chunk.delta

                if idx % CHUNK_SIZE == 0:
                    try:
                        await asyncio.wait_for(msg.edit(content=collected), timeout=1)

                    except asyncio.TimeoutError:
                        print("Timeout error, skipping edit.")
                        await msg.edit(content="Timeout Error")
                        continue

            except Exception as e:
                print(f"Error: {e}")

        await msg.edit(content=collected)

    await bot.process_commands(message)

bot.run(ENV_DICT["CHATBOT_TOKEN"])