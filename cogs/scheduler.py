import discord
from discord.ext import commands
from discord.ui import Button, View
from pathlib import Path
from ics_writer import ics_writer

#ADD FILE COMMENT HERE

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def schedule(self, ctx):
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
        title_msg = await self.bot.wait_for('message', check=check)
        event['title'] = title_msg.content

        await ctx.author.send("Location of the event:")
        location_msg = await self.bot.wait_for('message', check=check)
        event['location'] = location_msg.content

        await ctx.author.send("Date (Format YYYY-MM-DD):")
        valid_date = False
        while not valid_date:
            date_msg = await self.bot.wait_for('message', check=check)
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

        await ctx.author.send("Start time (Eastern Time ET). Please use HH:MM (24-hour time format, e.g. 2pm would be 14:00):")
        valid_start_time = False
        while not valid_start_time:
            start_time_msg = await self.bot.wait_for('message', check=check)
            start_time_str = start_time_msg.content.strip()
            if len(start_time_str) == 5 and start_time_str.count(':') == 1:
                start_time_parts = start_time_str.split(':')
                if all(part.isdigit() for part in start_time_parts) and len(start_time_parts[0]) == 2 and len(start_time_parts[1]) == 2:
                    event['start_time'] = start_time_str
                    valid_start_time = True
                else:
                    await ctx.author.send("Invalid start time (Eastern Time ET). Please use HH:MM (24-hour time format, e.g. 2pm would be 14:00).")
            else:
                await ctx.author.send("Invalid start time (Eastern Time ET). Please use HH:MM (24-hour time format, e.g. 2pm would be 14:00).")
        
        await ctx.author.send("End time (Eastern Time ET). Please use HH:MM (24-hour time format):")
        valid_end_time = False
        while not valid_end_time:
            end_time_msg = await self.bot.wait_for('message', check=check)
            end_time_str = end_time_msg.content.strip()
            if len(end_time_str) == 5 and end_time_str.count(':') == 1:
                end_time_parts = end_time_str.split(':')
                if all(part.isdigit() for part in end_time_parts) and len(end_time_parts[0]) == 2 and len(end_time_parts[1]) == 2:
                    event['end_time'] = end_time_str
                    valid_end_time = True
                else:
                    await ctx.author.send("Invalid end time (Eastern Time ET). Please use HH:MM (24-hour time format).")
            else:
                await ctx.author.send("Invalid end time (Eastern Time ET). Please use HH:MM (24-hour time format).")
        
        event['uid'] = event['date'].replace("-", "") + "LabHelperEvent" # uid stands for unique ID, required for the creation of an ICS file so that we can write the calendar event file.
        
        await ctx.author.send("Any additional notes or links for the event? If none, please text \"none\".")
        description_msg = await self.bot.wait_for('message', check=check)
        event['description'] = description_msg.content

        await ctx.author.send("Please provide the email addresses of participants, separated by commas (include your own email):")
        emails_msg = await self.bot.wait_for('message', check=check)
        event['emails'] = []
        for email in emails_msg.content.split(","):
            email = email.replace(" ", "")
            event['emails'].append(email) # Make sure there is no space so that the invite can be correctly sent.
        
        event_info = (f"Here are the event details:\n"
                            f"**Title**: {event['title']}\n"
                            f"**Location**: {event['location']}\n"
                            f"**Date/Time**: {event['date']}, from {event['start_time']} to {event['end_time']}\n"
                            f"**Notes**: {event['description']}\n"
                            f"**Participants**: {', '.join(event['emails'])}\n")
        await ctx.author.send(event_info)
        # Send the file to the user.
        ics_file_path = ics_writer(event)
        try:
            await ctx.author.send(file=discord.File(ics_file_path))
        except FileNotFoundError:
            await ctx.author.send("The file was not found. Please check the path.")
        except Exception as e:
            await ctx.author.send(f"An error occurred: {e}")
        delete_file = Path(ics_file_path)
        delete_file.unlink()

        class PollView(View):
            def __init__(self):
                super().__init__()
                self.response = None

            @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
            async def yes_button(self, interaction: discord.Interaction, button: Button):
                self.response = "yes"
                await interaction.response.send_message("Got it! The event details will be sent to the server.", ephemeral=True)
                self.stop()

            @discord.ui.button(label="No", style=discord.ButtonStyle.red)
            async def no_button(self, interaction: discord.Interaction, button: Button):
                self.response = "no"
                await interaction.response.send_message("Understood! The event details will not be posted.", ephemeral=True)
                self.stop()

        # Check if the user wants the info (not the file) to the server as well.
        embed = discord.Embed(title="Do you want me to send the event details to the server?", description="Click **Yes** to send the event details to the server, or **No** to keep them private.\n" +
                            "Note that the .ics file won't be sent to the server since the invite will be sent via email once you open the file. " +
                            "Only the event information will be sent to the server so others can see.")
        poll_view = PollView()
        await ctx.author.send(embed=embed, view=poll_view)

        # Wait for the user to click a button
        await poll_view.wait()

        # Handle the user's response
        if poll_view.response == "yes":
            await ctx.send(f"New event created by {ctx.author.mention}!\n" + event_info)

async def setup(bot):
        """
        Required setup function for the Cog to be loaded.
        """
        await bot.add_cog(Scheduler(bot))