
from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import stopwords
import db_methods as db
import os
import codecs
import time

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

    return

def search(input_query):
    query_processed = get_query_preprocessed(input_query)
    print()
    print("Results for a query: \""+input_query+"\"")
    query_tup = tuple(query_processed)

    t1 = time.time()
    result = db.search_Postings(query_tup)
    t2 = time.time()

    print("Results found in " + str(round((t2-t1)*1000, 10)) + "ms.")
    output_result(result)
    return


def main():
    queries = [ "predelovalne dejavnosti", "trgovina", "social services", "hackaton", "izredni študent", "vzdrževanje stiskalnic za iverne plošče"]
    #print('Search: ', end=" ")
    #query = input()
    # query = "SPOT Sistem informacije"


    # Change demanded queries
    query = queries[5]

    search(query)

if __name__ == "__main__":
    main()
