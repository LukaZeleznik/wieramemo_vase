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
        tokenized_text[idx] = (word.lower(), idx)   # INDICES !!!

    # Stopwords removal
    tokens_no_sw = [word for word in tokenized_text if not word[0] in stopwords.stop_words_slovene and not word[0] in additionally_ignored]
    # Remove strings that contain number
    tokens_no_sw = [word for word in tokens_no_sw if not bool(re.search(r'\d', word[0]))]

    # Remove punctuation
    tokens_no_punct = [s for s in tokens_no_sw if s[0] not in string.punctuation]
    # Tokens might have symbols (e.g. etn_prava) --> maybe split it?

    return tokens_no_punct


def get_repetitions_word_postings(word_postings, word):
    for item in word_postings:
        if word == item[0]:
            return item
    #a =[item for item in word_postings if words[i] == item[0]]
    return None

def write_to_database(words, domain, filename):

    # PRE-PROCESS FOR POSTINGS TABLE (frequencies of words, count repetitions)
    word_postings = [] # List of sets with non-duplicated words and counted repetition (freq)
    for i in range(len(words)):
        item_word_postings = get_repetitions_word_postings(word_postings, words[i][0])
        if not item_word_postings:
            word_postings.append([words[i][0], [str(words[i][1])]])   # [['uporablja', [2]], ['piškotke', [3]], ...]
        else:
            # Word already exists, add index of repetition to array (increase freq.)
            item_word_postings[1].append(str(words[i][1]))

    print("WRITING TO DATABASE: ",filename+", ", str(len(words)), " words, ", str(len(word_postings)), " unique words",)

    for posting in word_postings:
        word = posting[0]
        # INSERT IN IndexWord table
        db.insert_IndexWord(word)
        #print(db.insert_IndexWord(word))

        # INSERT IN Posting table(word, filename, indices...) e.g.: (‘davek’, ‘evem.gov.si/evem.gov.si.4.html’, 3,
        # ‘2,34,894’)
        db.insert_Posting(word, domain+"/"+filename, len(posting[1]), ",".join(posting[1]))
    print("FINISHED WRITING TO DATABASE.")
    return


def website_indexing(page_html, domain, filename):
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

    # Write words into database
    write_to_database(text_preprocesed, domain, filename)

    return


def main():
    domains = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]

    # Delete database
    db.delete_IndexWord()
    db.delete_Posting()

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
                        website_indexing(page_html, domain, name)

    # Close connection database
    db.close_connection()

if __name__ == "__main__":
    main()

