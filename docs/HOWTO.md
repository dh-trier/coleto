# coleto howto

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

#### On OSX

For wdiff: 
- This requires installation of Homebrew: https://brew.sh
- Then, do `brew install wdiff`. 

#### On Windows

### (A) Install as a package

(Coming soon.)

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

## For developers

Several tests have been implemented for coleto so far, more will follow. You can run them from the main `coleto` directory by doing `python -m pytest`. 

