import discord
from src.database.model import connect


db = connect()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)
bot.load_extension('src.cogs.emotes')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------------------------')


def start(token):
    bot.run(token)
