# Portfolio Web Crawler
# By Jibin Prince

# Imports
from bs4 import BeautifulSoup
import requests
import re
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def get_relevant_urls(web_url):
    """
    Gets relevant URLs from given URL. Function is tailored to the Golf.com site.
    :param web_url: website link
    :return: list of https URLs
    """

    # Get HTML from URL
    response = requests.get(web_url)
    html_text = response.text

    # Get list of URLs
    soup = BeautifulSoup(html_text, "html.parser")
    url_list_relevant = [link.get('href') for link in
                         soup.find_all('a', attrs={'href': re.compile("https://golf.com")})]

    return list(set(url_list_relevant))


def scrape_text_from_url(web_url_list):
    """
    Scrape text from given list of URLs and save to text files
    :param web_url_list: List of scraped URLs
    :return: list of text files containing scraped text
    """

    file_list = []
    file_counter = 0
    for url_item in web_url_list:
        # Extract text and title from given URL
        page = requests.get(url_item)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.get_text()
        txt_file_name = os.path.join("Scraped Text Files", "page-" + str(file_counter) + ".txt")

        # Delete file if file name exists
        if os.path.exists(txt_file_name):
            os.remove(txt_file_name)

        # Write text to a text file
        with open(txt_file_name, 'w', encoding="utf-8") as f:
            f.write(text)

        file_list.append(txt_file_name)
        file_counter += 1

    return file_list


def text_to_sentences(txt_file_name):
    """
    Gets list of sentences from given text file
    :param txt_file_name: name of text file containing scraped text
    :return: list of sentences from text file after preprocessing
    """

    # Read text from file
    with open(txt_file_name, 'r', encoding="utf-8") as f:
        contents = f.read()

    # Remove newlines and tabs from text
    new_contents_str = contents.replace("\n", " ").replace("\t", "")

    # Get list of sentences from text
    sentences_list = sent_tokenize(new_contents_str.strip())

    txt_file_name = txt_file_name.replace("Scraped Text Files", "Cleaned Text Files")

    # Delete file if file name exists
    if os.path.exists(txt_file_name):
        os.remove(txt_file_name)

    # Write text to a text file
    with open(txt_file_name, 'w', encoding="utf-8") as f:
        for sentence in sentences_list:
            f.write(sentence + "\n")

    return sentences_list


def extract_important_terms(sent_list):
    """
    Prints top 40 terms from given list of sentences
    :param sent_list: List of sentences
    :return: None
    """

    # Convert list of sentences into tokens
    tokens = []
    for sentence in sent_list:
        tokens += word_tokenize(sentence)

    # Lowercase and remove non alpha
    tokens = [t.lower() for t in tokens if t.isalpha() and len(t) > 1]

    # Remove stop words
    tokens = [t for t in tokens if t not in stopwords.words("english")]

    # Create dictionary of words with count
    word_count = {}
    for word in tokens:
        if word not in word_count:
            word_count[word] = 1
        elif word in word_count:
            word_count[word] += 1

    # Sort word dictionary by count descending
    sorted_word_dictionary = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    print("Top 40 terms:")
    for i in range(40):
        print(sorted_word_dictionary[i][0])


def build_knowledge_base(top_terms_list, sent_list):
    """
    Creates knowledge base dictionary of the given top 10 terms
    :param top_terms_list: List of the top 10 terms (manually decided)
    :param sent_list: List of sentences
    :return: None
    """

    knowledge_base = dict.fromkeys(top_terms_list, [])
    for term in top_terms_list:
        for sentence in sent_list:
            if term in sentence:
                knowledge_base[term].append(sentence)
        if os.path.exists(os.path.join("Knowledge Base", term + ".txt")):
            os.remove(os.path.join("Knowledge Base", term + ".txt"))
        with open(os.path.join("Knowledge Base", term + ".txt"), 'w', encoding="utf-8") as f:
            f.write(str(knowledge_base[term]))


if __name__ == "__main__":
    url = "https://golf.com/"

    # Get list of relevant URLs
    print("Get relevant URLs start")
    url_list = get_relevant_urls(url)
    print("Get relevant URLs end\n")

    # Scrape of all text in each URL
    print("Scraping text from URLs start")
    scraped_text_files_list = scrape_text_from_url(url_list)
    print("Scraping text from URLs end\n")

    # Convert text from each scraped text file into sentences
    list_of_sentences = []
    print("Convert text into sentences start")
    for text_file in scraped_text_files_list:
        list_of_sentences += text_to_sentences(text_file)
    print("Convert text into sentences end\n")

    # Extract important terms from cleaned text files
    print("Extract important terms start")
    extract_important_terms(list_of_sentences)
    print("Extract important terms end\n")

    # Build knowledge base of top 10 domain-relevant terms
    print("Build knowledge base start")
    top_terms = ["golf", "gear", "instruction", "bags", "woods", "clubs", "swing", "game", "tour", "drivers"]
    build_knowledge_base(top_terms, list_of_sentences)
    print("Build knowledge base end")
