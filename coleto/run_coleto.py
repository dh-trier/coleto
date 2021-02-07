#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.


"""
This is the main script that controls the coleto text collation pipeline.

For more information, please see the README.md and HOTWO.md files.
An API reference can be found in the docs folder.
"""


# === Imports ===

import meta_parameters
import text_preprocess
import text_wdiff
import text_analyze
import stats_progression
import stats_distribution
import viz_progression
import viz_distribution
import meta_documentation


# === Functions ===


def main():
    """Defines the coleto pipeline."""
    params = meta_parameters.main()
    text_preprocess.main(params)
    text_wdiff.main(params)
    analysissummary = text_analyze.main(params)
    stats_progression.main(params)
    stats_distribution.main(params)
    viz_progression.main(params)
    viz_distribution.main(params)
    meta_documentation.main(params, analysissummary)
    print("\n== coleto: All done. ==\n\n")


main()
