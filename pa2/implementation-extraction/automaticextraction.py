import re, os, sys, codecs
from bs4 import BeautifulSoup, NavigableString
import difflib as dl

self_closing_tags = ["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr",]

def cleanup_html(soup):
    #soup.head.decompose()  # remove head
    #for script in soup.body.find_all('script'):
    #    script.decompose()  # remove all script tags
    return soup.prettify()


def build_DOM_tree(text):
    # 1: cleanup html tags, enclose open tags...
    clean_html = cleanup_html(BeautifulSoup(text, "lxml"))

    # 2. build tree
    tree = BeautifulSoup(clean_html, "lxml")

    return tree


wrap_gl = ""
def construct_tag_list(source, path):
    global wrap_gl;

    # HERE TAG IS OPENED
    path.append(source.name)

    # TAG DOES NOT HAVE LOWER LEVELS
    if not source.find_all(recursive=False):
        # leaf node, backtrack, close tag...
        if source.name not in self_closing_tags:
            path.append("/" + source.name)
            pass
        return path

    # FOR EVERY TAGS CHILD
    for child1 in source.children:
        if not isinstance(child1, NavigableString):
            path = construct_tag_list(child1, path)

    # HERE TAG IS CLOSED
    if source.name not in self_closing_tags:
        path.append("/" + source.name)
        pass
    return path

def compare_tag_lists(list1, list2):
    # Indices list of matching element from other list
    # Using loop + count()
    res = []
    i = 0
    j = 0
    for tag in list1:
        if list1[i] == list2[j]:
            res.append(i)
            print(list1[i], "  ",list2[j])
        else:
            # TAG MISMATCH, find closing tag
            print(list1[i], "  ", list2[j], " M")
            catch=j
            while list2[catch] != (list1[i]):
                print(list2[catch], " ",catch)
                catch += 1
            j=catch

        i += 1
        j += 1

    print("The matching element Indices list : " + str(res))

    return

def roadrunner(text1, text2):
    # Site 1 is set as reg. expression wrapper. Update and generalize it by using the second (third, fourth,...) one.
    tree1 = build_DOM_tree(text1)
    tree2 = build_DOM_tree(text2)

    # Here you construct regex from first trees
    tag_list1 = construct_tag_list(tree1.body, [])
    print(tag_list1)
    tag_list2 = construct_tag_list(tree2.body, [])
    print(tag_list2)

    compare_tag_lists(tag_list1, tag_list2)
    return


def main():
    ### Temporary
    f1 = codecs.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'input-extraction', 'overstock.com', 'jewelry01.html'),
        'r',  encoding='iso-8859-1')
    f2 = codecs.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'input-extraction', 'overstock.com',
                     'jewelry02.html'),
        'r',  encoding='iso-8859-1')
    text1 = f1.read()
    text2 = f2.read()

    # Result is a union-free regular expression
    result_regex = roadrunner(text1, text2)


if __name__ == "__main__":
    main()
