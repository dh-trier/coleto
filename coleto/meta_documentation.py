#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2019.

"""
Script to save settings and parameters to disk for documentation. 
Each time coleto is run, a timestamped file is created with this information.
The purpose is to document, for any results, the parameters used. 

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
from datetime import datetime


# === Functions ===

def get_timestamp():
    """Generates and formats the current time's timestamp as a string.
    This allows to save a separate, unique documentation file for each run."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    return timestamp


def collect_documentation(params, analysissummary):
    """Collects parameters, settings, timestamp, filenames.
    This allows major factors conditioning results to be documented."""
    documentation = params
    documentation["timestamp"] = get_timestamp()
    documentation["numlines"] = analysissummary["numlines"]
    documentation["numdifferences"] = analysissummary["numdifferences"]
    return documentation


def generate_filename(documentation):
    """Generates the unique filename from the timestamp data."""
    timestamp = documentation["timestamp"]
    timestamp = re.sub(":", "-", timestamp)
    timestamp = re.sub(" ", "_", timestamp)
    documentation_name = documentation["documentation_name"]
    documentation_filename = documentation_name + "_" + timestamp + ".txt"
    return documentation_filename


def save_documentation(documentation):
    """Saves the documentation file to disc.
    For this to work, all info is turned into a suitable string."""
    documentation_filename = generate_filename(documentation)
    str_documentation = "## coleto documentation for run: "\
                        + documentation["timestamp"] + ".\n\n"
    for key, value in documentation.items():
        str_documentation = str_documentation\
                            + "- " + str(key) + " : " + str(value) + "\n"
    try:
        with open(documentation_filename, "w", encoding="utf8") as outfile:
            outfile.write(str_documentation)
        print("Looking good: Some documentation of this run has been saved.")
    except:
        print("Warning: Documentation of this run has NOT been saved.")


# === Main function ===

def main(params, analysissummary):
    """Creates documentation of the current analysis."""
    print("\n== coleto: running meta_documentation. ==")
    if params["documentation_mode"] == "minimal":
        documentation = collect_documentation(params, analysissummary)
        save_documentation(documentation)
