#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.

"""
Loads the file containing the collation results from Wdiff.
Then, identifies various kinds of differences that can be observed.
Assembles this information for each difference between the two texts.

Part of coleto, see: https://github.com/dh-trier/coleto.
"""


# === Imports ===

import re
import pandas as pd
import Levenshtein as ld


# === Functions ===

def get_difftext(wdiffed_file):
    """Loads the file containing the collation results from Wdiff.
    Returns a list of lines with one or several differences.
    In our case, each line corresponds to one sentence."""
    # print("\n-- get_difftext")
    with open(wdiffed_file, "r") as infile:
        difftext = infile.read()
        difftext = re.split("\n", difftext)
        print("Looking good: there are " + str(len(difftext)) + " lines.")
        return difftext


def clean_line(line):
    """Cleans up the lines a little bit."""
    line = re.sub("]{", "] {", line)
    line = re.sub(r"(-\]) ([^{])", "\\1 {++} \\2", line)
    line = re.sub(r"(\w) ({)", "\\1 [--] \\2", line)
    return line


def create_pairs(line):
    """
    For every line, identifies each difference
    Then, collects each pair of differences separately.
    Returns a list of string pairs (one difference each)
    #==============================================================#
    #====    Much better, but still not entirely correct!      ====#
    #==============================================================#
    """
    pairs = []
    somepairs = re.findall(r"\[-.*?\-\] {\+.*?\+}", line, re.DOTALL)
    pairs.extend(somepairs)
    if len(pairs) == 0:
        somepairs = re.findall(r"\[-.*?\-\]", line, re.DOTALL)
        somepairs = [item + " {++}" for item in somepairs]
        pairs.extend(somepairs)
    if len(pairs) == 0:
        somepairs = re.findall(r"{\+.*?\+}", line, re.DOTALL)
        somepairs = ["[--] " + item for item in somepairs]
        pairs.extend(somepairs)
    return pairs


def prepare_item(item):
    """
    Prepares the items (each one pair from the list of pairs) to be compared.
    Returns the two items as separate strings.
    """
    item = re.split(r'\] {', item)
    item1 = item[0][2:-1]
    item2 = item[1][1:-2]
    return item1, item2


def define_itemdata(itemid, item1, item2):
    """
    Defines the various pieces of information to be collected for each pair.
    Returns a dictionary that already includes the pairs' text but not data.
    """
    itemdata = {"itemid": itemid,
                "version1": item1,
                "version2": item2,
                "lev-dist": "NA",
                "lev-dist-class": "NA",
                "lendiff-chars": "NA",
                "lendiff-words": "NA",
                "category": "NA",
                "main-type": "NA",
                "insertion": 0,
                "deletion": 0,
                "capitalization": 0,
                "whitespace": 0,
                "italics": 0,
                "punctuation": 0,
                "hyphenation": 0,
                "numbers": 0,
                "condensation": 0,
                "expansion": 0,
                "tbc": 0}
    return itemdata


def define_columnorder():
    """
    Defines the order of the columns, purely for display.
    Returns a list.
    """
    columns = ["itemid",
               "version1",
               "version2",
               "category",
               "main-type",
               "lev-dist",
               "lev-dist-class",
               "lendiff-chars",
               "lendiff-words",
               "insertion",
               "deletion",
               "capitalization",
               "whitespace",
               "italics",
               "punctuation",
               "hyphenation",
               "numbers",
               "condensation",
               "expansion",
               "tbc"]
    return columns


