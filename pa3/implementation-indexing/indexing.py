import codecs
import os

from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize
import nltk
import stopwords

def get_text_preprocessed(text):

    # Tokenization
    tokenized_text = word_tokenize(text)

    # Stopwords removal
    tokens_without_sw = [word for word in tokenized_text if not word in stopwords.stop_words_slovene]
    print(tokens_without_sw)

    # To lower case
    for idx, word in enumerate(tokens_without_sw):
        tokens_without_sw[idx] = word.lower()

    print(tokens_without_sw)
    # todo: remove punctuation
    return text

def website_processing(page_html):
    soup = BeautifulSoup(page_html, features="html.parser")

    # kill all script and style elements
    for element in soup(["script", "style"]):
        element.extract()

    # kill all comment tags
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Get text as combined string from body tag
    text = soup.body.get_text()

    # todo: get indices from html documents for every word...
    text_preprocesed = get_text_preprocessed(text)

    return

def main():
    domains = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]

    i=1
    for domain in domains:
        if i == 1: # Temporary
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webpages-data', domain)
            # Loop through files in directory
            for root, dirs, files in sorted(os.walk(path, topdown=True)):
                for name in files:
                    if name.endswith('.html') and i==1:
                        name = os.path.join(root, name)
                        print('READING: ', name)
                        f = codecs.open(name, 'r', encoding='utf-8')
                        page_html = f.read()
                        website_processing(page_html)
                        i += 1  # Temporary


if __name__ == "__main__":
    main()