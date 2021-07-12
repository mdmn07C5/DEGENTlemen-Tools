from discord.ext import commands

def is_command_for(prefixes):
    def predicate(ctx):
        return ctx.prefix in prefixes
    return commands.check(predicate)


def check_prefix(allowed_prefixes):
    return ctx.prefix in allowed_prefixes

def is_oka(discriminator, banned_people):
    return discriminator in banned_people

