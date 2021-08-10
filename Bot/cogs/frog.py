import random
import secrets
from io import BytesIO

import requests
import discord
from bs4 import BeautifulSoup
from pathlib import Path
from discord.ext import commands

from utils import checks


class Frog(commands.Cog):

    def __init__(self, bot):
        path = Path(__file__).parent
        self.apu_links = open(path/'apu_links.txt', 'r').read().splitlines()
        random.shuffle(self.apu_links)
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @checks.is_command_for(('~'))
    async def apu(self, ctx):
        random_apu = random.choice(self.apu_links)
        response = requests.get(random_apu)
        buffer = BytesIO(response.content)
        file_extension = response.headers['Content-Type'].split('/')[-1]
        random_token = secrets.token_urlsafe(16)
        filename = '.'.join([random_token, file_extension])
        img_file = discord.File(filename=filename, fp=buffer)
        await ctx.send(content='', file=img_file,)

    @commands.command()
    async def pepo(self, ctx):
        await ctx.send('henlo fren')

    @commands.command()
    async def peepo(self, ctx):
        await ctx.send('widePeepoHappy')

# def get_random_apu_kym():
#     path = Path(__file__).parent
#     apu_links = open(path/'apu_links.txt', 'r').read().splitlines()
#     random.seed(None)
#     random_apu = random.choice(apu_links)

#     return requests.get(random_apu)
    
def setup(bot):
    bot.add_cog(Frog(bot))