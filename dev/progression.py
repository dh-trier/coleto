#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: textual_progression.py
# Author: Christof Schöch, 2016-2019.

"""
Script to visualize edits over textual progression.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
import pygal
from pygal import Config
from scipy.signal import savgol_filter as sf
from os.path import join


# === Functions for data preparation ===


def read_datafile(analysisfile):
    """Reads the output of "analyse_wdiff.py"
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


def supply_emptylines():
    """
    Create a dummy DataFrame in which every line in the text has a row.
    This is simply to make a left merge possible to obtain a DataFrame
    that also has rows for lines where no edit took place.
    Returns a DataFrame.
    """
    # FIXIT: This number should be derived from the data.
    rows = range(1, 7)  # 11870 – 11479
    levs = [0] * 7  # 11870 – 11479
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
    return data


def save_data(data, filename):
    """
    Saves the levenshtein distance data per category to a CSV file.
    """
    with open(filename, "w", encoding="utf8") as outfile:
        data.to_csv(outfile, sep="\t")


def prepare_data(analysisfile, levdistsfile):
    """
    Coordinate the process of preparing the data for visualization.
    """
    # print("\n-- prepare_data...")
    data = read_datafile(analysisfile)
    data = split_itemid(data)
    other, script = separate_categories(data)
    empty = supply_emptylines()
    other = merge_frames(other, empty)
    script = merge_frames(script, empty)
    data = merge_again(other, script)
    save_data(data, levdistsfile)
    # print(data.head())
    return data


# === Functions for data visualization ===


def define_config():
    config = Config()
    config.show_legend = False
    config.human_readable = True
    config.fill = False
    config.height = 1000
    config.width = 2000
    config.x_label_rotation = 300
    config.show_legend = False
    config.x_labels_major_every = 200  # 200
    config.show_minor_x_labels = False
    config.show_dots = False
    config.fill = True
    config.logarithmic = False
    return config


def apply_smoothing(data):
    """
    Apply Savitzky-Golay smoothing to the data for better readability.
    See: https://docs.scipy.org/doc/scipy-0.18.1/reference\
    /generated/scipy.signal.savgol_filter.html
    """
    # smoothed = data  # with this, no smoothing is applied.
    smoothed = sf(data, window_length=3, polyorder=1, mode="mirror")
    smoothed = sf(data, window_length=35, polyorder=1, mode="mirror")
    return smoothed


def using_pygal(data, progressionplot):
    # print("-- using_pygal...")
    lines = list(data.loc[:, "line"])
    script = apply_smoothing(data["script"])
    other = apply_smoothing(data["other"])
    config = define_config()
    plot = pygal.StackedBar(config, range=(0, 60))  # 60
    plot.title = "Edit intensity across the text"
    plot.y_title = "Levenshtein distance (smoothed)"
    plot.x_title = "Lines in the text"
    plot.x_labels = lines
    plot.add("Script-Identifiable Edits", script)
    plot.add("Other Edits", other)
    plot.render_to_file(progressionplot)


# === Coordinating function ===

def main(params):
    print("== coleto: running progression. ==")
    data = prepare_data(params["analysis_file"], params["levdists_file"])
    using_pygal(data, params["progressionplot"])
