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


# === Functions ===


def read_text(file):
    """Reads the text from a plain text file."""
    with open(file, "r") as infile:
        text = infile.read()
        text = re.sub("\n", " ", text)
        text = re.sub("  ", " ", text)
        return text


def sentence_splitter(text):
    """Splits a text string into individual sentences."""
    sentences = nltk.sent_tokenize(text)
    sentences = "\n".join(sentences)
    if sentences:
        print("Looking good: sentences found.")
    else:
        print("Error! No sentences were found.")
    return sentences


def save_sentences(sentences, filename):
    """Saves the sentences to a file, one sentence per line."""
    with open(filename, "w") as outfile:
        outfile.write(sentences)


# === Main function ===

def main(params):
    print("== coleto: running preprocess. ==")
    text1 = read_text(params["input_file1"])
    sentences1 = sentence_splitter(text1)
    save_sentences(sentences1, params["sentences_file1"])
    text2 = read_text(params["input_file2"])
    sentences2 = sentence_splitter(text2)
    save_sentences(sentences2, params["sentences_file2"])
