import discord
import logging
import os
from pathlib import Path
from ics_writer import ics_writer
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('/help'):
        # Implement all the commands and their descriptions
        pass

    # Process commands after handling the message
    await bot.process_commands(message)

    # Creates a pool on whether person wants this info to be sent to the discord chat or not. If reacted with thumbs up then send in there.
bot.run(token, log_handler=handler, log_level=logging.DEBUG)