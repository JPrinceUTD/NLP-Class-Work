# Portfolio Chapter 8 N-grams
# By Jibin Prince
# Program 1 - Build unigram and bigram dictionaries from the English, French, and Italian train data

# Imports
from nltk import word_tokenize
from nltk.util import ngrams
import pickle


def create_dictionaries(file_name):
    """
    Create unigram and bigram dictionaries from text in given file.
    :param file_name: file to read from
    :return: unigram dictionary, bigram dictionary - dictionary contains unigram/bigram and count indicating number of
                occurrences in given file.
    """

    # Read from given file
    with open(file_name, 'r', encoding="utf8") as f:
        raw_text = f.read()

    # Remove newlines
    raw_text = raw_text.replace("\n", " ")

    # Tokenize text
    tokens = word_tokenize(raw_text)

    # Create unigrams list
    unigrams_list = tokens

    # Create bigrams list
    bigrams_list = list(ngrams(tokens, 2))

    # Create unigram dictionary
    unigram_dict = {t: unigrams_list.count(t) for t in set(unigrams_list)}

    # Create bigram dictionary
    bigram_dict = {t: bigrams_list.count(t) for t in set(bigrams_list)}

    return unigram_dict, bigram_dict


if __name__ == "__main__":
    # Get unigram and bigram dictionaries of English, French, and Italian train data
    print("Create dictionaries start")
    unigram_dict_English, bigram_dict_English = create_dictionaries("data/LangId.train.English")
    unigram_dict_French, bigram_dict_French = create_dictionaries("data/LangId.train.French")
    unigram_dict_Italian, bigram_dict_Italian = create_dictionaries("data/LangId.train.Italian")
    print("Create dictionaries end")

    # Pickle all 6 dictionaries
    print("Pickle dictionaries start")
    with open("uni_english.pickle", 'wb') as handle:
        pickle.dump(unigram_dict_English, handle)

    with open("bi_english.pickle", 'wb') as handle:
        pickle.dump(bigram_dict_English, handle)

    with open("uni_french.pickle", 'wb') as handle:
        pickle.dump(unigram_dict_French, handle)

    with open("bi_french.pickle", 'wb') as handle:
        pickle.dump(bigram_dict_French, handle)

    with open("uni_italian.pickle", 'wb') as handle:
        pickle.dump(unigram_dict_Italian, handle)

    with open("bi_italian.pickle", 'wb') as handle:
        pickle.dump(bigram_dict_Italian, handle)
    print("Pickle dictionaries end")

    # Save dictionaries to file
    print("Save dictionaries to file start")
    with open("unigram dictionary english.txt", 'w') as file:
        file.write(str(unigram_dict_English))

    with open("bigram dictionary english.txt", 'w') as file:
        file.write(str(bigram_dict_English))

    with open("unigram dictionary french.txt", 'w') as file:
        file.write(str(unigram_dict_French))

    with open("bigram dictionary french.txt", 'w') as file:
        file.write(str(bigram_dict_French))

    with open("unigram dictionary italian.txt", 'w') as file:
        file.write(str(unigram_dict_Italian))

    with open("bigram dictionary italian.txt", 'w') as file:
        file.write(str(bigram_dict_Italian))
    print("Save dictionaries to file end")
