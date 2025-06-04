import discord
from discord.ext import commands
import sqlite3

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
        pass

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