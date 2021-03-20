#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Script to visualize some basic collation statistics.
The key information visualized is frequency of edit types.
Uses the pygal library to create several barcharts in SVG.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""

# === Imports === 

import pandas as pd
import pygal
from pygal import Config
from pygal.style import Style
import sys

# === Read data functions


def load_statistics(statistics_file):
    """Loads the statistics TSV file."""
    with open(statistics_file, "r", encoding="utf8") as infile:
        statistics = pd.read_csv(infile, sep="\t", index_col=0)
        # print(statistics)
        if statistics.shape[0] > 0: 
            print("Looking good: simple statistics data has been loaded.")
        else: 
            sys.exit("ERROR! simple statistics data has not been loaded. Stopping.")
        return statistics


# === Visualization functions ===


def define_config():
    """Defines some configuration options for the pygal plot."""
    config = Config()
    config.show_legend = False
    config.legend_at_bottom = True
    config.human_readable = True
    config.print_values = True
    config.show_x_labels = True
    config.show_y_labels = True
    config.fill = True
    return config


def define_style():
    """Defines the pygal plot styling."""
    mystyle = Style(
        background="transparent",
        plot_background="transparent",
        font_family="googlefont:Alegreya",
        label_font_size=15,
        major_label_font_size=15,
        value_font_size=20,
        colors=(
            "DarkSlateGray",
            "DarkSlateGray",
            "DarkSlateGray",
            "DarkSlateGray",
            "DarkSlateGray",
            "DarkSlateGray"))
    return mystyle


def prepare_simple_data(statistics, selection):
    """Prepares data for visualization."""
    data = statistics.loc[selection, :]
    # print(data)
    return data


def make_barchart1(data, typesplot):
    """Creates a pygal barchart with the type frequency data."""
    config = define_config()
    mystyle = define_style()
    labels = list(data.index)
    values = list(data.loc[:, "values"])
    plot = pygal.HorizontalBar(config, style=mystyle)
    plot.title = "Distribution of Script-Identifiable Edits"
    plot.x_labels = labels
    plot.add("types", [
            {"value": values[0], "color": "DarkSlateGray", "label": labels[0]},
            {"value": values[1], "color": "DarkSlateGray", "label": labels[1]},
            {"value": values[2], "color": "DarkSlateGray", "label": labels[2]},
            {"value": values[3], "color": "DarkSlateGray", "label": labels[3]},
            {"value": values[4], "color": "DarkSlateGray", "label": labels[4]},
            {"value": values[5], "color": "DarkSlateGray", "label": labels[5]},
            ], stroke_style={"width": 0})
    plot.render_to_file(typesplot)
    print("Looking good: simple edit type visualization has been saved.")


# === Complex visualization functions


def load_pivotdata(pivotstatistics_file): 
    """Loads the transformed statistics data."""
    with open(pivotstatistics_file, "r", encoding="utf8") as infile: 
        complexdata = pd.read_csv(infile, sep="\t", index_col=0)
        #print(complexdata.head())
        if complexdata.shape[0] > 2: 
            print("Looking good: complex edit type data has been loaded.")
        else: 
            sys.exit("ERROR! complex edit type data has not been loaded. Stopping.")
        return complexdata


def prepare_complex_data(complexdata):
    """Prepares the more complex, transformed statistics data
    for visualization. Fills in blanks if necessary."""
    # print(complexdata)
    data = {}
    try:
        data["to be confirmed - all"] = complexdata.loc["tbc", "sums"]
    except:
        data["to be confirmed - all"] = 0
    try:
        data["condensation - minor"] = complexdata.loc["condensation", "minor"]
    except:
        data["condensation - minor"] = 0
    try:
        data["expansion - minor"] = complexdata.loc["expansion", "minor"]
    except:
        data["expansion - minor"] = 0
    try:
        data["condensation - major"] = complexdata.loc["condensation", "major"]
    except:
        data["condensation - major"] = 0
    try:
        data["expansion - major"] = complexdata.loc["expansion", "major"]
    except:
        data["expansion - major"] = 0
    try:
        data["deletion - all"] = complexdata.loc["deletion", "sums"]
    except:
        data["deletion - all"] = complexdata.loc["deletion", "sums"]
    try:
        data["insertion - all"] = complexdata.loc["insertion", "sums"]
    except:
        data["insertion - all"] = 0
    data = pd.DataFrame.from_dict(data, orient="index", columns=["counts"])
    # print(data)
    return data


def make_barchart2(data, typesplot):
    """Creates a barchart for the complex analysis categories."""
    config = define_config()
    mystyle = define_style()
    labels = list(data.index)
    values = list(data.loc[:, "counts"])
    plot = pygal.HorizontalBar(config, style=mystyle)
    plot.title = "Distribution of Complex Edit Types"
    plot.x_labels = labels
    plot.add("types", [
            {"value": values[0], "color": "DarkSlateGray", "label": labels[0]},
            {"value": values[1], "color": "DarkSlateGray", "label": labels[1]},
            {"value": values[2], "color": "DarkSlateGray", "label": labels[2]},
            {"value": values[3], "color": "DarkSlateGray", "label": labels[3]},
            {"value": values[4], "color": "DarkSlateGray", "label": labels[4]},
            {"value": values[5], "color": "DarkSlateGray", "label": labels[5]},
            {"value": values[6], "color": "DarkSlateGray", "label": labels[6]},
            ], stroke_style={"width": 0})
    plot.render_to_file(typesplot)
    print("Looking good: complex edit type visualization has been saved.")


def main(params):
    """Creates several barchars showing the frequencies
    of various kinds of edits in the data."""
    print("\n== coleto: running viz_distribution. ==")
    statistics = load_statistics(params["simplestatistics_file"])
    selection1 = [
        "italics",
        "whitespace",
        "hyphenation",
        "capitalization",
        "punctuation",
        "numbers"]
    data1 = prepare_simple_data(statistics, selection1)
    make_barchart1(data1, params["simpletypesplot"])
    complexdata = load_pivotdata(params["complexstatistics_file"])
    data2 = prepare_complex_data(complexdata)
    make_barchart2(data2, params["complextypesplot"])
