#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Visualize edit intensity over textual progression.
Relies on cumulated Levenshtein distances per sentence.
Uses the pygal library to create a barchart. 
Uses scipy for some smoothing. 
Input: The distribution statistics. 
Ouptut: Saves an SVG file to disk. 

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
import pygal
from pygal import Config
from pygal.style import Style
from scipy.signal import savgol_filter as sf
from os.path import join


# === Functions ===


def load_data(levdists_file):
    """Reads the data produced by statistics1: Levenshtein distances.
    Returns the DataFrame."""
    with open(levdists_file, "r") as infile:
        data = pd.read_csv(
            infile,
            sep="\t",
            index_col=0)
    #print(data.head(10))
    return data


def define_config():
    """Defines some configuration settings for the pygal plot."""
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


def define_style():
    """Defines a styling for the pygal plot."""
    mystyle = Style(
        background="transparent",
        plot_background="transparent",
        font_family="googlefont:Alegreya",
        label_font_size=30,
        major_label_font_size=30,
        value_font_size=40,
        title_font_size=35
        
        )
    return mystyle


def apply_smoothing(data, smoothing):
    """
    Apply Savitzky-Golay smoothing to the data for better readability.
    See: https://docs.scipy.org/doc/scipy-0.18.1/reference\
    /generated/scipy.signal.savgol_filter.html
    """
    if smoothing: 
        smoothed = sf(data, window_length=3, polyorder=1, mode="mirror")
        smoothed = sf(data, window_length=35, polyorder=1, mode="mirror")
    else: 
       smoothed = data  # with this, no smoothing is applied.
    return smoothed


def main(params):
    """Creates the visualization of the amount of change,
    calculated in Levenshtein distances per sentence,
    over the course of the textual progression."""
    print("\n== coleto: running viz_progression. ==")
    data = load_data(params["levdists_file"])
    lines = list(data.loc[:, "line"])
    script = apply_smoothing(data["script"], params["smoothing"])
    other = apply_smoothing(data["other"], params["smoothing"])
    config = define_config()
    mystyle = define_style()
    plot = pygal.StackedBar(config, style=mystyle)  # 60
    plot.title = "Edit intensity across the text"
    plot.y_title = "Levenshtein distance (smoothed)"
    plot.x_title = "Sentences in the text"
    plot.x_labels = lines
    plot.add("Script-Identifiable Edits", script)
    plot.add("Other Edits", other)
    plot.render_to_file(params["progressionplot"])
    print("Looking good: The progression visualization has been saved.")
