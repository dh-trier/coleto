# coleto howto

This is where the documentation will one day be placed. 


1) requirements:

- Python 3. This package has been tested with Python 3.8. It should also work with Python 3.6+

-  Python package: Levenshtein. 
https://pypi.org/project/python-Levenshtein/

- Python package: pygal 
http://www.pygal.org/en/stable/installing.html 

- NLTK (?)

- NLTK punkt module

 >>> import nltk
  >>> nltk.download('punkt')

- wdiff
	- on OSX, this requires installation of Homebrew: https://brew.sh
	- then brew install wdiff 

2) Download two folders and place them both in one directory:

https://github.com/dh-trier/coleto.git 
https://github.com/dh-trier/coleto-data.git

3) run the run_coleto.py script, which is in the coleto_main directory

On Mac, use  the cd command to navigate to the folder in Terminal, then 

python3 run_coleto.py  

4) If everything works, this will create the output files in coleto-data-main/Doyle/output

