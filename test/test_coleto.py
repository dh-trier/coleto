#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Several tests for the coleto package. 
The tests are meant for developers. 
They should be run after cloning the package from Github.
Run the tests by calling the script from the cmd / terminal. 
When on /coleto, do: python3 -m pytest 
Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import pytest
from os.path import join
from coleto_pkg import text_preprocess
from coleto_pkg import text_analyze


# === Test functions ===

def test_always_passes():
    """This test simply tests whether the tests run at all."""
    assert True


def test_sentence_splitter(): 
    """This test checks the sentence splitting mechanism.
    Finds out whether a string containing several sentences
    is split into the correct number of sentences."""
    inputfile = "test_coleto.py"
    sampletext = "This is one sentence. This is another sentence. This is a third sentence. This is a fourth sentence. This is a fifth sentence. This is a sixth sentence."
    sentences, num_sentences = text_preprocess.sentence_splitter(inputfile, sampletext)
    assert num_sentences == 6, "Number of sentences in test textshould be 6."


def test_text_analyze_itemanalysis_1(): 
    """This test checks some of the functionality of the 'item analysis'.
    It checks whether the differences between a single given pair of items
    are recognized correctly by the function 
    and entered correctly into the dictionary holding the results."""
    item1 = "dark"
    item2 = "dark night"
    itemdata = {"itemid": "test",
                "version1": item1,
                "version2": item2,
                "lev-dist": "NA",
                "lev-dist-class": "NA",
                "lendiff-chars": "NA",
                "lendiff-words": "NA",
                "category": "NA",
                "main-type": "NA",
                "insertion": 0,
                "deletion": 0,
                "capitalization": 0,
                "whitespace": 0,
                "italics": 0,
                "punctuation": 0,
                "hyphenation": 0,
                "numbers": 0,
                "condensation": 0,
                "expansion": 0,
                "tbc": 0}
    itemdata = text_analyze.perform_itemanalysis(itemdata, item1, item2)
    print(itemdata)
    assert itemdata["version1"] == "dark"\
        and itemdata["version2"] == "dark night"\
        and itemdata["lendiff-words"] == 1\
        and itemdata["lendiff-chars"] == 6\
        and itemdata["lev-dist-class"] == "major"\
        and itemdata["expansion"] == 1\
        and itemdata["insertion"] == 0\
        and itemdata["tbc"] == 0\
        and itemdata["numbers"] == 0\
        and itemdata["main-type"] == "expansion"\
        , "comparing 'dark' and 'dark night'."



# === Calling the tests


if __name__ == '__main__':
    test_always_passes()
    test_sentence_splitter()
    test_text_analyze_itemanalysis_1()

