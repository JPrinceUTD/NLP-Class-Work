import json
import random
import string
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Dropout


def create_patterns_and_tags_lists(data):
    words_list = []
    classes_list = []
    patterns = []
    tags = []

    # Extract words from patterns and its corresponding tags
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            # Tokenize each pattern
            tokens = nltk.word_tokenize(pattern)

            # Add tokens to patterns vocab
            words_list.extend(tokens)

            # Add to pattern list
            patterns.append(pattern)

            # Add corresponding tag to tag list
            tags.append(intent["tag"])

            # Add corresponding tag to tags vocab
            if intent["tag"] not in classes_list:
                classes_list.append(intent["tag"])

    # Lemmatize pattern vocabulary
    # Remove punctuation, convert words to lowercase
    lemmatizer = WordNetLemmatizer()
    words_list = [lemmatizer.lemmatize(word.lower()) for word in words_list if word not in string.punctuation]

    # Sort pattern and tag vocabulary and remove duplicates
    words_list = sorted(set(words_list))
    classes_list = sorted(set(classes_list))

    return words_list, classes_list, patterns, tags


def create_train_model_data(words_list, classes_list, patterns, tags):
    training = []
    output_empty = [0] * len(classes_list)
    lemmatizer = WordNetLemmatizer()

    # Create bag of words model
    for index, document in enumerate(patterns):
        bag_of_words = []
        text = lemmatizer.lemmatize(document.lower())
        for word in words_list:
            bag_of_words.append(1) if word in text else bag_of_words.append(0)

        # Mark the index of class that the current pattern is associated with
        output_row = list(output_empty)
        output_row[classes_list.index(tags[index])] = 1

        # Add bag of words list and associated class to training list
        training.append([bag_of_words, output_row])

    # Shuffle the training list and convert it to array
    random.shuffle(training)
    training = np.array(training, dtype=object)

    # Split training list into features and target labels
    features = np.array(list(training[:, 0]))
    target = np.array(list(training[:, 1]))

    return features, target


def lemmatize_input(text):
    tokens = nltk.word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens


def bag_of_words_input(text, vocab):
    tokens = lemmatize_input(text)
    bag_of_words = [0] * len(vocab)
    for word in tokens:
        for index, word_vocab in enumerate(vocab):
            if word_vocab == word:
                bag_of_words[index] = 1
    return np.array(bag_of_words)


def tag_prediction(trained_model, text, vocab, labels):
    bag_of_words = bag_of_words_input(text, vocab)
    result = trained_model.predict(np.array([bag_of_words]))[0]  # Get probabilities
    y_pred = [[index, res] for index, res in enumerate(result) if res > 0.5]
    y_pred.sort(key=lambda x: x[1], reverse=True)  # Sort probabilities in descending order
    return_list = []
    for res in y_pred:
        return_list.append(labels[res[0]])  # Add tags with the highest probabilities in descending order
    return return_list


def get_response(predicted_tags, json_intents):
    if len(predicted_tags) == 0:
        answer = "Sorry! I do not understand."
    else:
        tag = predicted_tags[0]
        intents_list = json_intents["intents"]
        for i in intents_list:
            if i["tag"] == tag:
                answer = random.choice(i["responses"])
                break
    return answer


if __name__ == "__main__":
    # Load intents dataset from intents JSON file
    with open('intents.json') as f:
        intents = json.load(f)

    # Create patterns and associated tags lists
    words, classes, pattern_list, tag_list = create_patterns_and_tags_lists(intents)

    # Create x and y data for the train model
    train_x, train_y = create_train_model_data(words, classes, pattern_list, tag_list)

    # Build neural network model
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x=train_x, y=train_y, epochs=150, verbose=1)

    # Initiate chatbot interaction
    name = str(input("\nWhat is your name? "))
    chat_history_file_name = "Chat History/" + name.lower() + ".txt"

    print("\nI am a chatbot that helps you understand skyscrapers. Type quit if you want to end this "
          "conversation. Type history if you want to see your chat history.\n")
    with open(chat_history_file_name, 'a', encoding='UTF-8') as f:
        f.write("Bot > I am a chatbot that helps you understand skyscrapers. Type quit if you want to end this "
                "conversation. Type history if you want to see your chat history.\n")
    while True:
        user_input = input("")
        with open(chat_history_file_name, 'a', encoding='UTF-8') as f:
            f.write(name + " > " + user_input + "\n")

        if user_input == "quit":
            print("You have successfully ended our conversation. Thank you for chatting with me.")
            with open(chat_history_file_name, 'a', encoding='UTF-8') as f:
                f.write("Bot > You have successfully ended our conversation. Thank you for chatting with me.\n")
            break
        elif user_input == "history":
            with open(chat_history_file_name, 'r', encoding='UTF-8') as f:
                for line in f:
                    print(line.rstrip())
        else:
            predicted_intents = tag_prediction(model, user_input, words, classes)
            result = get_response(predicted_intents, intents)

            print(result + "\n")
            with open(chat_history_file_name, 'a', encoding='UTF-8') as f:
                f.write("Bot > " + str(result) + "\n")