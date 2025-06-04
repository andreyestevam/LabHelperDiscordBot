import discord
import logging
import asyncio
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

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load_cogs()
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())