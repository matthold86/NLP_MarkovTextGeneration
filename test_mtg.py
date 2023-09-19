"""Markov Text Generator.

Patrick Wang, 2023

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

import nltk
import time

from mtg import finish_sentence


def test_generator():
    """Test Markov text generator."""
    corpus = nltk.word_tokenize(
        nltk.corpus.gutenberg.raw("austen-sense.txt").lower()
    )

    #words = finish_sentence(
    #    ["she", "was", "not"],
    #    3,
    #    corpus,
    #    randomize=False,
    #)
    words = finish_sentence(
        ["robot"],
        3,
        corpus,
        randomize=False,
    )
    #print(words)
    #assert words == [
    #    "she",
    #    "was",
    #    "not",
    #    "in",
    #    "the",
    #    "world",
    #    ".",
    #] or words == [
    #    "she",
    #    "was",
    #    "not",
    #    "in",
    #    "the",
    #    "world",
    #    ",",
    #    "and",
    #    "the",
    #    "two",
    #]

    #assert words == ['she', 'was', 'not', ',', ',', ',', ',', ',', ',', ',']
    assert words == ['robot', ',', 'and', 'the', 'two', 'miss', 'steeles', ',', 'as', 'she']


if __name__ == "__main__":
    start_time = time.time()
    test_generator()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Compilation time: {elapsed_time:.6f} seconds")