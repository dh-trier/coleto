#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Calculates edit intensity over textual progression.
Focuses on cumulated Levenshtein distances. 
Reports them per category of edit and per sentence.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
from os.path import join
from os.path import basename


# === Functions ===


def read_datafile(analysisfile):
    """Reads the output of 'analyze'.
    Selects the relevant columns and turns them into a DataFrame.
    Returns the DataFrame."""
    with open(analysisfile, "r") as infile:
        data = pd.read_csv(
            infile,
            sep="\t",
            usecols=["itemid", "category", "lev-dist"])
    # print(data.head(10))
    return data


def split_itemid(data):
    """The column "itemid" contains the line number
    and the edit number per line.
    This function splits them apart.
    It then creates two new columns from this information.
    Returns the DataFrame."""
    split = data["itemid"].str.split("-", n=1, expand=True)
    data["line"] = split[0]
    data["edit"] = split[1]
    data.drop(columns=["itemid"], inplace=True)
    # print(data.head(10))
    return data


def separate_categories(data):
    """
    Separate the rows concerning "script-identifiable edits" from those
    concerning "other edits".
    Also, in each categry, and for each line, calculate the sum of
    levenshtein distances across all edits for that line.
    Return two separate DataFrames.
    """
    # Line 6 should have an entry in both other and script.
    data = data.groupby(["category", "line"], axis=0).sum()
    other = data.loc["other", :].reset_index()\
        .astype(int).sort_values(by=["line"])
    script = data.loc["script-identifiable", :]\
        .reset_index().astype(int).sort_values(by=["line"])
    # print(script.head(), other.head())
    return other, script


def get_numsentences(analysissummaryfile):
    """
    Retrieves the number of sentences.
    Used primarily in the documentation file so far.
    """
    with open(analysissummaryfile, "r", encoding="utf8") as infile: 
        summary = pd.read_csv(infile, sep="\t", index_col=0)
        numsentences = summary["numlines"].values[0]
        return numsentences


def supply_emptylines(numsentences):
    """
    Create a dummy DataFrame in which every line in the text has a row.
    This is simply to make a left merge possible to obtain a DataFrame
    that also has rows for lines where no edit took place.
    Returns a DataFrame.
    """
    rows = range(1, numsentences)  # 11870 – 11479
    levs = [0] * numsentences  # 11870 – 11479
    empty = pd.DataFrame(
        list(zip(rows, levs)),
        columns=["line", "lev-dist"]).astype(int)
    # print(empty.head())
    return empty


def merge_frames(withdata, empty):
    """Merge the dummy DataFrame with the DataFrames containing data.
    Creates a DataFrame with one row per line in the novel.
    Done once for other, once for script.
    Returns a DataFrame."""

    merged = empty.merge(withdata, how="left", on="line").fillna(0)
    merged["lev-dist"] = merged["lev-dist_x"] + merged["lev-dist_y"]
    merged.drop(["lev-dist_x", "lev-dist_y"], axis=1, inplace=True)
    # print(merged.shape)
    # print(merged.head(10))
    return merged


def merge_again(other, script):
    """
    Merge the two DataFrames for other and script together again,
    but keeping distinct rows for the cumulated levenshtein distances
    for each category (other and script).
    Returns DataFrame.
    """
    data = other.merge(script, how="left", on="line")
    data.rename(columns={"lev-dist_x": "other", "lev-dist_y": "script"},
                inplace=True)
    # print(data.head())
    return data


def save_data(data, filename):
    """
    Saves the levenshtein distance data per category to a TSV file.
    """
    with open(filename, "w", encoding="utf8") as outfile:
        data.to_csv(outfile, sep="\t")
    print("Looking good: The Levenshtein distance data has been saved.")
    print("The file is called " + basename(filename) + ".")


def main(params):
    """Calculates edit intensity over textual progression.
    Focuses on cumulated Levenshtein distances. 
    Reports them per category of edit and per sentence."""
    print("\n== coleto: running stats_progression.")
    data = read_datafile(params["analysis_file"])
    data = split_itemid(data)
    other, script = separate_categories(data)
    numsentences = get_numsentences(params["analysissummary_file"])
    empty = supply_emptylines(numsentences)
    other = merge_frames(other, empty)
    script = merge_frames(script, empty)
    data = merge_again(other, script)
    save_data(data, params["levdists_file"])

