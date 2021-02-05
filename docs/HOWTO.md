# HOW-TO for coleto

Coleto is a text comparison, or collation, tool written in Python and using wdiff in the background. 

This document explains the installation requirements, installation procedure and general usage of coleto. In addition, it describes the processing steps involved in coleto. 

See also the general information on coleto in the [README](https://github.com/dh-trier/coleto/blob/main/README.md). 

## Requirements

### Python 

Python 3. This package has been tested with Python 3.8. It should also work with Python 3.6+

Python packages

* Levenshtein: https://pypi.org/project/python-Levenshtein/; install through pip
* pygal: http://www.pygal.org/en/stable/installing.html; install through pip
* NLTK: http://www.nltk.org/; install through pip
* NLTK punkt model: 

### Non-Python 

* wdiff


## Installation instructions

### Install Python requirements

Using pip, install all Python packages listed above. 

To download the NLTK punkt model, on the command line / terminal, enter: `python3`, then `import nltk`, then `nltk.download('punkt')`. 

### Install Non-Python requirements

#### On Linux 

TBD.

#### On OSX

For wdiff: 
- This requires installation of Homebrew: https://brew.sh
- Then, do `brew install wdiff`. 

#### On Windows

TBD.

### (A) Install as a package

(Coming soon to pypi.)

### Alternatively, install directly via the repos

Download as a ZIP archive, or clone using Git, the following two repositories: two folders and place them both in one directory:

* https://github.com/dh-trier/coleto.git
* https://github.com/dh-trier/coleto-data.git

If you downloaded the ZIP archive, unzip both files and place the contents in the same directory. In that directory, you should see two folders: `coleto` and `coleto-data` side by side. 

If you cloned the repositories, just make sure you clone both to the same directory, so that again, you have the two folders side by side. This will ensure coleto easily finds the data. 

## Usage

Generally speaking, there are four steps to running coleto. 

(1) Place your input data in the right folder. If you're using sample data provided in `coleto-data`, you are all set. If you're ready to analyze your own data, create a new directory on the same level as the sample data directories, create an directory called `input` in there and place the two texts you would like to compare in the `input`directory. 

(2) Adjust the parameters in the `parameters.py` file found in `coleto/coleto_pkg`. 

(3) Run coleto, either from the command line or from an IDE. 

(4) Inspect the results, which are all written to the `output` directory inside the corresponding data directory. 

### From the command line

Run the run_coleto.py script, which is in the coleto_main directory

On Mac, use  the cd command to navigate to the folder in Terminal, then 

python3 run_coleto.py  

If everything works, this will create the output files in coleto-data-main/Doyle/output

### From an IDE

Open `parameters.py` to adjust the parameters. 

Open `run_coleto.py` to execute the pipeline. 

## What coleto actually does

### The pipeline

1. `parameters.py`: This is where the user sets some parameters and additional parameters are generated and packaged up in the `params` variable, a `dict` containing all programme parameters, in particular directories, paths and settings. 
1. `text_preprocess`: This step essentially performs sentence splitting, as well as some gentle cleaning-up, on the input texts. 
1. `text_wdiff`: In this step, wdiff is called to perform the actuall collation of the texts. 
1. `text_analyze`: This this step, the wdiff output is analyzed and the results are saved to a TSV file. This is the main contribution of coleto (see details below). 
1. `stats_progression`: This submodule calculates the data for `viz_progression`, namely the amount of change detected in each sentence of the text.
1. `viz_progression`: This submodule uses `pygal`to create a stacked barchart showing how the amount of changes varies over the texts' development from beginning to end.
1. `stats_distribution`: This submodule calculates how many instances of different types of changes detected by the `text_analyze`step. 
1. `viz_distribution`: This submodule uses `pygal` to create some barcharts showing the distribution of types of changes. 

### The analysis step 

The main contribution of coleto is that it takes a good look at each individual instance of a difference between the two text versions and attempts to describe it quantitatively and categorize it. The following is a list of things that are checked and registered. (More are in development.)

**Quantitative / descriptive aspects**

1. `itemid`: A unique identifier is assigned to each difference. 
1. `version1`: The string in version 1 of the text. 
1. `version2`: The string in version 2 of the text. 
1. `lev-dist`: The levenshtein difference between the two strings. 
1. `lev-dist-class`: The class assigned to the levenshtein distance (minor or major, with a cut-off at a levenshtein distance of 5). 
1. `lendiff-chars`: The absolute difference in length between the two strings in characters. 
1. `lendiff-words`: The absolute difference in length between the two strings expressed in words. 
1. `condensation`: Positive if the length in characters of string 2, when compared to string 1, is smaller by at least 3 characters. 
1. `expansion`: Positive if the length in characters of string 2, when compared to string 1, is larger by at least 3 characters. 
1. `insertion`: Positive if the length of string 1 is 0. 
1. `deletion`: Positive if the length of string 2 is 0. 

**Qualitative / categorical aspects** 

1. `category`: A first, rough categorization as to whether the difference is `script-identifiable` (is happening purely on the surface level) or not. 
1. `main-type`: A second categorization, depending on the type of difference detected. The following is a list of these categories. These categories are also noted in binary fashion in the results table to facilitate manipulation and calculations. 
1. `capitalization`: Positive if the difference between the two strings depends only on capitalization. 
1. `whitespace`: Positive if the difference between the two strings depends only on whitespace. 
1. `italics`: Positive if the difference between the two strings depends only on markers for italics, like `*` or `_`. 
1. `punctuation`: Positive if the difference between the two strings depends only on punctuation. 
1. `hyphenation`: Positive if the difference between the two strings depends only on hyphenation. 
1. `numbers`: Positive if the difference between the two strings involves numbers. 
1. `tbc`: Positive if none of the above qualitative / categorical aspects could be identified. This is particularly the case (a) when the difference is created by a combination of the above-mentioned categories or (b) when the difference cannot be reduced to surface features but rather resides in the semantics. 

All of this information is written to a TSV file called `diff-analysis.tsv` that is the key output of coleto. It can be inspected manually and is used to generate the subsequent statistics and visualizations. 


## For developers

Several tests have been implemented for coleto so far, more will follow. You can run them from the main `coleto` directory by doing `python -m pytest`. 

