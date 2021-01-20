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

# === Functions ===


def get_parameters():
    """User-defined parameters are loaded.
    In addition, further parameters are generated.
    All parameters are made available to the other modules.
    """

    # User-defined parameter definitions go here
    working_directory = ""
    data_directory = join(working_directory, "data", "Doyle", "")

    # Additional parameters: input files, sentence-split files.
    output_directory = join(data_directory, "output", "")
    input_files = []
    for file in glob.glob(join(data_directory, "*.txt")):
        input_files.append(file)
    if len(input_files) == 2:
        print("Looking good: found two files to deal with.")
    else:
        print("Error! There should be exactly 2 files in the input folder.")
    input_file1 = input_files[0]
    input_file2 = input_files[1]
    sentences_file1 = join(
        output_directory,
        os.path.basename(input_file1).split(".")[0] + "_sentences.txt")
    sentences_file2 = join(
        output_directory,
        os.path.basename(input_file2).split(".")[0] + "_sentences.txt")

    # Additional parameters: further files
    wdiffed_file = join(output_directory, "wdiffed.txt")
    analysis_file = join(output_directory, "diff-analysis.tsv")
    levdists_file = join(output_directory, "lev-dists-by-line.tsv")
    progressionplot = join(
        output_directory,
        "edits-over-textual-progression.svg")
    statistics_file = join(output_directory, "statistics.tsv")
    pivotstatistics_file = join(
        output_directory,
        "martian_pivot-statistics.csv")
    typesplot1 = join(output_directory, "typesplot1.svg")
    typesplot2 = join(output_directory, "typesplot2.svg")

    # Output folder is created
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Parameter definitions are packaged up
    params = {
        "working_directory": working_directory,
        "data_directory": data_directory,
        "output_directory": output_directory,
        "input_file1": input_file1,
        "input_file2": input_file2,
        "sentences_file1": sentences_file1,
        "sentences_file2": sentences_file2,
        "wdiffed_file": wdiffed_file,
        "analysis_file": analysis_file,
        "levdists_file": levdists_file,
        "progressionplot": progressionplot,
        "statistics_file": statistics_file,
        "pivotstatistics_file": pivotstatistics_file,
        "typesplot1": typesplot1,
        "typesplot2": typesplot2,
         }

    return params


def main():
    print("== coleto: running parameters. ==")
    params = get_parameters()
    return params
