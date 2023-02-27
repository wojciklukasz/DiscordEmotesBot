import os
import discord
from database.model import connect


db = connect()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)
bot.load_extension('cogs.emotes')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------------------')

bot.run(os.getenv('TOKEN'))
