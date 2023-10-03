import re
import discord
from discord.ext import commands
from src.database.model import increase_count_emote, increase_count_reaction, get_count_emote, get_count_reaction, \
    decrease_count_emote, decrease_count_reaction


emote_regex = r'<:\w*:\d*>'
animated_emote_regex = r'<a:\w*:\d*>'


class Emotes(commands.Cog):
    """Cog for handling all emotes related commands"""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def usage(self, ctx, emote):
        """Returns how many times a given emote has been used"""

        is_emote = True if len(re.findall(emote_regex, emote)) > 0 else False
        if not is_emote:
            embed = discord.Embed(
                title='Error!',
                description='**This is not a valid emote!**',
                color=discord.Colour.red()
            )

            await ctx.respond(embed=embed)
            return

        print(f'Getting uses of {emote} in server {ctx.guild} ID: {ctx.guild.id}')

        embed = discord.Embed(
            title=f'Usage of {emote}',
            color=discord.Colour.blurple(),
        )

        count_emote = get_count_emote(emote, ctx.guild)
        count_reaction = get_count_reaction(emote, ctx.guild)

        if count_emote == 0 and count_reaction == 0:
            embed.add_field(name='This emote has not been used yet!', value='*sad emote noises*')
        else:
            embed.add_field(name='As an emote:', value=count_emote)
            embed.add_field(name='As a reaction:', value=count_reaction)

        embed.set_thumbnail(url=f'https://cdn.discordapp.com/emojis/{emote.split(":")[2][:-1]}.png')

        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        emotes = re.findall(emote_regex, message.content)
        animated_emotes = re.findall(animated_emote_regex, message.content)

        for e in emotes:
            increase_count_emote(e, message.guild)
        for e in animated_emotes:
            increase_count_emote(e, message.guild)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.member == self.bot.user:
            return

        increase_count_reaction(str(reaction.emoji), reaction.member.guild)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        emotes = re.findall(emote_regex, message.content)
        animated_emotes = re.findall(animated_emote_regex, message.content)

        for e in emotes:
            decrease_count_emote(e, message.guild)
        for e in animated_emotes:
            decrease_count_emote(e, message.guild)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        guild = await self.bot.fetch_guild(reaction.guild_id)
        decrease_count_reaction(str(reaction.emoji), guild)


def setup(bot):
    print('Loading Emotes cog...', end=' ')
    bot.add_cog(Emotes(bot))
    print('Done!')
