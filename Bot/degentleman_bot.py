# import dotenv
from dotenv import dotenv_values
from discord.ext import commands
from pathlib import Path
from io import BytesIO
import random, discord, secrets
import checks, frog, admin
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = dotenv_values('.env')['TOKEN']
OKA = dotenv_values('.env')['OKA_DISCRIMINATOR']
PREFIXES = {
    'frog': '~',
    'ai_rpg': '!',
    'everything_else': '.'
}

bot = commands.Bot(command_prefix=PREFIXES.values(), case_insensitive=True)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(discord.Colour.purple())
    embed.set_author(name='Help: list of available commands')
    embed.add_field(
        name='.qrd <name>', 
        value='Gives you a quick run down on <person>',
        inline=True
    )
    embed.add_field(
        name='~',
        value='frog commands'
    )
    embed.add_field(
        name='!',
        value='AIDs'
    )

    await ctx.send(embed=embed)

# miscellaneous shit
@bot.command()
@checks.is_command_for((PREFIXES['frog'], PREFIXES['ai_rpg']))
async def checkem(ctx):
    await ctx.send(f'{ctx.prefix} is an allowed prefix')


@bot.command()
@checks.is_command_for((PREFIXES['everything_else']))
async def qrd(ctx, msg):
    if is_oka(ctx.author.discriminator):
        await ctx.send(f"bro that's cringe, you're cringe.")
    else:
        path = Path(__file__).parent
        responses = open(path/'oka.txt', 'r').read().splitlines()
        random.seed(a=None)
        response = random.choice(responses)
        await ctx.send(f'Quick Run Down on {msg}: {msg} {response}')

def is_oka(discriminator):
    return discriminator == OKA



# @bot.command()
# @checks.is_command_for((PREFIXES['frog']))
# @commands.cooldown(1, 30, commands.BucketType.default)
# async def apu(ctx):
#     response = frog.get_random_apu()
#     buffer = BytesIO(response.content)
#     extension = response.headers['Content-Type'].split('/')[-1]
#     random_token = secrets.token_urlsafe(16)
#     filename = '.'.join([random_token, extension])
#     img_file = discord.File(filename=filename, fp=buffer)

#     await ctx.send(content='', file=img_file,)

@bot.command()
@checks.is_owner()
async def me(ctx):
    await ctx.send(f'You: {ctx.message.author.id}')



bot.add_cog(admin.Admin(bot))
bot.add_cog(frog.Frog(bot))
bot.run(TOKEN)