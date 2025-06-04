import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect('resources.db')



connection.close()