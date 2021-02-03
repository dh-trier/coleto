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


# === Test functions ===

def test_always_passes():
    """This test simply tests whether the tests run at all."""
    assert True


def test_sentence_splitter(): 
   inputfile = "test_coleto.py"
   sampletext = "This is one sentence. This is another sentence. This is a third sentence. This is a fourth sentence. This is a fifth sentence. This is a sixth sentence."
   sentences, num_sentences = text_preprocess.sentence_splitter(inputfile, sampletext)
   assert num_sentences == 6, "Number of sentences in test textshould be 6."


if __name__ == '__main__':
    test_always_passes()
    test_sentence_splitter()

