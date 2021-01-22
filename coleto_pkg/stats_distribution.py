#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2019.

"""
Script to create some statistics from the diff analysis data.
These statistics focus on the edit types. 

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
import numpy as np
from os.path import join
from os.path import basename


# === Functions ===

def read_datafile(tsvfile):
    """Read a TSV file with data."""
    with open(tsvfile, "r") as infile:
        data = pd.read_csv(infile, sep="\t")
        # print(data.head(10))
        return data


def lev_stats(levdata, statistics):
    levdata.drop("Unnamed: 0", axis=1, inplace=True)
    statistics["lev_allscript"] = np.sum(levdata["script"])
    statistics["lev_allother"] = np.sum(levdata["other"])
    return statistics


def ana_stats(anadata, statistics):
    # print(anadata.columns)
    # FIXIT: Could be written more succinctly.
    statistics["condensation"] = sum(anadata["condensation"])
    statistics["expansion"] = sum(anadata["expansion"])
    statistics["deletion"] = sum(anadata["deletion"])
    statistics["to be confirmed"] = sum(anadata["tbc"])
    statistics["insertion"] = sum(anadata["insertion"])
    statistics["capitalization"] = sum(anadata["capitalization"])
    statistics["whitespace"] = sum(anadata["whitespace"])
    statistics["italics"] = sum(anadata["italics"])
    statistics["punctuation"] = sum(anadata["punctuation"])
    statistics["hyphenation"] = sum(anadata["hyphenation"])
    statistics["numbers"] = sum(anadata["numbers"])
    statistics["script-identifiable"] = statistics["capitalization"]\
        + statistics["whitespace"]\
        + statistics["italics"]\
        + statistics["punctuation"]\
        + statistics["hyphenation"]\
        + statistics["numbers"]
    statistics["other edits"] = statistics["condensation"]\
        + statistics["expansion"]\
        + statistics["deletion"]\
        + statistics["insertion"]\
        + statistics["to be confirmed"]
    statistics = pd.DataFrame.from_dict(
        statistics,
        orient="index",
        columns=["values"])
    return statistics


def save_data(statistics, statisticsfile):
    """Saves the statistics data to a TSV file."""
    with open(statisticsfile, "w", encoding="utf8") as outfile:
        statistics.to_csv(outfile, sep="\t")
    print("Looking good: the statistics data has been saved to disk.")
    print("The file is called " + basename(statisticsfile) + ".")


def save_pivotdata(anadata, pivotstatisticsfile):
    """Saves a selection of data in pivoted format to a TSV file."""
    pivotdata = anadata.pivot_table(
        index="main-type",
        columns="lev-dist-class",
        aggfunc='size',
        fill_value=0)
    pivotdata["sums"] = pivotdata.sum(axis=1)
    #print(pivotdata)
    with open(pivotstatisticsfile, "w", encoding="utf8") as outfile:
        pivotdata.to_csv(outfile, sep="\t")


# === Main function ===


def main(params):
    print("\n== coleto: running stats_distribution. ==")
    statistics = {}
    levdata = read_datafile(params["levdists_file"])
    statistics = lev_stats(levdata, statistics)
    anadata = read_datafile(params["analysis_file"])
    statistics = ana_stats(anadata, statistics)
    save_data(statistics, params["simplestatistics_file"])
    save_pivotdata(anadata, params["complexstatistics_file"])
