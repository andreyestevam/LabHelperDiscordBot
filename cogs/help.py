from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="📘 Bot Commands",
            description="Here are the available commands:",
            color=discord.Color.blue()
        )

        embed.add_field(name="!resources", value="List all available resources.", inline=False)
        embed.add_field(name="!add_resource", value="Add a new resource interactively.", inline=False)
        embed.add_field(name="!delete_resource", value="Delete a resource by its title.", inline=False)
        embed.add_field(name="!schedule", value="Schedule a calendar event via DM and email the invite to participants.", inline=False)
        embed.add_field(name="!help or !commands", value="Show this help message.", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Help(bot))