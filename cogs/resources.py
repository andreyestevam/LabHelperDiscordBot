import discord
from discord.ext import commands
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

class Resources(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect('resources.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS resources (
                        resource_title TEXT NOT NULL,
                        description TEXT,
                        link TEXT NOT NULL
                    )         
                """)
    
    @commands.command()
    async def resources(self, ctx):
        await ctx.message.delete() # Deletes the message from the server

        with sqlite3.connect('resources.db') as connection: # Opens the database
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM resources ORDER BY resource_title')

            rows = cursor.fetchall() # Fetch all the results

            if not rows:
                await ctx.send("No resources found.")
                return
            
            # Split resources into multiple embeds since Discord has a limit
            embeds = []
            current_embed = discord.Embed(title="Learning Resources", color=discord.Color.blue())

            for i, row in enumerate(rows):
                title, description, link = row

                if len(description) > 1000: # Limit description to avoid exceeding Discord's character limit
                    description = description[:997] + "..."

                current_embed.add_field(name=title, value=f"{description or '*No description*'}\n{link}", inline=False)

                if (i + 1) % 25 == 0 or (i + 1) == len(rows): # Checks if the current_embed reached Discord's limit
                    current_embed.set_footer(text=f"Requested by {ctx.author.display_name}")
                    current_embed.timestamp = datetime.now(ZoneInfo("America/New_York"))
                    embeds.append(current_embed)
                    if (i + 1) != len(rows):
                        current_embed = discord.Embed(title="Learning Resources (cont.)", color=discord.Color.blue())

            for embed in embeds:
                await ctx.send(embed=embed)

    @commands.command()
    async def add_resource(self, ctx):
        pass

    @commands.command()
    async def delete_resource(self, ctx):
        pass

async def setup(bot):
        """
        Required setup function for the Cog to be loaded.
        """
        await bot.add_cog(Resources(bot))