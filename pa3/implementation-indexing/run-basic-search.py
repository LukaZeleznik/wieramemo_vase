from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re
import stopwords
import string
import os
import codecs
from bs4 import BeautifulSoup, Comment

additionally_ignored = ['x', '×', '–', '•', '©', '--']  # ignore like stopwords

def get_query_preprocessed(text):
    # Tokenization
    tokenized_text = word_tokenize(text)

    # To lower case
    for idx, word in enumerate(tokenized_text):
        tokenized_text[idx] = word.lower()  # Lower case

    # Stopwords removal
    tokens_no_sw = [word for word in tokenized_text if not word in stopwords.stop_words_slovene]

    return tokens_no_sw

def open_file(filename):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webpages-data', filename)
        f = codecs.open(path, 'r', encoding='utf-8')
        page_html = f.read()
        return page_html
    except IOError:
        print("Error: File does not appear to exist.")
        return None

def get_snipet(doc, freq, indexes):
    indexes = indexes.split(",") # to list
    indexes = [int(s) for s in indexes] # to int list
    snipet = ''

    # OPEN FILE
    page_html = open_file(doc)

    if page_html:
        soup = BeautifulSoup(page_html, features="html.parser")

        # kill all script and style elements
        for element in soup(["script", "style"]):
            element.extract()

        # kill all comment tags
        for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Get while HTML text as combined string from body tag
        text_data = soup.body.get_text(separator=' ')
        tokenized_text = word_tokenize(text_data)

        # For every repetition in tekst, create a snipet
        for idx in indexes:
            # CREATE -/+ 3 NEIGHBOURHOOD of word
            neighbourhood = []
            for neighbour_idx in range(idx-3, idx+4):
                if neighbour_idx>=0 and neighbour_idx<len(tokenized_text):
                    neighbourhood.append(tokenized_text[neighbour_idx])

            # Add to snipets string
            neighbourhood_str = " ".join(neighbourhood)
            snipet = snipet + neighbourhood_str
            # ...
            if idx != indexes[-1]:
                snipet = snipet + ' ... '
        return snipet
    else:
        return 'Error'

def output_result(result):
    #for row in result:
    #    print(f"\tHits: {row[1]}\n\t\tDoc: '{row[0]}'\n\t\tIndexes: {row[2]}")

    print('-' * 120)
    print(f"{'Frequencies':<15}{'Document':<45}{'Snippet':<50}")
    print(f"{'-' * 13:<15}{'-' * 43:<45}{'-' * 60:<60}")

    for row in result:
        snipet = get_snipet(row[0], row[1], row[2])
        print(f"{row[1]:<15}{row[0]:<45}{snipet:<60}")

def get_text_preprocessed(text):
    # Tokenization
    tokenized_text = word_tokenize(text)

    # To lower case
    for idx, word in enumerate(tokenized_text):
        tokenized_text[idx] = (word.lower(), idx)   # INDICES !!!

    # Stopwords removal
    tokens_no_sw = [word for word in tokenized_text if not word[0] in stopwords.stop_words_slovene and not word[0] in additionally_ignored]
    # Remove strings that contain number
    tokens_no_sw = [word for word in tokens_no_sw if not bool(re.search(r'\d', word[0]))]

    # Remove punctuation
    tokens_no_punct = [s for s in tokens_no_sw if s[0] not in string.punctuation]
    # Tokens might have symbols (e.g. etn_prava) --> maybe split it?

    return tokens_no_punct

def get_preprocesed_text(page_html):
    soup = BeautifulSoup(page_html, features="html.parser")

    # kill all script and style elements
    for element in soup(["script", "style"]):
        element.extract()

    # kill all comment tags
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Get text as combined string from body tag
    text_data = soup.body.get_text(separator=' ')

    # Preprocess text (tokenize, e.g.)
    text_preprocesed = get_text_preprocessed(text_data)   # RESULT: [('word1', idx1), ('word2', idx2), ...]

def search_postings(query):
    domains = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]

    i = 1
    for domain in domains:
        if i == 1 or i == 2:  # Temporary
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webpages-data', domain)
            # Loop through files in directory
            for root, dirs, files in sorted(os.walk(path, topdown=True)):
                for name in files:
                    if name.endswith('.html') and (i == 1 or i == 2):
                        filepath_full = os.path.join(root, name)
                        print(filepath_full)
                        i += 1  # Temporary
                        f = codecs.open(filepath_full, 'r', encoding='utf-8')
                        page_html = f.read()
                        get_preprocesed_text(page_html)


def search(input_query):
    query_processed = get_query_preprocessed(input_query)
    print()
    print("query: ",query_processed)
    query_tup = tuple(query_processed)

    result = search_postings(query_tup)
    output_result(result)

def main():
    print('Search: ', end=" ")
    #query = input()
    query = 'Sistem SPOT'
    search(query)

if __name__ == "__main__":
    main()