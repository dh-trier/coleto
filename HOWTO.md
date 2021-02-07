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

### Install wdiff

#### On Linux 

In the terminal, do the following: 

- `sudo apt-get update`
- `sudo apt-get install wdiff`. 

#### On OSX

Installation of wdiff requires installation of Homebrew: https://brew.sh. 

Then, do `brew install wdiff`. 

#### On Windows

See this page for instructions on how to download and install wdiff for Windows: https://www.di-mgt.com.au/wdiff-for-windows.html

### Install directly via the repos

Download as a ZIP archive, or clone using Git, the following repository: https://github.com/dh-trier/coleto.git. 

If you downloaded the ZIP archive, unzip the file and place the contents a directory of your choice. 

If you cloned the repository, just make sure you cloned it to a location where you can run it from. 

## Usage

Generally speaking, there are four steps to running coleto. 

1. Place input data in the right folder
2. Adjust the configuration file
3. Run the coleto pipeline
4. Inspect the results

### Input files

Place your input data in the right folder. If you're using sample data provided in `coleto/data`, you are all set. If you're ready to analyze your own data, create a new directory on the same level as the sample data directories, create an directory called `input` in there and place the two texts you would like to compare in the `input`directory. 

### Adjust the config file

Adjust the parameters in the `config.yaml` file found in the top-level or main `coleto` directory. Remember to maintain the whitespace character after the colon when modifying the values.

This is what each parameter means: 

- `working_directory`: This specifies where on your system the main coleto directory (the copy of the repository) is located in. Default: "". 
- `dataset`: The directory name of the dataset folder inside the `data` directory, and containing the `input` and `output`folders for this dataset. Default: "Doyle". 
- `language`: The language of the text files to be compared. Default: en (English). 
- `smoothing`: Whether or not the visualization of the amount of changes over text time uses smoothing or not. Recommended to be `True`for longer texts, `False` for short texts. Default: `True`. 
- `levenshtein_cutoff`: The cutoff value for the categorization of edits as major or minor, in terms of their Levenshtein distance. Any edit with a value larger than this will be categorized as major, any other edit will be categorized as minor. Default: `5`.
- `documentation_mode`: Whether the script should save a minimal documentation of each run (just one timestamped file with some metadat) or a complete documentation (all data files, scripts and the config file). Default: minimal. (The `complete` mode is not implemented yet.)

### Run coleto

Run coleto, either from the command line or from an IDE. 

#### Running coleto from the command line

Run the run_coleto.py script, which is in the `coleto/coleto/` directory. 

On Mac and Linux, use  the `cd` command to navigate to the main `coleto?` folder in Terminal, then run: `python3 coleto/run_coleto.py`  

Watch our for the programm messages on the progress with processing the files. There should not be any warnings or errors. If everything works fine, coleto will create the output files in the directory `data/{dataset}/output`. 

#### Running coleto from an IDE

Use your IDE to open the file `run_coleto.py`, then press `F5` to execute the pipeline. 

### Inspect the results

Inspect the results, which are all written to the `output` directory inside the corresponding data directory. 


## What coleto does

### The pipeline

1. `config.yaml`: This is where the user sets some configurations. 
1. `meta_parameters.py`: This is parameters are generated and packaged up in the `params` variable, a `dict` containing all programme parameters, in particular directories, paths and settings. 
1. `text_preprocess`: This step essentially performs sentence splitting, as well as some gentle cleaning-up, on the input texts. 
1. `text_wdiff`: In this step, wdiff is called to perform the actuall collation of the texts. 
1. `text_analyze`: This this step, the wdiff output is analyzed and the results are saved to a TSV file. This is the main contribution of coleto (see details below). 
1. `stats_progression`: This submodule calculates the data for `viz_progression`, namely the amount of change detected in each sentence of the text.
1. `viz_progression`: This submodule uses `pygal`to create a stacked barchart showing how the amount of changes varies over the texts' development from beginning to end.
1. `stats_distribution`: This submodule calculates how many instances of different types of changes detected by the `text_analyze`step. 
1. `viz_distribution`: This submodule uses `pygal` to create some barcharts showing the distribution of types of changes. 
1. `meta_documentation`: This submodule writes all the parameters of the current run to a timestamped file along with very basic summary statistics. 

### The analysis step 

The main contribution of coleto is that it takes a good look at each individual instance of a difference between the two text versions and attempts to describe it quantitatively and categorize it. The following is a list of things that are checked and registered. (More are in development.)

**Quantitative / descriptive aspects**

1. `itemid`: A unique identifier is assigned to each difference. 
1. `version1`: The string in version 1 of the text. 
1. `version2`: The string in version 2 of the text. 
1. `lev-dist`: The levenshtein difference between the two strings. 
1. `lev-dist-class`: The class assigned to the levenshtein distance (minor or major, with a cut-off at a levenshtein distance of 5). 
1. `lendiff-chars`: The (positive or negative) difference in length between the two strings in characters. 
1. `lendiff-words`: The (positive or negative) difference in length between the two strings expressed in words. 
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

