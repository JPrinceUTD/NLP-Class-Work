# Portfolio Chapter 5 - Word Guessing Game
# By Jibin Prince

# Imports
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


def preprocess(text):
    """
    Preprocesses given text
    :param text: Raw text
    :return:
        1. tokens - non-unique tokens from given text
        2. nouns - unique lemmas from given text that are nouns
    """

    # Tokenize text
    tokens = word_tokenize(text)

    # Lowercase and remove non alpha
    tokens = [t.lower() for t in tokens if t.isalpha()]

    # Remove stop words and keep only words that are longer than 5 characters
    tokens = [t for t in tokens if t not in stopwords.words("english") and len(t) > 5]
    print("Number of tokens:", len(tokens))

    # Calculate lexical diversity
    print("Lexical diversity: %.2f" % (len(set(tokens)) / len(tokens)))

    # Get unique lemmas from text
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))

    # POS tag unique lemmas
    tags = nltk.pos_tag(lemmas_unique)
    print("First 20 unique lemmas tagged:", tags[:20])

    # Keep list of unique lemmas that are nouns
    is_noun = lambda pos: pos[:2] == "NN"
    nouns = [word for (word, pos) in tags if is_noun(pos)]
    print("Number of nouns:", len(nouns))

    print("")
    return tokens, nouns


def guessing_game(word_list):
    """
    This function simulates a word guessing game similar to hangman.
    :param word_list: given word list
    :return: none
    """

    user_score = 5

    # Select a random word from given list
    word_to_guess = str(word_list[randint(0, 49)])
    guessed_list = []

    print("\nLet's play a word guessing game!")

    guess_attempt = "".join(c if c in guessed_list else '_' for c in word_to_guess)
    guess = ""
    while word_to_guess != guess_attempt and user_score >= 0 and guess != "!":
        print(guess_attempt)
        guess = input("Guess a letter: ")
        if guess.lower() in word_to_guess:
            guessed_list.append(str(guess.lower()))
            guess_attempt = "".join(c if c in guessed_list else '_' for c in word_to_guess)
            user_score += 1
            print("Right! Score is", user_score)
        else:
            if guess != "!":
                user_score -= 1
                if user_score >= 0:
                    print("Sorry, guess again! Score is", user_score)

    if word_to_guess == guess_attempt:
        print(guess_attempt)
        print("You solved it!")

    while user_score >= 0 and guess != "!":
        word_to_guess = str(word_list[randint(0, 49)])
        guessed_list = []

        print("\nGuess another word")

        guess_attempt = "".join(c if c in guessed_list else '_' for c in word_to_guess)
        guess = ""
        while word_to_guess != guess_attempt and user_score >= 0 and guess != "!":
            print(guess_attempt)
            guess = input("Guess a letter: ")
            if guess.lower() in word_to_guess:
                guessed_list.append(str(guess.lower()))
                guess_attempt = "".join(c if c in guessed_list else '_' for c in word_to_guess)
                user_score += 1
                print("Right! Score is", user_score)
            else:
                if guess != "!":
                    user_score -= 1
                    if user_score >= 0:
                        print("Sorry, guess again! Score is", user_score)

        if word_to_guess == guess_attempt:
            print(guess_attempt)
            print("You solved it!")

    print("Current score:", user_score)


if __name__ == "__main__":
    """
        When executing this program, a filename must be passed in
        as a command-line argument.
    """

    # Check if filename has been passed in
    if len(sys.argv) <= 1:
        sys.exit("File name was not provided!")

    # Read input file as raw text
    inputFile = sys.argv[1]
    with open(inputFile, 'r') as f:
        inputText = f.read()

    # Preprocess raw text
    tokens, nouns = preprocess(inputText)

    # Create dictionary of noun and count of noun in tokens
    noun_dictionary = {n: tokens.count(n) for n in nouns}

    # Sort noun dictionary by noun count descending
    sorted_noun_dictionary = sorted(noun_dictionary.items(), key=lambda x: x[1], reverse=True)

    # Print 50 most common words for dictionary and store them in a list for guessing game
    guessing_game_words_list = []
    print("50 most common words:")
    for i in range(50):
        print(sorted_noun_dictionary[i])
        guessing_game_words_list.append(sorted_noun_dictionary[i][0])

    # Run guessing game
    guessing_game(guessing_game_words_list)
