# Portfolio Chapter 8 N-grams
# By Jibin Prince
# Program 2 - Use language dictionaries from Program 1 to predict language line by line of test data

# Imports
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
import os


def compute_probabilities(line, uni_english, uni_french, uni_italian, bi_english, bi_french, bi_italian):
    # Get total vocabulary size
    total_vocab_size = len(dict(uni_english)) + len(dict(uni_french)) + len(dict(uni_italian))

    # Get unigrams and bigrams of given line
    unigrams_test = word_tokenize(line)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # Calculate English probability using Laplace Smoothing
    prob_english = 1
    for bigram in bigrams_test:
        b = bi_english[bigram] if bigram in bi_english else 0
        u = uni_english[bigram[0]] if bigram[0] in uni_english else 0
        v = total_vocab_size
        prob_english = prob_english * ((b + 1) / (u + v))

    # Calculate French probability using Laplace Smoothing
    prob_french = 1
    for bigram in bigrams_test:
        b = bi_french[bigram] if bigram in bi_french else 0
        u = uni_french[bigram[0]] if bigram[0] in uni_french else 0
        v = total_vocab_size
        prob_french = prob_french * ((b + 1) / (u + v))

    # Calculate Italian probability using Laplace Smoothing
    prob_italian = 1
    for bigram in bigrams_test:
        b = bi_italian[bigram] if bigram in bi_italian else 0
        u = uni_italian[bigram[0]] if bigram[0] in uni_italian else 0
        v = total_vocab_size
        prob_italian = prob_italian * ((b + 1) / (u + v))

    # Get language with the highest probability
    highest_prob = max(prob_english, prob_french, prob_italian)
    if highest_prob == prob_english:
        lang = "English"
    elif highest_prob == prob_french:
        lang = "French"
    else:
        lang = "Italian"

    return lang


if __name__ == "__main__":
    # Read in pickled dictionaries
    print("Read picked dictionaries start")
    with open("uni_english.pickle", 'rb') as handle:
        uni_english_dict = pickle.load(handle)

    with open("bi_english.pickle", 'rb') as handle:
        bi_english_dict = pickle.load(handle)

    with open("uni_french.pickle", 'rb') as handle:
        uni_french_dict = pickle.load(handle)

    with open("bi_french.pickle", 'rb') as handle:
        bi_french_dict = pickle.load(handle)

    with open("uni_italian.pickle", 'rb') as handle:
        uni_italian_dict = pickle.load(handle)

    with open("bi_italian.pickle", 'rb') as handle:
        bi_italian_dict = pickle.load(handle)
    print("Read picked dictionaries end\n")

    # Calculate probabilities of language of test data and write the highest probability language to file
    print("Calculate language probabilities of test data start")
    if os.path.exists("Highest Probability Lang From Test Data.txt"):
        os.remove("Highest Probability Lang From Test Data.txt")
    counter = 1
    with open("data/LangId.test", 'r') as f:
        for line_text in f:
            language = compute_probabilities(line_text, uni_english_dict, uni_french_dict, uni_italian_dict,
                                             bi_english_dict, bi_french_dict, bi_italian_dict)
            with open("Highest Probability Lang From Test Data.txt", 'a') as file:
                file.write(str(counter) + " " + language + "\n")
            counter += 1
    print("Calculate language probabilities of test data end\n")

    # Calculate accuracy of language prediction done previously with given solution
    print("Get accuracy start")
    with open("data/LangId.sol", 'r') as solFile:
        solFile_list = [line for line in solFile]
    with open("Highest Probability Lang From Test Data.txt", 'r') as predictedFile:
        predictedFile_list = [line for line in predictedFile]

    line_count = 0
    correct = 0
    print("\nIncorrectly classified lines")
    for line in solFile_list:
        if solFile_list[line_count] == predictedFile_list[line_count]:
            correct += 1
        else:
            print(str(line_count + 1))
        line_count += 1

    accuracy_percent = float(correct / line_count) * 100
    print("\nAccuracy: " + str(accuracy_percent) + "%\n")

    print("Get accuracy end")

