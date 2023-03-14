# Noisy-Channel-Model

## Purpose
Finds corrections based on input using the noisy channel model. Language model is unigram frequency distributuion based on [big.txt](http://norvig.com/big.txt) from Peter Norvig, error model is based on [spell-errors.txt](https://norvig.com/ngrams/spell-errors.txt) dataset borrowed from Peter Norvig as well and Levenshtien distance.

## Usage
1. Download and install [python](https://www.python.org/downloads/)
2. Clone the repo
3. Run `pip -r requirements.txt`
4. Run `python ./noisy_channel.py [-OPTIONS]`

## Options
`-c`, `--correct`
  - List of words that the program will find the best word to replace with. Please ensure the list is space separated: `-c word1 word2 word3 ...`
    
`-p`, `--proba`
  - List of words in an array and for each item prints it's probability from the noisy channel model (P(w), P(e|w)). Please ensure the list is space separated: `-p word1 word2 word3 ...`
  
`-f`, `--filename`
  - Supplies the program with the file to train the noisy channel model on if you would like. Recommended to use txt file. Default is 'big.txt'.
