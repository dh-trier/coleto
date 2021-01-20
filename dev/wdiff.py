#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Uses subprocess to call wdiff from the command line.
You need to have wdiff installed.
"""


# === Imports ===

import subprocess


# === Functions ===

def call_wdiff(sentences_file1, sentences_file2, wdiffed_file):
    command = "wdiff --avoid-wraps " + sentences_file1 + " "\
        + sentences_file2 + " > " + wdiffed_file
    # print(command)
    subprocess.Popen(command, shell=True)
    print("Looking good. Please check the wdiff results file on disk.")


# === Main ===

def main(params):
    print("== coleto: running wdiff. ==")
    call_wdiff(
        params["sentences_file1"],
        params["sentences_file2"],
        params["wdiffed_file"])
