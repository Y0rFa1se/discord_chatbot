from dotenv import dotenv_values
import discord
from discord.ext import commands
import asyncio
import aiohttp
import json
import base64

from modules.gpt import (
    openai_init,
    render_requests,
    render_image,
    render_pdf,
    render_responses,
    gpt_request
)

MODELS = json.load(open("models.json", "r"))
print(MODELS)

ENV_DICT = dotenv_values(".env")

gpt_client = openai_init(ENV_DICT["GPT_API"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

CHUNK_SIZE = int(ENV_DICT["CHUNK_SIZE"])

HISTORY = []

@bot.event
async def on_ready():
    global HISTORY

    print(f"Bot is ready as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.playing, name="hi")

    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    global HISTORY
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
        print("attachment")
        for attachment in message.attachments:
            if attachment.content_type:
                print(attachment.content_type)
                if attachment.content_type.startswith("image/"):
                    file_data = await attachment.read()
                    file_data = base64.b64encode(file_data).decode("utf-8")
                    file_ext = attachment.content_type.split("/")[1]

                    HISTORY = render_image(file_data, file_ext, HISTORY)
                
                if attachment.content_type.startswith("application/"):
                    file_data = await attachment.read()
                    file_data = base64.b64encode(file_data).decode("utf-8")
                    file_ext = attachment.content_type.split("/")[1]

                    if file_ext == "pdf":
                        HISTORY = render_pdf(file_data, HISTORY)
    
    if message.content:
        requests = message.content
        HISTORY = render_requests(requests, HISTORY)
        responses = gpt_request(gpt_client, MODEL, HISTORY)

        msg = await message.channel.send("Typing...")
        collected = ""

        for idx, chunk in enumerate(responses):
            try:
                collected += chunk.delta

                if idx % CHUNK_SIZE == 0:
                    try:
                        await asyncio.wait_for(msg.edit(content=collected), timeout=30)

                    except asyncio.TimeoutError:
                        print("Timeout error, skipping edit.")
                        await msg.edit(content="Timeout Error")
                        continue

            except Exception as e:
                print(f"Error: {e}")

        await msg.edit(content=collected)

        HISTORY = render_responses(collected, HISTORY)

    await bot.process_commands(message)

bot.run(ENV_DICT["CHATBOT_TOKEN"])