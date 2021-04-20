import codecs
from lxml import html
import re

def extract_with_xpath_overstock(page_html):

    title = list_price = price = saving = saving_percent = content = ""

    document_tree = html.fromstring(page_html)

    titles = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/a/b/text()')
    print("titles: (", len(titles), ")")
    for title in titles:
        print("\t", title)

    list_prices = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()')

    print("list prices: (", len(list_prices), ")")
    for list_price in list_prices:
        print("\t", list_price)

    prices = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()')

    print("prices: (", len(prices), ")")
    for price in prices:
        print("\t", price)


    savings_and_savings_percents = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()')

    print("savings: (", len(savings_and_savings_percents), ")")
    for savings_and_saving_percent in savings_and_savings_percents:

        saving = re.findall("^\S*", savings_and_saving_percent)
        saving_percent = re.findall("\((.*?)\)", savings_and_saving_percent)

        print("\t", saving[0], "---", saving_percent[0])


    contents = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[2]')
    contents = [content.text_content() for content in contents]

    print("contents: (", len(contents), ")")
    for content in contents:


        print("\t", content)

    return ""

def extract_with_xpath_rtv(page_html):

    author = published_time = title = sub_title = lead = content = ""

    document_tree = html.fromstring(page_html)

    author = document_tree.xpath('//div[@class="author-timestamp"]/strong/text()')
    print("author:", author[0])

    title = document_tree.xpath('//header[@class="article-header"]/h1/text()')
    print("title:", title[0])

    published_time = document_tree.xpath('//div[@class="author-timestamp"]/text()')
    print("published time:", published_time[1].strip("| "))

    sub_title = document_tree.xpath('//div[@class="subtitle"]/text()')
    print("sub title:", sub_title[0])

    lead = document_tree.xpath('//p[@class="lead"]/text()')
    print("lead:", lead[0])

    content = document_tree.xpath('//article[@class="article"]/p')
    content = [p.text_content() for p in content]
    separator = " "
    print("content: ", separator.join(content))

    return ""


if __name__ == "__main__":
    # f = codecs.open("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", 'r')
    f = codecs.open("../input-extraction/overstock.com/jewelry01.html", 'r')
    page_html = f.read()
    # extracted_data = extract_with_xpath_rtv(page_html)
    extracted_data = extract_with_xpath_overstock(page_html)
    # print(extracted_data)