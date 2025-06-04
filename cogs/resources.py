import discord
from discord.ext import commands
import sqlite3

connection = sqlite3.connect('resources.db')
cursor = connection.cursor()

cursor.execute("""
                CREATE TABLE resources (
                    resource_title TEXT NOT NULL,
                    description TEXT,
                    link TEXT NOT NULL
                )         
            """)

connection.close()