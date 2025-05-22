import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime

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
    
    event = dict() # This dictionary will hold all the info about the event.
    
    # Send a DM to the user. Then, all the info will be handled through the DM for privacy purposes.
    await ctx.author.send(f"Hey, {ctx.author}! Let's schedule a meeting. Please provide the following details:")

    await ctx.author.send("Title of the event:")
    title_msg = await bot.wait_for('message', check=check)
    event['title'] = title_msg.content

    await ctx.author.send("Location of the event:")
    location_msg = await bot.wait_for('message', check=check)
    event['location'] = location_msg.content

    await ctx.author.send("Date (Format YYYY-MM-DD HH:MM):")
    valid_date = False
    while not valid_date:
        date_msg = await bot.wait_for('message', check=check)
        try:
            event['date'] = datetime.strptime(date_msg.content, "%Y-%m-%d %H:%M")
            valid_date = True
        except ValueError:
            await ctx.author.send("Invalid date/time format. Please use YYYY-MM-DD HH:MM.")
    
    await ctx.author.send("Any additional notes or links for the event? If none, please text \"none\".")
    description_msg = await bot.wait_for('message', check=check)
    event['description'] = description_msg.content

    await ctx.author.send("Please provide the email addresses of participants, separated by commas (include your own email):")
    emails_msg = await bot.wait_for('message', check=check)
    event['emails'] = []
    for email in emails_msg.content.split(","):
        event['emails'].append(email)
    
    await ctx.author.send(f"Here are the event details:\n"
                          f"**Title**: {event['title']}\n"
                          f"**Location**: {event['location']}\n"
                          f"**Date/Time**: {event['date']}\n"
                          f"**Notes**: {event['description']}\n"
                          f"**Participants**: {', '.join(event['emails'])}\n"
                          f"Sending invites... please check your email soon for more details!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)