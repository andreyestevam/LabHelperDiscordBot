import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

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

@bot.command()
async def schedule(ctx):
    '''
    This command, when triggered, will collect the information from the user so that a calendar event
    can be created using the information provided. The user will provide the title, location, date and
    time, description or links (optional), as well as provide the email of all of the invitees.

    When all the information is finally provided, the LabHelper will send the invites via email to all
    the invitees and send a message on the Discord server so that everyone can see which event was scheduled.
    '''
    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
    

bot.run(token, log_handler=handler, log_level=logging.DEBUG)