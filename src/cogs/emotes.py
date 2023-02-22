import re
import discord
from discord.ext import commands
from database.model import increase_count, get_count_emote


class Emotes(commands.Cog):
    """Cog for handling all emotes related commands"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def usage(self, ctx, emote):
        """Returns how many times a given emote has been used"""

        is_emote = True if len(re.findall(r'<:\w*:\d*>', emote)) > 0 else False
        if not is_emote:
            embed = discord.Embed(
                title='Error!',
                description='**This is not a valid emote!**',
                color=discord.Colour.red()
            )

            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(
            title=f'Usage of {emote}',
            color=discord.Colour.blurple(),
        )

        count = get_count_emote(emote, ctx.guild)
        if count == 0:
            embed.add_field(name='This emote has not been used yet!', value='*sad emote noises*')
        else:
            embed.add_field(name='As an emote:', value=count)
        embed.set_thumbnail(url=f'https://cdn.discordapp.com/emojis/{emote.split(":")[2][:-1]}.png')

        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        emotes = re.findall(r'<:\w*:\d*>', message.content)

        for e in emotes:
            increase_count(e, message.guild)


def setup(bot):
    print('Loading Emotes cog...', end=' ')
    bot.add_cog(Emotes(bot))
    print('Done!')
