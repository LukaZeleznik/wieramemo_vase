import re, os, sys, codecs
from bs4 import BeautifulSoup
import difflib as dl


def cleanup_html(soup):
    soup.head.decompose()  # remove head
    for script in soup.body.find_all('script'):
        script.decompose()  # remove all script tags
    return soup.prettify()


def build_DOM_tree(text):
    # 1: cleanup html tags, enclose open tags...
    clean_html = cleanup_html(BeautifulSoup(text, "lxml"))

    # 2. build tree
    tree = BeautifulSoup(clean_html, "lxml")

    return tree


visited1 = []  # List to keep track of visited nodes.
queue1 = []  # Initialize a queue
visited2 = []  # List to keep track of visited nodes.
queue2 = []  # Initialize a queue


# https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
def bfs(startnode1, startnode2):
    visited1.append(startnode1)
    queue1.append(startnode1)
    visited2.append(startnode2)
    queue2.append(startnode2)

    while (len(queue1) != 0) or (len(queue2) != 0):
        if len(queue1) > 0:
            s1 = queue1.pop(0)
            print("1. ", s1.name, end=' ')
            for neighbour in s1.find_all(recursive=False):
                if neighbour not in visited1:  # might cause problems?
                    visited1.append(neighbour)
                    queue1.append(neighbour)
        if len(queue2) > 0:
            s2 = queue2.pop(0)
            print("2. ", s2.name, end=' ')
            for neighbour in s2.find_all(recursive=False):
                if neighbour not in visited2:  # might cause problems?
                    visited2.append(neighbour)
                    queue2.append(neighbour)
        print();

        # TODO: ALIGN TREES, compare tags and strings mismaches, add strings to tree...

        return;


def roadrunner(text1, text2):
    # Site 1 is set as reg. expression wrapper. Update and generalize it by using the second (third, fourth,...) one.
    tree1 = build_DOM_tree(text1);
    tree2 = build_DOM_tree(text2);
    wrapper = '^[\s\S]*<body[^\>]*>([\s\S]*)<\/body>[\s\S]*$'

    # TODO: dynamically construct wrapper from tree1?
    print(re.match(wrapper, tree1.prettify()))

    # Here you iterate through trees
    bfs(tree1.html, tree2.html)

    return wrapper


def main():
    ### Temporary
    f1 = codecs.open("..\input-extraction\overstock.com\jewelry01.html", 'r');
    f2 = codecs.open("..\input-extraction\overstock.com\jewelry02.html", 'r');
    text1 = f1.read()
    text2 = f2.read()

    # Result is a union-free regular expression
    result_regex = roadrunner(text1, text2)
    print(result_regex)


if __name__ == "__main__":
    main()
