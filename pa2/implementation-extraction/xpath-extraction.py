import codecs
from lxml import html
import re
import json

def extract_with_xpath_overstock(page_html):

    # title = list_price = price = saving = saving_percent = content = ""

    document_tree = html.fromstring(page_html)

    titles = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/a/b/text()')
    titles = [" ".join(title.replace("\n", " ").split()) for title in titles]

    # print("titles: (", len(titles), ")")
    # for title in titles:
    #     print("\t", title)

    list_prices = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()')

    # print("list prices: (", len(list_prices), ")")
    # for list_price in list_prices:
    #     print("\t", list_price)

    prices = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()')

    # print("prices: (", len(prices), ")")
    # for price in prices:
    #     print("\t", price)


    savings_and_savings_percents = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()')
    savings = []
    savings_percents = []

    # print("savings: (", len(savings_and_savings_percents), ")")
    for savings_and_saving_percent in savings_and_savings_percents:

        saving = re.findall("^\S*", savings_and_saving_percent)[0]
        savings.append(saving)
        saving_percent = re.findall("\((.*?)\)", savings_and_saving_percent)[0]
        savings_percents.append(saving_percent)

        # print("\t", saving, "---", saving_percent)


    contents = document_tree.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[*]/td[2]/table/tbody/tr/td[2]')
    contents = [" ".join(content.text_content().replace("\n", " ").split()) for content in contents]

    # print("contents: (", len(contents), ")")
    # for content in contents:
    #     print("\t", content)

    data_records = []

    for title, list_price, price, saving, saving_percent, content in zip(titles, list_prices, prices, savings,
                                                                         savings_percents, contents):
        data_record = dict()
        data_record["Title"] = title
        data_record["ListPrice"] = list_price
        data_record["Price"] = price
        data_record["Saving"] = saving
        data_record["SavingPercent"] = saving_percent
        data_record["Content"] = content

        data_records.append(data_record)

    json_data_records = json.dumps(data_records, ensure_ascii=False)
    return json_data_records

def extract_with_xpath_rtv(page_html):

    # author = published_time = title = sub_title = lead = content = ""

    document_tree = html.fromstring(page_html)

    author = document_tree.xpath('//div[@class="author-timestamp"]/strong/text()')
    author = author[0]
    # print("author:", author)

    title = document_tree.xpath('//header[@class="article-header"]/h1/text()')
    title = title[0]
    # print("title:", title)

    published_time = document_tree.xpath('//div[@class="author-timestamp"]/text()')
    published_time = published_time[1].replace("|", "").replace("\t", "").replace("\n", "").strip()
    # print("published time:", published_time)

    sub_title = document_tree.xpath('//div[@class="subtitle"]/text()')
    sub_title = sub_title[0]
    # print("sub title:", sub_title)

    lead = document_tree.xpath('//p[@class="lead"]/text()')
    lead = lead[0]
    # print("lead:", lead)

    content = document_tree.xpath('//article[@class="article"]/p')
    content = [p.text_content() for p in content]
    separator = " "
    content = separator.join(content).strip()
    # print("content: ", content)

    data_record = dict()

    data_record["Author"] = author
    data_record["Title"] = title
    data_record["PublishedTime"] = published_time

    data_record["SubTitle"] = sub_title
    data_record["Lead"] = lead
    data_record["Content"] = content

    json_data_record = json.dumps(data_record, ensure_ascii=False)
    return json_data_record

def extract_with_xpath_24ur():
    pass

def extract_with_xpath_bolha(page_html):

    title = location = price = published_time = ""

    document_tree = html.fromstring(page_html)

    titles = document_tree.xpath('//*[@id="form_browse_detailed_search"]/div/div[1]/div[6]/div[4]/ul/li[*]/article/h3/a/text()')

    print("titles: (", len(titles), ")")
    print(titles)

    locations = document_tree.xpath('//*[@id="form_browse_detailed_search"]/div/div[1]/div[6]/div[4]/ul/li[*]/article/div[2]/div/text()')
    locations_new = []
    for location in locations:
        if location[0] != "\n":
            locations_new.append(location)
    locations = locations_new

    print("locations: (", len(locations), ")")
    print(locations)

    prices = document_tree.xpath('//*[@id="form_browse_detailed_search"]/div/div[1]/div[6]/div[4]/ul/li[*]/article/div[7]/ul/li/strong/text()')
    prices_new = []
    for price in prices:
        prices_new.append(price)
    prices = prices_new

    print("prices: (", len(prices), ")")
    print(prices)

    return ""

if __name__ == "__main__":

    rtv_html_names = ["Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
                 "Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html" ]

    overstock_html_names = ["jewelry01.html", "jewelry02.html"]

    bolha_html_names = ["Oddaja sob _ Najem sob - Nepremičnine bolha.com.html", "Analogni fotoaparati.html"]


    for rtv_html_name in rtv_html_names:
        f = codecs.open("../input-extraction/rtvslo.si/" + rtv_html_name, 'r', encoding='utf-8')
        page_html = f.read()
        extracted_data = extract_with_xpath_rtv(page_html)
        print(rtv_html_name + ":", extracted_data)

    for overstock_html_name in overstock_html_names:
        f = codecs.open("../input-extraction/overstock.com/" + overstock_html_name, 'r', encoding='iso-8859-1')
        page_html = f.read()
        extracted_data = extract_with_xpath_overstock(page_html)
        print(overstock_html_name + ":", extracted_data)

    # for bolha_html_name in bolha_html_names:
    #     f = codecs.open("../input-extraction/bolha.com/" + bolha_html_name, 'r', encoding='utf-8')
    #     page_html = f.read()
    #     extracted_data = extract_with_xpath_bolha(page_html)
    #     print(bolha_html_name + ":", extracted_data)
