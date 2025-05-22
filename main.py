import discord
import logging
import os
from ics_writer import ics_writer
from dotenv import load_dotenv
from discord.ext import commands

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
    
    await ctx.message.delete()
    event = dict() # This dictionary will hold all the info about the event.
    
    # Send a DM to the user. Then, all the info will be handled through the DM for privacy purposes.
    await ctx.author.send(f"Hey, {ctx.author}! Let's schedule a meeting. Please provide the following details:")

    await ctx.author.send("Title of the event:")
    title_msg = await bot.wait_for('message', check=check)
    event['title'] = title_msg.content

    await ctx.author.send("Location of the event:")
    location_msg = await bot.wait_for('message', check=check)
    event['location'] = location_msg.content

    await ctx.author.send("Date (Format YYYY-MM-DD):")
    valid_date = False
    while not valid_date:
        date_msg = await bot.wait_for('message', check=check)
        date_str = date_msg.content.strip()
        if len(date_str) == 10 and date_str.count('-') == 2:
            date_parts = date_str.split('-')
            if all(part.isdigit() for part in date_parts) and len(date_parts[0]) == 4 and len(date_parts[1]) == 2 and len(date_parts[2]) == 2:
                event['date'] = date_str
                valid_date = True
            else:
                await ctx.author.send("Invalid date format. Please use YYYY-MM-DD.")
        else:
            await ctx.author.send("Invalid date format. Please use YYYY-MM-DD.")

    await ctx.author.send("Start time (format HH:MM):")
    valid_start_time = False
    while not valid_start_time:
        start_time_msg = await bot.wait_for('message', check=check)
        start_time_str = start_time_msg.content.strip()
        if len(start_time_str) == 5 and start_time_str.count(':') == 1:
            start_time_parts = start_time_str.split(':')
            if all(part.isdigit() for part in start_time_parts) and len(start_time_parts[0]) == 2 and len(start_time_parts[1]) == 2:
                event['start_time'] = start_time_str
                valid_start_time = True
            else:
                await ctx.author.send("Invalid start time. Please use HH:MM.")
        else:
            await ctx.author.send("Invalid start time. Please use HH:MM.")
    
    await ctx.author.send("End time (format HH:MM):")
    valid_end_time = False
    while not valid_end_time:
        end_time_msg = await bot.wait_for('message', check=check)
        end_time_str = end_time_msg.content.strip()
        if len(end_time_str) == 5 and end_time_str.count(':') == 1:
            end_time_parts = end_time_str.split(':')
            if all(part.isdigit() for part in end_time_parts) and len(end_time_parts[0]) == 2 and len(end_time_parts[1]) == 2:
                event['end_time'] = end_time_str
                valid_end_time = True
            else:
                await ctx.author.send("Invalid end time. Please use HH:MM.")
        else:
            await ctx.author.send("Invalid end time. Please use HH:MM.")
    
    event['uid'] = event['date'] + "LabHelperEvent" # uid stands for unique ID, required for the creation of an ICS file so that we can write the calendar event file. 
    
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
                          f"**Participants**: {', '.join(event['emails'])}\n")
    
    # Send the file to the user.
    ics_file_path = ics_writer(event)
    try:
        await ctx.author.send(file=discord.File(ics_file_path))
    except FileNotFoundError:
        await ctx.author.send("The file was not found. Please check the path.")
    except Exception as e:
        await ctx.author.send(f"An error occured: {e}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)