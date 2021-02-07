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
import yaml


# === Functions ===

def load_user_parameters():
    """Loads user-defined parameters from the config.yaml file."""
    with open(join("config.yaml"),
              "r", encoding="utf8") as infile:
        user_params = yaml.safe_load(infile)
    if len(user_params) > 3:
        print("Looking good: found the user-defined parameters.")
    else:
        print("Error! No user-defined parameters were found.")
    return user_params


def get_parameters(user_params):
    """User-defined parameters are added to main parameters.
    Further parameters are generated based on them.
    All parameters are made available to the other modules."""
    # Generated arameters: input files, sentence-split files.
    dataset_directory = join(user_params["working_directory"],
                             "data", user_params["dataset"])
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
        "working_directory": user_params["working_directory"],
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
        "smoothing": user_params["smoothing"],
        "language": user_params["language"],
        "levenshtein_cutoff": user_params["levenshtein_cutoff"],
        "documentation_mode": user_params["documentation_mode"]
         }

    return params


def main():
    """Loads and generates parameters for the current analysis."""
    print("\n== coleto: running parameters. ==")
    user_params = load_user_parameters()
    params = get_parameters(user_params)
    return params
