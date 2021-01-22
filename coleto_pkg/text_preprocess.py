#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Splits a plain text file with newlines for paragraph endings
into a sequence of sentences, one sentence per line.
This is the first step in the alignement process.

Variant plain text files need to be placed in a folder.
This folder is referenced by the parameter "input_folder".

Resulting plain text files are written to an output folder.
This folder is referenced by the parameter "input_folder".
"""


# === Imports ===

import nltk
import re
import sys
import os
from os.path import basename



# === Functions ===


def read_text(file):
    """Reads the text from a plain text file."""
    # print(os.path.basename(file))
    with open(file, "r") as infile:
        text = infile.read()
        # print(text[0:100])
        text = re.sub("\n", " ", text)
        text = re.sub("  ", " ", text)
        return text


def sentence_splitter(input_file, text):
    """Splits a text string into individual sentences."""
    sentences = nltk.sent_tokenize(text)
    if len(sentences) > 5:
        print("Looking good: " + str(os.path.basename(input_file)) + " has " 
        + str(len(sentences)) + " sentences.")
    elif len(sentences) > 2: 
        print("Warning: are there really only " + str(len(sentences)) 
        + " sentences in " + str(os.path.basename(input_file)) + "?")
    else:
        sys.exit("ERROR! Only " + str(len(sentences)) 
        + " sentences were found.\nIs there text in your input files?")
    sentences = "\n".join(sentences)
    return sentences


def save_sentences(sentences, filename):
    """Saves the sentences to a file, one sentence per line."""
    with open(filename, "w") as outfile:
        outfile.write(sentences)
    print("The text split into sentences has been saved to " 
    + basename(filename) + ".")        


# === Main function ===

def main(params):
    print("\n== coleto: running text_preprocess. ==")
    text1 = read_text(params["input_file1"])
    sentences1 = sentence_splitter(params["input_file1"], text1)
    save_sentences(sentences1, params["sentences_file1"])
    text2 = read_text(params["input_file2"])
    sentences2 = sentence_splitter(params["input_file2"], text2)
    save_sentences(sentences2, params["sentences_file2"])
