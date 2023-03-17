# Noisy-Channel-Model

## Purpose
Finds corrections based on input using the noisy channel model. Language model is unigram frequency distributuion based on [big.txt](http://norvig.com/big.txt) from Peter Norvig, error model is based on [spell-errors.txt](https://norvig.com/ngrams/spell-errors.txt) dataset borrowed from Peter Norvig as well and Levenshtien distance.

## Noisy Channel Model

The noisy channel model is a method of finding corrections for “noisy” or misspelled words. The model is based in probability and is as follows:

### $$\hat{w} = P(e|w)P(w)$$

$\hat{w}$ is the probability that the word $w$ is the proper spelling of the misspelled word $e$. $P(w)$ is the language model or the probability that the suggested word $w$ is correct given the current context, $P(e|w)$ is the channel / error model or the probability that the error $e$ is generated from suggested word $w$. To find suggested words I used Pyenchant, a python library that checks the spelling of words and suggests replacements. When programming the implementation of this algorithm there are many ways to generate its probabilities using different models, however I chose to use unigram frequency from a given file for our language model, and a mixture of a frequent error dataset and Levenshtein distance for our error model. The error dataset works well for words within this it's database but not all words are recorded, thus it is also important to have an alternative method for such words. This can also enable us to know which word in the frequent error list is closer to being the proper spelling. For these cases we will employ the use of Levenshtein distance. Levenshtein distance is the number of differences in a given word compared to another, these differences can be split into four groups: insertion, deletion, substitution, and transposition. This gives us a number we can use to estimate how close our error is to a suggested word and in our case we return the percentage of the suggested word that is the same as our error, or the absolute value of: (Levenshtein distance / length of the suggestion) - 1. We can add this percentage to our error probability from our error dataset and now have our final $P(e|w)$. From here we can simply multiply both $P(w)$ and $P(e|w)$ together and take the word with the greatest probability as our replacement.

## Usage
1. Download and install [python](https://www.python.org/downloads/)
2. Clone the repo
3. Run `pip install -r requirements.txt`
4. Run `python ./noisy_channel.py [-OPTIONS]`

## Options
`-c`, `--correct`
  - List of words that the program will find the best word to replace with. Please ensure the list is space separated: `-c word1 word2 word3 ...`
    
`-p`, `--proba`
  - List of words in an array and for each item prints it's probability from the noisy channel model (P(w), P(e|w)). Please ensure the list is space separated: `-p word1 word2 word3 ...`
  
`-f`, `--filename`
  - Supplies the program with the file to train the noisy channel model on if you would like. Recommended to use txt file. Default is 'big.txt'.
