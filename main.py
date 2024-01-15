import discord
import aiohttp
import random
import asyncio
import os
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
keep_alive()

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="&", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

async def fetch_user_messages(session, channel, author, mentions, history_limit):
    user_messages = []
    async for msg in channel.history(limit=history_limit):
        # Exclude the bot's messages from the history
        if msg.author == bot.user:
            continue

        msg_content = msg.content.strip()
        if msg_content:
            user_messages.append(msg_content)
    return user_messages

async def process_message(message, bot_emojis):
    channel = message.channel

    async with channel.typing():
        history_limit = random.randint(1, 10000)

        async with aiohttp.ClientSession() as session:
            user_messages = await fetch_user_messages(session, channel, message.author, message.mentions, history_limit)

        if user_messages:
            random_message_content = random.choice(user_messages)

            excluded_emojis = [
                "baslamaBar", "baslangicBar", "bosBitisBar", "bosBar",
                "doluBar", "doluBitisBar", "loading_bg", "loading",
                "exclamation_mark", "error", "death_note53", "animeyay",
                "1037831738707165214", "850656705322156052",
                "Wheel_No", "Wheel_No1", "Wheel_No2", "Wheel_No3", "Wheel_No4", "Wheel_No5",
                "Wheel_No6", "Wheel_Yes", "Wheel_Yes1", "Wheel_Yes2", "Wheel_Yes3", "Wheel_Yes4",
                "Wheel_Yes5", "Wheel_Yes6", "Wheel_Yes7", "Wherl_No7", "gatito_loading", "no",
                "sucess", "yes", "check", "out"
            ]

            # Get a random emoji from any server the bot has joined (excluding the specified ones)
            emoji = random.choice([e for e in bot_emojis if e.name not in excluded_emojis])

            # Send the random emoji at the end of the same message with a blank space
            await message.reply(f"{random_message_content} {str(emoji)}")
        else:
            await message.reply('a')

async def process_messages(message, bot_emojis):
    task = process_message(message, bot_emojis)
    await asyncio.gather(task)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        bot_emojis = bot.emojis
        await process_messages(message, bot_emojis)

@bot.event
async def on_disconnect():
    print("Bot disconnected. Reconnecting...")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error in {event}: {args[0]}")
    if isinstance(args[0], discord.ConnectionClosed):
        print("Reconnecting...")
        await asyncio.sleep(5)  # Add a delay before attempting to reconnect
        await bot.login(token, bot=True)
        await bot.connect()

token = os.getenv("token")

if token is None:
    print("Error: Token not found in environment variables.")
else:
    bot.run(token)
