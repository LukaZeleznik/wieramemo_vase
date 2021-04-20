import codecs
from lxml import html

def extract_with_xpath(page_html):

    # title = listPrice = price = saving = savingPercent = content = ""
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
    f = codecs.open("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", 'r')
    page_html = f.read()
    extracted_data = extract_with_xpath(page_html)
    #print(extracted_data)