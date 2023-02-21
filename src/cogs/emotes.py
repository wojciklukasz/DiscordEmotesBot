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
        if is_emote:
            await ctx.respond(emote)
        else:
            await ctx.respond('This is not a valid emote!')


def setup(bot):
    print('Loading Emotes cog...', end=' ')
    bot.add_cog(Emotes(bot))
    print('Done!')
