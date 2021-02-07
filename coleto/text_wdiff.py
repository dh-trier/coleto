#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Uses subprocess to call wdiff from the command line.
You need to have wdiff installed.
Based on the input texts split into sentences,
wdiff first aligns the text, identifying insertions and deletions. 
It then identifies each location of difference between two aligned sentences.
A sanity check is included to make sure wdiff has run correctly.
"""


# === Imports ===

import subprocess
import re
import sys
import time
from os.path import basename


# === Functions ===

def call_wdiff(sentences_file1, sentences_file2, wdiffed_file):
    """Executes the wdiff algorithm via a subprocess command."""
    command = "wdiff --avoid-wraps " + sentences_file1 + " "\
        + sentences_file2 + " > " + wdiffed_file
    # print(command)
    subprocess.Popen(command, shell=True)
    print("Looking good: wdiff results have been written to disk.")


def check_results(wdiffed_file): 
    """Performs sanity check: See how many differences have been found."""
    time.sleep(2)
    with open(wdiffed_file, "r", encoding="utf8") as infile: 
        wdiffed = infile.read()
        insertions = re.findall(r"\{\+", wdiffed)
        deletions = re.findall(r"\[\-", wdiffed)
        diffs = insertions + deletions
        # print(diffs)
        if len(diffs) > 5: 
            print("Looking good: at least " + str(len(diffs)//2) + " differences have been found.")
            print("The results have been written to the file " + basename(wdiffed_file) + ".")
        elif len(diffs) > 0: 
            print("Warning: only about " + str(len(diffs)//2) + " differences have been found.")
            print("The results have been written to the file " + basename(wdiffed_file) + ".")
        else: 
            sys.exit("ERROR! No differences have been found. Stopping.")       


# === Main ===

def main(params):
    """Uses subprocess to call wdiff from the command line.
    You need to have wdiff installed."""
    print("\n== coleto: running text_wdiff. ==")
    call_wdiff(
        params["sentences_file1"],
        params["sentences_file2"],
        params["wdiffed_file"])
    check_results(params["wdiffed_file"])
