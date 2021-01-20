#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2019.

"""
Script to create some statistics from the diff analysis data.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
import numpy as np
from os.path import join
import pygal
from pygal import Config
from pygal.style import Style


# === Functions ===

def read_datafile(csvfile):
    """
    Read a CSV file with data.
    """
    with open(csvfile, "r") as infile:
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
    """Saves the analysis data to a CSV file."""
    with open(statisticsfile, "w", encoding="utf8") as outfile:
        statistics.to_csv(outfile, sep="\t")


def save_pivotdata(anadata, pivotstatisticsfile):
    """Saves a selection of data in pivoted format to a CSV file."""
    pivotdata = anadata.pivot_table(
        index="main-type",
        columns="lev-dist-class",
        aggfunc='size',
        fill_value=0)
    pivotdata["sums"] = pivotdata.sum(axis=1)
    with open(pivotstatisticsfile, "w", encoding="utf8") as outfile:
        pivotdata.to_csv(outfile, sep="\t")
    return pivotdata


# === Visualization functions ===

def define_config():
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
    data = statistics.loc[selection, :]
    # print(data)
    return data


def make_barchart1(data, typesplot):
    config = define_config()
    mystyle = define_style()
    labels = list(data.index)
    values = list(data.loc[:, "values"])
    plot = pygal.HorizontalBar(config, style=mystyle)
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


def prepare_complex_data(pivotdata):
    data = {}
    data["to be confirmed - all"] = pivotdata.loc["tbc", "sums"]
    data["condensation - minor"] = pivotdata.loc["condensation", "minor"]
    data["expansion - minor"] = pivotdata.loc["expansion", "minor"]
    data["condensation - major"] = pivotdata.loc["condensation", "major"]
    data["expansion - major"] = pivotdata.loc["expansion", "major"]
    data["deletion - all"] = pivotdata.loc["deletion", "sums"]
    data["insertion - all"] = pivotdata.loc["insertion", "sums"]
    data = pd.DataFrame.from_dict(data, orient="index", columns=["counts"])
    # print(data)
    return data


def make_barchart2(data, typesplot):
    config = define_config()
    mystyle = define_style()
    labels = list(data.index)
    values = list(data.loc[:, "counts"])
    plot = pygal.HorizontalBar(config, style=mystyle)
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


# === Main function ===


def main(params):
    print("== coleto: running statistics. ==")
    # (1) Collect data
    statistics = {}
    levdata = read_datafile(params["levdists_file"])
    statistics = lev_stats(levdata, statistics)
    anadata = read_datafile(params["analysis_file"])
    statistics = ana_stats(anadata, statistics)
    save_data(statistics, params["statistics_file"])
    pivotdata = save_pivotdata(anadata, params["pivotstatistics_file"])
    # (2) Visualize data
    selection1 = [
        "italics",
        "whitespace",
        "hyphenation",
        "capitalization",
        "punctuation",
        "numbers"]
    data1 = prepare_simple_data(statistics, selection1)
    make_barchart1(data1, params["typesplot1"])
    # data2 = prepare_complex_data(pivotdata)
    # make_barchart2(data2, params["typesplot2"])
