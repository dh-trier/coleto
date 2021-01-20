#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: textual_progression.py
# Author: Christof Schöch, 2016-2019.

"""
Script to visualize edits over textual progression.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


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
    print(pivotdata)
    data = {}
    try:
        data["to be confirmed - all"] = pivotdata.loc["tbc", "sums"]
    except:
        data["to be confirmed - all"] = 0
    try:
        data["condensation - minor"] = pivotdata.loc["condensation", "minor"]
    except:
        data["condensation - minor"] = 0
    try:
        data["expansion - minor"] = pivotdata.loc["expansion", "minor"]
    except:
        data["expansion - minor"] = 0
    try:
        data["condensation - major"] = pivotdata.loc["condensation", "major"]
    except:
        data["condensation - major"] = 0
    try:
        data["deletion - all"] = pivotdata.loc["deletion", "sums"]
    except:
        data["deletion - all"] = pivotdata.loc["deletion", "sums"]
    try:
        data["insertion - all"] = pivotdata.loc["insertion", "sums"]
    except:
        data["insertion - all"] = 0
    data = pd.DataFrame.from_dict(data, orient="index", columns=["counts"])
    print(data)
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


def main(params):
    print("== coleto: running visualize. ==")
    # FIXIT: Load data here from file.
    statistics = ana_stats(anadata, statistics)
    # FIXIT: Load data here from file.
    pivotdata = save_pivotdata(anadata, params["pivotstatistics_file"])
    selection1 = [
        "italics",
        "whitespace",
        "hyphenation",
        "capitalization",
        "punctuation",
        "numbers"]
    data1 = prepare_simple_data(statistics, selection1)
    make_barchart1(data1, params["typesplot1"])
    data2 = prepare_complex_data(pivotdata)
    make_barchart2(data2, params["typesplot2"])
