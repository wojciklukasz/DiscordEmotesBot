import re
import discord
from discord.ext import commands
from discord.ext.commands.errors import EmojiNotFound


class Emotes(commands.Cog):
    """Cog for handling all emotes related commands"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def usage(self, ctx, emote):
        """Returns how many times a given emote has been used"""

        is_emote = True if len(re.findall(r'<:\w*:\d*>', emote)) > 0 else False
        if not is_emote:
            await ctx.respond('This is not a valid emote!')
            return

        embed = discord.Embed(
            title=f'Usage of {emote}',
            color=discord.Colour.blurple(),
        )
        embed.add_field(name='As an emote:', value='2')
        embed.set_thumbnail(url=f'https://cdn.discordapp.com/emojis/{emote.split(":")[2][:-1]}.png')

        await ctx.respond(embed=embed)


def setup(bot):
    print('Loading Emotes cog...', end=' ')
    bot.add_cog(Emotes(bot))
    print('Done!')
