import codecs
import os

from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize
import re
import stopwords
import string
# noinspection PyUnresolvedReferences
import db_methods as db

additionally_ignored = ['x', '×', '–', '•', '©', '--']  # ignore like stopwords

def get_text_preprocessed(text):
    # Tokenization
    tokenized_text = word_tokenize(text)

    # To lower case
    for idx, word in enumerate(tokenized_text):
        tokenized_text[idx] = word.lower()

    # Stopwords removal
    tokens_no_sw = [word for word in tokenized_text if not word in stopwords.stop_words_slovene and not word in additionally_ignored]
    # Remove strings that contain number
    tokens_no_sw = [word for word in tokens_no_sw if not bool(re.search(r'\d', word))]

    # Remove punctuation
    tokens_no_punct = [s for s in tokens_no_sw if s not in string.punctuation]

    return tokens_no_punct


def get_indices(text_preprocesed, page_html):
    indices = []
    for word in text_preprocesed:
        regular_ex = rf"\b{word}\b"
        is_in_document = re.search(regular_ex, page_html, flags=re.IGNORECASE)
        if is_in_document:
            ind_of_word = []
            for match in re.finditer(regular_ex, page_html, flags=re.IGNORECASE):
                num_ind = match.start()
                ind_of_word.append(num_ind)
            indices.append(ind_of_word)
        else:
            indices.append("ERROR: " + word)
            print("Word not found:", word)

    return indices


def write_to_database(words, indices, domain, filename):
    print("WRITING TO DATABASE: ", filename, ", ", str(len(words)) ," words")
    # INSERT IN IndexWord table
    for word in words:
        db.insert_IndexWord(word)

    # TODO: INSERT IN posting table (word, filename, indices...)
    return


def website_indexing(page_html, domain, filename):
    soup = BeautifulSoup(page_html, features="html.parser")
    desired_tag = soup.find("link")

    # kill all script and style elements
    for element in soup(["script", "style"]):
        element.extract()

    # kill all comment tags
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Get text as combined string from body tag
    text_data = soup.body.get_text(separator=' ')

    # Preprocess text (tokenize, e.g.)
    text_preprocesed = get_text_preprocessed(text_data)
    print(text_preprocesed)

    # Find indices of words
    # MAYBE WE NEED TO DELETE SCRIPT TAGS FROM HTML STRING IN WHICH WE FIND INDICES
    indices = get_indices(text_preprocesed, page_html)

    # Write words into database
    write_to_database(text_preprocesed, indices, domain, filename)

    return


def main():
    domains = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]

    # Delete database
    db.delete_IndexWord()

    i = 1
    for domain in domains:
        if i == 1:  # Temporary
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webpages-data', domain)
            # Loop through files in directory
            for root, dirs, files in sorted(os.walk(path, topdown=True)):
                for name in files:
                    if name.endswith('.html') and i == 1:
                        filepath_full = os.path.join(root, name)
                        i += 1  # Temporary
                        f = codecs.open(filepath_full, 'r', encoding='utf-8')
                        page_html = f.read()
                        website_indexing(page_html, domain, name)

    # Close connection database
    db.close_connection()

if __name__ == "__main__":
    main()

