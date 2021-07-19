from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
from discord.ext import commands
import requests, random, pprint, secrets, discord
import checks

pp = pprint.PrettyPrinter(indent=4)

class Frog(commands.Cog):

    def __init__(self, bot):
        path = Path(__file__).parent
        self.apu_links = open(path/'apu_links.txt', 'r').read().splitlines()
    
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
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



def get_random_apu():
    request = requests.get('https://www.memeatlas.com/pepe-memes.html')
    soup = BeautifulSoup(request.content, 'html.parser')
    result_set = soup.find(id='list')

    results = []
    for result in result_set.contents:
        if (res := result.find('a')) != -1:
            results.append(res['href'])
    
    random.seed(None)
    random_apu = f'https://www.memeatlas.com/{random.choice(results)}'
    # return random_apu
    return requests.get(random_apu)

# def get_random_apu_kym():
#     path = Path(__file__).parent
#     apu_links = open(path/'apu_links.txt', 'r').read().splitlines()
#     random.seed(None)
#     random_apu = random.choice(apu_links)

#     return requests.get(random_apu)