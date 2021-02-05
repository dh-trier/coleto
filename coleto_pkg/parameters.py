#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.


"""Script to define and generate parameters, such as paths and filenames.
The parameters are then used by the various coleto modules.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import os
from os.path import join
import glob
import sys


# ===========================================================
# USER-DEFINED PARAMETERS
working_directory = join("..", "coleto-data", "")
dataset_directory = join(working_directory, "Loaisel")
smoothing = True
# ============================================================


# === Functions ===


def get_parameters():
    """User-defined parameters are loaded.
    Further parameters are generated based on them.
    All parameters are made available to the other modules.
    """

    # Generated arameters: input files, sentence-split files.
    input_directory = join(dataset_directory, "input", "")
    output_directory = join(dataset_directory, "output", "")
    # print("This is the input directory: ", input_directory)
    input_files = []
    for file in glob.glob(join(input_directory, "*.txt")):
        input_files.append(file)
    # print(len(input_files))
    # print(input_files)
    if len(input_files) == 2:
        print("Looking good: found two files to deal with.")
    else:
        sys.exit("Error! There should be exactly 2 files in the input folder.")
    input_file1 = input_files[0]
    input_file2 = input_files[1]
    sentences_file1 = join(
        output_directory,
        os.path.basename(input_file1).split(".")[0] + "_split.txt")
    sentences_file2 = join(
        output_directory,
        os.path.basename(input_file2).split(".")[0] + "_split.txt")

    # Output folder is created
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Parameter definitions are packaged up
    params = {
        "working_directory": working_directory,
        "dataset_directory": dataset_directory,
        "input_directory": input_directory,
        "output_directory": output_directory,
        "input_file1": input_file1,
        "input_file2": input_file2,
        "sentences_file1": sentences_file1,
        "sentences_file2": sentences_file2,
        "wdiffed_file": join(output_directory, "wdiffed.txt"),
        "analysis_file": join(output_directory, "diff-analysis.tsv"),
        "analysissummary_file": join(output_directory, "diff-summary.tsv"),
        "levdists_file": join(output_directory, "diff-levenshtein-data.tsv"),
        "progressionplot": join(output_directory,
                                "edits-over-textual-progression.svg"),
        "simplestatistics_file": join(output_directory,
                                      "diff-simple-statistics.tsv"),
        "complexstatistics_file": join(output_directory,
                                       "diff-complex-statistics.tsv"),
        "simpletypesplot": join(output_directory, "simple-types-plot.svg"),
        "complextypesplot": join(output_directory, "complex-types-plot.svg"),
        "documentation_name": join(output_directory, "documentation"),
        "smoothing": smoothing,
         }

    return params


def main():
    print("\n== coleto: running parameters. ==")
    params = get_parameters()
    return params