def perform_itemanalysis(itemdata, item1, item2):
    """
    This function performs the actual analysis.
    The procedure is applied to each pair in each line.
    For the most part, a substitution test is done and if successful,
    the corresponding category is assigned.
    More than one category can be assigned to an item.
    """
    # Test for insertion of new word(s)
    if len(item1) == 0:
        itemdata["insertion"] = 1
        itemdata["main-type"] = "insertion"
        itemdata["category"] = "other"
    # Test for complete deletion of word(s)
    elif len(item2) == 0:
        itemdata["deletion"] = 1
        itemdata["main-type"] = "deletion"
        itemdata["category"] = "other"
    # Test for difference in upper/lower case
    elif item1.lower() == item2.lower():
        itemdata["capitalization"] = 1
        itemdata["main-type"] = "capitalization"
        itemdata["category"] = "script-identifiable"
    # Test for difference in whitespace
    elif re.sub(" ", "", item1) == re.sub(" ", "", item2):
        itemdata["whitespace"] = 1
        itemdata["main-type"] = "whitespace"
        itemdata["category"] = "script-identifiable"
    # Test for difference in italics
    elif re.sub(r"\*", "", item1) == re.sub(r"\*", "", item2):
        itemdata["italics"] = 1
        itemdata["main-type"] = "italics"
        itemdata["category"] = "script-identifiable"
    # Test for difference in punctuation
    # FIXIT: Doesn't work like it should. Doesn't find punctuation.
    elif re.sub(r"[\",';:!?\.\(\)]", "", item1) == \
            re.sub(r"[\",';:!?\.\(\)]", "", item2):
        itemdata["punctuation"] = 1
        itemdata["main-type"] = "punctuation"
        itemdata["category"] = "script-identifiable"
    # Test for difference in hyphenation
    elif re.sub(r"\-", "", item1) == re.sub(" ", "", item2):
        itemdata["hyphenation"] = 1
        itemdata["main-type"] = "hyphenation"
        itemdata["category"] = "script-identifiable"
    # Test for difference in hyphenation
    elif re.sub(" ", "", item1) == re.sub(r"\-", "", item2):
        itemdata["hyphenation"] = 1
        itemdata["main-type"] = "hyphenation"
        itemdata["category"] = "script-identifiable"
    # Test for difference involving (but not limited to) numbers
    elif bool(re.search(r'\d', item1+item2)) is True:
        itemdata["numbers"] = 1
        itemdata["main-type"] = "numbers"
        itemdata["category"] = "script-identifiable"
    # Test for whether the length is substantially reduced
    elif len(item1) > len(item2)+3:
        itemdata["condensation"] = 1
        itemdata["main-type"] = "condensation"
        itemdata["category"] = "other"
    # Test for whether the length is substantially expanded
    elif len(item2) > len(item1)+3:
        itemdata["expansion"] = 1
        itemdata["main-type"] = "expansion"
        itemdata["category"] = "other"
    # If none of the above could be identified, mark it for human inspection.
    else:
        itemdata["tbc"] = 1
        itemdata["main-type"] = "tbc"
        itemdata["category"] = "other"
    # Information about the amount of condensation or expansion in characters
    itemdata["lendiff-chars"] = len(item2) - len(item1)
    # Information about the amount of condensation or expansion in words
    itemdata["lendiff-words"] = len(re.split(r"\W+", item2))\
        - len(re.split(r"\W+", item1))
    # Information about the Levenshtein distance
    itemdata["lev-dist"] = ld.distance(item1, item2)
    # print(itemdata["lev-dist"])
    # Classification of items by large or small Levenshtein distance
    if itemdata["lev-dist"] > 5:
        itemdata["lev-dist-class"] = "major"
    else:
        itemdata["lev-dist-class"] = "minor"
    return itemdata


def analyse_diffs(difftext):
    """This function coordinates the analysis of the differences.
    It iterates over each line, and over each difference in each line.
    Returns a pandas DataFrame containing all analysis data."""
    # print("-- analyse_diffs")
    allitemdata = []
    line_number = 0
    for line in difftext[:]:
        line_number += 1
        line = clean_line(line)
        # print("\n" + line)
        pairs = create_pairs(line)
        # for pair in pairs:
        #     print(pair)
        item_number = 0
        for item in pairs:
            item_number += 1
            item1, item2 = prepare_item(item)
            itemid = str(line_number)+"-"+str(item_number)
            itemdata = define_itemdata(itemid, item1, item2)
            itemdata = perform_itemanalysis(itemdata, item1, item2)
            # print(itemdata)
            allitemdata.append(itemdata)
    columns = define_columnorder()
    allitemdata = pd.DataFrame(allitemdata, columns=columns)
    # print(allitemdata)
    if allitemdata.shape[0] > 1:
        print("Looking good: some differences have been analysed.")
    else:
        print("Error! No differences have been analysed.")
    return allitemdata


def save_analysis(analysisresults, analysisfile):
    """Saves the pandas DataFrame to a TSV file."""
    with open(analysisfile, "w", encoding="utf8") as outfile:
        analysisresults.to_csv(outfile, sep="\t", index=False)


# === Main ===

def main(params):
    """Coordinates the analysis of the wdiff file."""
    print("== coleto: running analyse. ==")
    difftext = get_difftext(params["wdiffed_file"])
    analysisresults = analyse_diffs(difftext)
    save_analysis(analysisresults, params["analysis_file"])
