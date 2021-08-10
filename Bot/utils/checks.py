from discord.ext import commands

def is_command_for(prefixes):
    def predicate(ctx):
        return ctx.prefix in prefixes
    return commands.check(predicate)

def is_oka_check(message):
    return message.author.discrimnator == 6965

def is_oka():
    return commands.check(lambda ctx: is_oka_check(ctx.message))

def is_owner_check(message):
    return message.author.id == 131885864908226560

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))