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
                    guild_id INTEGER NOT NULL,
                    resource_title TEXT NOT NULL,
                    description TEXT,
                    link TEXT NOT NULL
                )
            """)
    
    @commands.command()
    async def resources(self, ctx):
        guild_id = ctx.guild.id
        
        with sqlite3.connect('resources.db') as connection: # Opens the database
            cursor = connection.cursor()
            cursor.execute('SELECT resource_title, description, link FROM resources WHERE guild_id = ? ORDER BY resource_title', (guild_id,))

            rows = cursor.fetchall() # Fetch all the results

            if not rows:
                await ctx.send("No resources found.")
                return
            
            # Split resources into multiple embeds since Discord has a limit
            embeds = []
            current_embed = discord.Embed(title="Useful Resources", color=discord.Color.blue())

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
        guild_id = ctx.guild.id

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            await ctx.send("Please enter the **title** of the resource:")
            title_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            title = title_msg.content

            await ctx.send("Please enter the **description** of the resource (or type 'none'):")
            desc_msg = await self.bot.wait_for("message", timeout=120.0, check=check)
            description = desc_msg.content
            if description.lower() == 'none':
                description = None

            await ctx.send("Please enter the **link** to the resource:")
            link_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            link = link_msg.content

            with sqlite3.connect('resources.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO resources (guild_id, resource_title, description, link) VALUES (?, ?, ?, ?)",
                               (guild_id, title, description, link))
                connection.commit()

            await ctx.send(f"✅ Resource '{title}' added successfully!", delete_after=10)

        except Exception as e:
            await ctx.send(f"❌ Failed to add resource: {str(e)}", delete_after=10)

    @commands.command()
    async def delete_resource(self, ctx):
        guild_id = ctx.guild.id

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            await ctx.send("Please enter the **title** of the resource you want to delete:")
            title_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            title_to_delete = title_msg.content

            with sqlite3.connect('resources.db') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM resources WHERE guild_id = ? AND resource_title = ?", (guild_id, title_to_delete))
                resource = cursor.fetchone()

                if resource is None:
                    await ctx.send(f"❌ Resource titled '{title_to_delete}' not found.", delete_after=10)
                    return

                cursor.execute("DELETE FROM resources WHERE guild_id = ? AND resource_title = ?", (guild_id, title_to_delete))
                connection.commit()

            await ctx.send(f"✅ Resource '{title_to_delete}' deleted successfully.", delete_after=10)

        except Exception as e:
            await ctx.send(f"❌ Failed to delete resource: {str(e)}", delete_after=10)

async def setup(bot):
        """
        Required setup function for the Cog to be loaded.
        """
        await bot.add_cog(Resources(bot))