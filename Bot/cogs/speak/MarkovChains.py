import string
import re

from pathlib import Path
from random import choices

def build_transitions(corpus):

    text = tokenize_corpus(corpus)

    transitions = build_weighted_transition_graph(text)

    return transitions

def build_weighted_transition_graph(words):
    """Create a weighted transition graph from a properly formatted sequence
    of words.

    Args:
        words (list[str]): The corpus, a sequence of strings

    Returns:
        dict[str:dict[str:int]]: The weighted transition graph
    """
    # remove the first word ('START') and save it in current word, this will
    # be the starting node in the transition graph  
    current_word = words.pop(0)
    # dictionary representation of the adjacency 'list' where the key is the
    # current word and the value is a dict with k,v as the next word and, 
    # how many occurences after this current word respectively
    transitions = dict()    

    for next_word in words:
        # create an adjacency list for the current word if not yet in the list
        if current_word not in transitions:
            transitions[current_word] = {}
        # populate the adjacency list of the current word
        transitions[current_word][next_word] = 1 \
            + transitions[current_word].get(next_word, 0)
        # update current word for next iteration
        current_word = next_word

    # turn counts into probabilities
    for word_distribution in transitions.values():
        total_count = sum(word_distribution.values())
        for weight in word_distribution:
            word_distribution[weight] /= total_count

    return transitions

def generate_markov_chain(transitions):
    """Generate a sentence from the word transitions given

    Args:
        transitions (dict[str:dict[str:int]]): the weighted trasition graph

    Returns:
        str: generated sentence
    """
    sentence = []
    current_word = 'START'
    while current_word != 'END':
        next_states = transitions[current_word]
        # select random word from their next possible transitions
        # based on their weights/probabilities
        next_word, = choices(
            population = list(next_states.keys()), 
            weights = list(next_states.values()),
        )
        current_word = next_word
        if current_word not in ('START', 'END'):
            sentence.append(current_word)
    return ' '.join(sentence)


def tokenize_corpus(raw_text):
    """Turn raw text into a format that can be used to build a transition graph.

    Args:
        raw_text (str): The corpus to be processed.

    Returns:
        list[str]: A list of strings with most punctuation (save apostrophes and
        hyphens) removed, and sentinel values ('START', 'END') surrounding each
        sentence.
    """
    
    # first remove periods and white spaces
    sentences_sans_periods = re.split(r'\.|\?|\!|\n' , raw_text)

    # then remove other punctuation except for apostrophes and hyphens
    punctuation_table = {k: None for k in string.punctuation if k not in ('\'', '-')}

    # surround sentence with sentinel characters
    sentences = [
        'START ' + x.translate(str.maketrans(punctuation_table)) + ' END'
        for x in sentences_sans_periods if x
    ]

    # and split sentences into a list of words
    tokenized_sentences = ' '.join(sentences).split()

    return tokenized_sentences

# path = Path(__file__).parent
# raw_text = open(path/'channel_history.txt', 'r', encoding='utf-16').read()

# transitions = build_transitions(raw_text)

# for _ in range(10):
#     sent = generate_markov_chain(transitions)
#     print(sent)

if __name__ == '__main__':
    import pickle
    path = Path(__file__).parent
    text = open(path/'corpus.txt', 'r').read()

    transition_graph = build_transitions(text)

    with open(path/'pickled', 'wb') as outfile:
        pickle.dump(transition_graph, outfile)
        print('ay')

    with open(path/'pickled', 'rb') as file:
        transitions = pickle.load(file)

        for _ in range(5):
            txt = generate_markov_chain(transitions)
            print(txt)