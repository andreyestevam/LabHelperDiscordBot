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
            
            embed = discord.Embed(title="Learning Resources", color=discord.Color.blue())

            rows_msg = ""
            for row in rows:
                title, description, link = row
                embed.add_field(name=title, value=f"{description or '*No description*'}\n{link}", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            embed.timestamp = datetime.now(ZoneInfo("America/New_York"))
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