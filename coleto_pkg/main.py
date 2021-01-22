#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Christof Schöch, 2016-2019.

"""
Run the coleto collation pipeline.

Part of coleto, see: https://github.com/dh-trier/coleto. 
"""


# === Imports ===

import os
from os.path import join

import preprocess
#import martians2_wdiff
#import martians3_analyse
#import martians4_progression
#import martians5_statistics


# === Files and folders ===

workdir = ""
inputs = join(workdir, "input", "*.txt")
outputs = join(workdir, "output", "")
sentfile1 = join(workdir, "output", "martian1-sent.txt")
sentfile2 = join(workdir, "output", "martian2-sent.txt")
wdfile = join(workdir, "output", "martians12_wdiffed.txt")
analysisfile = join(workdir, "output", "martians12_diff-analysis.csv")
levdistsfile = join(workdir, "output", "martian_lev-dists-by-line.csv")
progressionplot = join(workdir, "output", "martian_edits-over-textual-progression.svg")
statisticsfile = join(workdir, "output", "martian_statistics.csv")
pivotstatisticsfile = join(workdir, "output", "martian_pivot-statistics.csv")
typesplot1 = join(workdir, "output", "typesplot1.svg")
typesplot2 = join(workdir, "output", "typesplot2.svg")


if not os.path.exists(outputs):
    os.makedirs(outputs)


# === Functions ===

#martians1_preprocess.main(inputs, outputs)
#martians2_wdiff.main(sentfile1, sentfile2, wdfile)
#martians3_analyse.main(wdfile, analysisfile)
#martians4_progression.main(analysisfile, levdistsfile, progressionplot)
martians5_statistics.main(analysisfile, levdistsfile, statisticsfile, pivotstatisticsfile, typesplot1, typesplot2)
