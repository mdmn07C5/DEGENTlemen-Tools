import pickle
from random import randint
from io import StringIO

from pathlib import Path
from typing import final

from discord.ext import commands

from .MarkovChains import generate_markov_chain, build_transitions


class Speech(commands.Cog):

    def __init__(self, bot):
        self.filepath = Path(__file__).parent
        self.bot = bot
        corpus = open(self.filepath/'corpus.txt', 'r').read()
        self.speech_transitions = build_transitions(corpus)
        self._save_speech_patterns()                

    @commands.Cog.listener()
    async def on_message(self, message):
        """Even that listens to mentions of this bot, will reply with a 
        randomly generated text. 

        Args:
            message (discord.Message): The message the bot was mentioned in,
            the only purpose of it is to get the channel it was posted in so
            the bot can reply in the same channel. 
        """
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            sentence_count = randint(0, 5)
            reply = generate_markov_chain(self.speech_transitions)
            for _ in range(sentence_count):
                reply += '\n' + generate_markov_chain(self.speech_transitions)
            await message.channel.send(reply)

    # ======================================================================= #
    # The methods below are to be used if you want chat history to be used as #
    # the corpus for the markov chain sentence generator, which may not be a  #
    # good idea because of the existence of special characters, links, gifs,  #
    # etc. in the messages.                                                   #
    # ======================================================================= #
    def _save_speech_patterns(self):
        """Serialize the transition graph
        """
        with open(self.filepath/'transition_graph', 'wb') as output_file:
            pickle.dump(self.speech_transitions, output_file)
    
    def _load_speech_patterns(self):
        """De-serialize transition graph and load into speech_transitions
        """
        with open(self.filepath/'transition_graph', 'rb') as input_file:
            self.speech_transitions = pickle.load(input_file)

    @commands.command(hidden=True, name='lern2spek')
    async def save_speech_pattern(self, ctx, message_limit):
        """Build a transition graph from the message history of the channel 
        that this command was called in, and serializes it.

        Args:
            ctx (discord.ext.commands.Context): The context which this command
            was called (the channel, the user, the prefix, etc.). 
            message_limit (str): How many messages in the history to go back
        """
        channel = ctx.channel
        msgs = StringIO('')
        async for msg in channel.history(limit=int(message_limit)):
            msgs.write(msg.content + '\n')
        
        self.speech_transitions = build_transitions(msgs.getvalue())

        self._save_speech_patterns()

        await ctx.send(f'\N{OK HAND SIGN} am big brain now {message_limit}')

    @commands.command(hidden=True, name='wrinklebrain')
    async def load_speech_patterns(self, ctx):
        """De-serialize a transition graph (if different from the one created
        during instantiation) and load it into speech transitions.

        Args:
            ctx (discord.ext.commands.Context): The context which this command
            was called (the channel, the user, the prefix, etc.).
        """
        self._load_speech_patterns()
        await ctx.send('\N{OK HAND SIGN} remberd happy day')


def setup(bot):
    bot.add_cog(Speech(bot))
