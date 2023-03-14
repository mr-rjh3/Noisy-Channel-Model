"""
------------------------------------------------------------------------------------------
File:    noisy_channel.py
Purpose: Assignment 2, Question 4
------------------------------------------------------------------------------------------
Author:  Riley Huston
Due:  2023-02-13
"""
import argparse
import alive_progress as alive_bar
import nltk
from nltk.tokenize import RegexpTokenizer
import enchant
import os

def readFile(filename):
    if(not os.path.isfile(filename)):
        print(f"File {filename} does not exist. Is it in the same directory as noisy_channel.py?")
        exit()
    print(f"Reading {filename}...")
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    return data

def readErrorFile():
    print("Reading error file...")
    errors = {}
    with open("spell-errors.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            words = line.split(": ")
            errors[words[0]] = words[1].split(", ")
    return errors

def tokenizeData(data):
    print("Tokenizing data...")
    with alive_bar.alive_bar():
        tokenizer = RegexpTokenizer(r'\w+') # remove punctuation
        corpus = tokenizer.tokenize(data)
    return corpus

def getWordProb(corpusDist, corpusSize, words):
    corpusProb = {}
    for word in words:
        prob = corpusDist[word] / corpusSize
        # print(f"P({word}) = {prob}")
        corpusProb[word] = prob
    return corpusProb

def getCommonErrorProb(errorsDict, words):
    errorProb = {}
    for word in words:
        if word in errorsDict:
            # Word in in file of common mispellings
            prob = len(errorsDict[word]) / 100
            errorProb[word] = prob
        else:
            # Word is not in file of common mispellings
            errorProb[word] = 0
    return errorProb

def getLevenshteinDistance(suggestion, error):
    # possible operations: insertion, deletion, substitution (transposition is not considered)
    # insertion: add a letter (e.g. "cat" -> "cats" thus difference in length)
    # deletion: remove a letter (e.g. "cats" -> "cat" thus difference in length)
    # substitution: replace a letter (e.g. "cat" -> "cut" iterates through both words and finds each difference)

    distance = abs(len(suggestion)-len(error)) # initialize with difference in length
    # find the minimum length of the two words
    if len(suggestion) < len(error): 
        minlength = len(suggestion)
    else:
        minlength = len(error)
    # iterate through both words until we reach the end of one, for each difference found add 1 to the distance
    for i in range(minlength):
        if suggestion[i] != error[i]:
            distance += 1
    return abs(distance / len(suggestion) - 1) # return the distance as a percentage of the suggested word that is the same


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Page Rank Program')
    parser.add_argument("-c", "--correct", help="List of words in an array and for each prints best word to replace.", default=[], nargs='+', type=str) # nargs='+' means 1 or more
    parser.add_argument("-p", "--proba", help="List of words in an array and for each item prints P(w).", default=[], nargs='+', type=str) # nargs='+' means 1 or more
    parser.add_argument("-f", "--filename", help="Supplies the program with the file to train the noisy channel model on. Recommended to use txt file. Default is 'big.txt'.", default="big.txt", type=str) # nargs='+' means 1 or more
    
    args = parser.parse_args()

    # Initial check to see if there are any words that are spelled correctly
    d = enchant.Dict("en_US") # create a dictionary for the "en_US" language to verify if a word is spelled correctly
    suggestions = {}
    noSuggestions = True
    for error in args.correct:
        suggestions[error] = d.suggest(error)
        if(len(suggestions[error]) > 0):
            noSuggestions = False
        # print(f"Suggestions for {error}: ", suggestions[error])
    for error in args.proba:
        suggestions[error] = d.suggest(error)
        if(len(suggestions[error]) > 0):
            noSuggestions = False
        # print(f"Suggestions for {error}: ", suggestions[error])
    if(len(suggestions) == 0):
        print("No words to check.")
        exit()
    if(noSuggestions):
        print("No suggestions for any of the words.")
        exit()
    data = readFile(args.filename)
    corpus = tokenizeData(data)
    print("Corpus size: ", len(corpus))

    stopwords = nltk.corpus.stopwords.words('english')
    corpusDist = nltk.FreqDist(token.lower() for token in corpus if token not in stopwords) # frequency distribution of the words in the corpus
    

    # Getting P(w) for the suggested words
    probOfSuggestionsInCorpus = {}
    for error in suggestions:
        probOfSuggestionsInCorpus[error] = getWordProb(corpusDist, len(corpus), suggestions[error])

    
    # Getting P(e|w) for the suggested words 
    # Start by getting the error probability from common mispellings
    # get dictionary of words and their common mispellings (will not contain all mispellings / all words)
    errorsDict = readErrorFile() 
    probOfSuggestionsInError = {}
    for error in suggestions:
        probOfSuggestionsInError[error] = getCommonErrorProb(errorsDict, suggestions[error]) 
    # Next add the error probability from levenshtein distance (P(e|w) = distance/100)
    for error in suggestions:
        for suggestion in suggestions[error]:
            probOfSuggestionsInError[error][suggestion] += getLevenshteinDistance(error, suggestion) # multiply current error probability with difference percentage (from levenshtein distance)

    # Getting P(e|w)*P(w) for the suggested words
    probOfSuggestions = {}
    for error in suggestions:
        probOfSuggestions[error] = {}
        for suggestion in suggestions[error]:
            probOfSuggestions[error][suggestion] = probOfSuggestionsInCorpus[error][suggestion] * probOfSuggestionsInError[error][suggestion] # P(e|w) * P(w)
    
    # for suggestion in probOfSuggestionsInCorpus:
    #     print(f"P(w) Suggestion {suggestion}: ", probOfSuggestionsInCorpus[suggestion])
    # for suggestion in probOfSuggestionsInError:
    #     print(f"P(e|w) Suggestion {suggestion}: ", probOfSuggestionsInError[suggestion])
    # for suggestion in probOfSuggestions:
    #     print(f"Prob for Suggestion for {suggestion}: ", probOfSuggestions[suggestion])

    # Find the word with the highest probability for each word in args.correct
    for error in args.correct:
        maxProb = 0
        maxWord = ""
        if(len(suggestions[error]) == 0):
            print(f"{error} has no suggested words.")
        for suggestion in suggestions[error]:
            if probOfSuggestions[error][suggestion] > maxProb:
                maxProb = probOfSuggestions[error][suggestion]
                maxWord = suggestion
        if(maxProb == 0):
            print(f"{error} has no suggested words. Due to P(w) being 0 for all suggestions. I suggest you use a larger corpus.")
        else:
            print(f"Best word to replace {error} is {maxWord}")

    # print the probability for each word in args.proba
    for error in args.proba:
        maxProb = 0
        maxWord = ""
        for suggestion in suggestions[error]:
            if probOfSuggestions[error][suggestion] > maxProb:
                maxProb = probOfSuggestions[error][suggestion]
                maxWord = suggestion
        if(maxProb == 0):
            print(f"{error} has no suggested words due to P(w) being 0 for all suggestions. I suggest you use a larger corpus.")
        else:
            print(f"Probablility that {error} was meant to be {maxWord}: {maxProb}, P(w): {probOfSuggestionsInCorpus[error][maxWord]}, P(e|w): {probOfSuggestionsInError[error][maxWord]}")