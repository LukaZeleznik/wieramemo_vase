import re, os, sys, codecs
from bs4 import BeautifulSoup
import difflib as dl

self_closing_tags = ["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr",]

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


wrap_gl = ""
def construct_wrapper(graph, source, path= []):
    global wrap_gl;

    path.append(source)
    print("<"+source.name+ ">")
    wrap_gl += "<" + source.name + ".*?>\s*"
    if len(source.find_all(recursive=False)) == 0:
        # leaf node, backtrack, end
        # not all tags have enclosing tag...
        if source.name not in self_closing_tags:
            print("</" + source.name + ">")
            wrap_gl += "</.*?" + source.name + ">\s*"
        return path

    for neighbour in source.find_all(recursive=False):
        path = construct_wrapper(graph, neighbour, path )

    if source.name not in self_closing_tags:
        print("</"+ source.name+ ">")
        wrap_gl += "</.*?" + source.name + ">\s*"
    return path


def roadrunner(text1, text2):
    # Site 1 is set as reg. expression wrapper. Update and generalize it by using the second (third, fourth,...) one.
    tree1 = build_DOM_tree(text1)
    tree2 = build_DOM_tree(text2)

    # Here you construct regex from first trees
    wr = construct_wrapper(tree1, tree1.html, [])
    print(wrap_gl)

    return wr


def main():
    ### Temporary
    f1 = codecs.open("..\input-extraction\overstock.com\jewelry01.html", 'r');
    f2 = codecs.open("..\input-extraction\overstock.com\jewelry02.html", 'r');
    text1 = f1.read()
    text2 = f2.read()

    # Result is a union-free regular expression
    result_regex = roadrunner(text1, text2)


if __name__ == "__main__":
    main()
