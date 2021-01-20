#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2021.


"""
Script that runs the coleto text collation pipeline.
Please see the readme.md file and the documentation.
"""


# === Imports ===

import parameters
import preprocess
import wdiff
import analyze
import statistics
import progression


# === Functions ===


def main():
    params = parameters.main()
    preprocess.main(params)
    wdiff.main(params)
    analyze.main(params)
    # statistics.main(params)
    # progression.main(params)


main()
