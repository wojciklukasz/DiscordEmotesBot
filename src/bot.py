import os
import discord
from dotenv import load_dotenv
from cogs.emotes import Emotes


load_dotenv()
bot = discord.Bot()
bot.load_extension('cogs.emotes')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------------------')


@bot.slash_command(name='add')
async def add(ctx, x: int, y: int):
    """Adds two numbers together"""
    await ctx.respond(x + y)

bot.run(os.getenv('TOKEN'))
