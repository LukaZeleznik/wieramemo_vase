import re, os, sys, codecs
from bs4 import BeautifulSoup, NavigableString, Comment
import difflib as dl

self_closing_tags = ["area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"]
ignore_tags = ["b", "script", "br", "em", "hr"]

def cleanup_html(soup):
    for script in soup.body.find_all('script'):
        script.decompose()  # remove all script tags
    return soup.prettify()


def build_DOM_tree(text):
    # 1: cleanup html tags, enclose open tags...
    clean_html = cleanup_html(BeautifulSoup(text, "lxml"))

    # 2. build tree
    tree = BeautifulSoup(clean_html, "lxml")

    return tree

def get_repeating_tag(tag_name, items_list, current_idx):
    num_of_opening_tags = 1
    repeating_part = [items_list[current_idx][1].name]
    while num_of_opening_tags >0 and current_idx < len(items_list) - 1:
        current_idx = current_idx + 1
        next_item = items_list[current_idx][1]
        tag = items_list[current_idx][0]  # < or /
        # is td=tr?
        if next_item.name == tag_name:
            #another open <tr>
            if tag == "<":
                num_of_opening_tags += 1
            else:
                num_of_opening_tags -= 1
        repeating_part.append(tag + next_item.name)
    return repeating_part, current_idx


# Recursive function that builds list from tree, maybe not the best solution, as we later find out...

def construct_tag_list(source, path):

    # HERE TAG IS OPENED
    if source.name not in ignore_tags:
        path.append(("<", source))

    # TAG DOES NOT HAVE LOWER LEVELS
    if not source.find_all(recursive=False):
        # leaf node, backtrack, close tag...
        if source.name not in self_closing_tags and source.name not in ignore_tags:
            path.append(("</", source))
            pass
        return path

    # FOR EVERY TAGS CHILD
    for child1 in source.children:
        if not isinstance(child1, NavigableString):
            path = construct_tag_list(child1, path)

    # HERE TAG IS CLOSED
    if source.name not in self_closing_tags and source.name not in ignore_tags:
        path.append(("</", source))
        pass
    return path

def check_tags_text(tag1, tag2):
    if tag1.name in ignore_tags or tag2.name in ignore_tags: return
    text_tags1 = tag1.findAll(text=True, recursive=False)
    text_tags2 = tag2.findAll(text=True, recursive=False)
    text1_list = []
    text2_list = []
    # Tried with regex but failed, ALSO stripped_strings exists :/
    for a in text_tags1:
        # Ignore comment tags text
        if not isinstance(a, Comment) and len(a.strip())>0:
            text1_list.append(a.strip())
    for a in text_tags2:
        if not isinstance(a, Comment) and len(a.strip())>0:
            text2_list.append(a.strip())
    if text1_list==text2_list:
        for i in text1_list: print(i , end = "  ")
    else:
        print("#TEXT" , end = "  ")

    return

def compare_tag_lists(list1, list2):
    """lists of tuples ('<', tag)"""
    print("<html>  <head>  </head>", end = "  ")
    # Indices list of matching element from other list
    i = 0
    j = 0
    while i < len(list1) and j<len(list2):
        tag1=list1[i][1] # Tag is second element in tuple, stupid
        tag2=list2[j][1]
        if tag1.name == tag2.name:
            # TAG MATCH
            #print(list1[i][0], tag1.name, "  ", list2[j][0],tag2.name)
            print(list1[i][0] + tag1.name + ">", end = "  ") # opening tag, print to output

            #IF TAGS MATCH CHECK THEIR TEXT
            if list1[i][0] != "</": check_tags_text(tag1, tag2)

        else:
            # TAG MISMATCH, find closing tag
            prev_tag_name_list1 = get_previous_tag_name(list1, i)
            prev_tag_name_list2 = get_previous_tag_name(list2, j)

            #print(list1[i], "  ", list2[j], " MISMATCHTAG", " prev1: ", prev_tag_name_list1)

            # check if repeating : in WRAPPER - LIST GOES ON, e.g. <tr> (and sample has </tbody>)
            if tag1.name == prev_tag_name_list1:
                # wrapper iterator?
                square_candidate, new_idx = get_repeating_tag(
                    prev_tag_name_list1, list1, i)
                i = new_idx + 1
                print("(<", end = "")
                for n in square_candidate:
                    if n[0] == "</": print ("<"+n+">", end = "")
                    else: print (n+">", end = "")
                print(")?", end = "  ")
                continue

            # SAMPLE is repeating
            if tag2.name == prev_tag_name_list2:
                # sample iterator?
                square_candidate, new_idx = get_repeating_tag(
                    prev_tag_name_list2, list2, j)
                j = new_idx + 1
                print("(<", end="")
                for n in square_candidate:
                    if n[0] == "</":
                        print("<" + n + ">", end="")
                    else:
                        print(n + ">", end="")
                print(")?")
                continue

        i += 1
        j += 1
    print("</html>  ")
    return

def get_previous_tag_name(items_list, current_index):
    current_index -= 1
    tag = items_list[current_index][1].name
    return tag

def roadrunner(text1, text2):
    # Site 1 is set as reg. expression wrapper. Update and generalize it by using the second (third, fourth,...) one.
    tree1 = build_DOM_tree(text1)
    tree2 = build_DOM_tree(text2)

    # Here you construct regex from first trees
    tag_list1 = construct_tag_list(tree1.body, [])
    tag_list2 = construct_tag_list(tree2.body, [])

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
    roadrunner(text1, text2)


if __name__ == "__main__":
    main()
