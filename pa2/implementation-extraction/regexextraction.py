import re, os, sys, codecs, json
from lxml import html

def extract_with_regex_overstock(text):
    titles = []
    listPrices = []
    prices = []
    priceSavings = []
    savingPercents = []
    contents = []

    title1 = re.findall('PROD_ID=([0-9]+?)"><b>(.+?)</b>', text, flags=re.DOTALL)
    if title1:
        for title in title1:
            #print(title)
            if title[1] != '':
                titles.append(' '.join(title[1].split()))
    else:
        print("title1 not found")

    listPrice1 = re.findall('''List Price:</b></td>\n*\s*<td align="left" nowrap="nowrap"><s>(.+?)</s>''', text, flags=re.DOTALL)
    if listPrice1:
        #print(listPrice1)
        for listPrice in listPrice1:
            if listPrice != '':
                listPrices.append(' '.join(listPrice.split()))
    else:
        print("listPrice1 not found")

    price1 = re.findall('''class="bigred"><b>(.+?)</b></span></td>''', text, flags=re.DOTALL)
    if price1:
        #print(price1)
        for price in price1:
            if price != '':
                prices.append(' '.join(price.split()))
    else:
        print("price1 not found")

    priceSaving1 = re.findall('''<td align="left" nowrap="nowrap"><span class="littleorange">(.+?)<{1}|\n{1}''', text, flags=re.DOTALL)
    if priceSaving1:
        for priceSaving in priceSaving1:
            if priceSaving != '':
                priceSaving = (' '.join(priceSaving.split()))
                priceSavingPlusPercent = priceSaving.split(" ")
                priceSavings.append(priceSavingPlusPercent[0])
                savingPercents.append(priceSavingPlusPercent[1])
    else:
        print("priceSavings1 not found")

    content1 = re.findall('''<td valign="top"><span class="normal">(.+?)</b></span>''', text, flags=re.DOTALL)
    if content1:
        #print(content1)
        for content in content1:
            if content != '':
                contentCleared = re.sub(r'<br><a href=".*"><span class="tiny"><b>','',' '.join(content.split()))
                contents.append(contentCleared)
    else:
        print("content1 not found")

    data_records = []

    for title, list_price, price, saving, saving_percent, content in zip(titles, listPrices, prices, priceSavings,
                                                                         savingPercents, contents):
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
    return [titles, listPrices, prices, priceSavings, savingPercents, contents]

def extract_with_regex_rtv(text):
    titles = []
    subtitles = []
    leads = []
    authors = []
    publishedTimes = []
    contents = []

    title1 = re.findall('<title>(.+?)</title>', text, flags=re.DOTALL)
    if title1:
        for title in title1:
            #print(title)
            if title != '':
                titles.append(' '.join(title.split()))
    else:
        print("title1 not found")

    subtitle1 = re.findall('<div class="subtitle">(.+?)</div>', text, flags=re.DOTALL)
    if subtitle1:
        #print(subtitle1)
        for subtitle in subtitle1:
            if subtitle != '':
                subtitles.append(' '.join(subtitle.split()))
    else:
        print("subtitle1 not found")

    lead1 = re.findall('<p class="lead">(.+?)</p>', text, flags=re.DOTALL)
    if lead1:
        #print(lead1)
        for lead in lead1:
            if lead != '':
                leads.append(' '.join(lead.split()))
    else:
        print("lead1 not found")

    author1 = re.findall('<div class="author-name">(.+?)</div>', text, flags=re.DOTALL)
    if author1:
        for author in author1:
            if author != '':
                authors.append(' '.join(author.split()))
    else:
        print("authors1 not found")

    publishedTime1 = re.findall('<div class="publish-meta">(.+?)<br>', text, flags=re.DOTALL)
    if publishedTime1:
        #print(publishedTime1)
        for publishedTime in publishedTime1:
            if publishedTime != '':
                publishedTimes.append(' '.join(publishedTime.split()))
    else:
        print("publishedTime1 not found")

    content1 = re.findall('<article class="article">.*?(<p.*>(.*?)<\/p>).*?<div class="gallery">', text,re.DOTALL)
    if content1:
        #print(content1)
        for content in content1:
            if content[0] != '':
                cnt = ' '.join(content[0].split())
                cnt = cnt.replace("<strong>","")
                cnt = cnt.replace("</strong>","")
                cnt = cnt.replace("<br>","")
                cnt = cnt.replace("<sub>","")
                cnt = cnt.replace("</sub>","")
                cnt = cnt.replace("<a>","")
                cnt = cnt.replace("</a>","")
                cnt = cnt.replace("<p>","")
                cnt = cnt.replace("</p>","")
                cnt = cnt.replace("</figcaption>","")
                cnt = cnt.replace("</figure>","")
                cnt = cnt.replace("</span>","")
                cnt = cnt.replace('<p class="Body">', '')
                cnt = cnt.replace('<iframe src="./Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si_files/LCypVFeHy_c.html" width="100%" height="350" frameborder="0" allowfullscreen="" border="0"></iframe>',"")
                cnt = cnt.replace('<figure class="{hide_class} photoswipe image c-figure-full" itemprop="associatedMedia" itemscope="" itemtype="http://schema.org/ImageObject">',"")
                cnt = cnt.replace('<a href="./Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si_files/65559996.jpg" itemprop="contentUrl" data-size="1200x800" data-large="https://img.rtvslo.si/_up/upload/2019/01/25/65559996.jpg" data-id="1">',"")
                cnt = cnt.replace('<img src="./Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si_files/65559996.jpg" title="" alt="">',"")
                cnt = cnt.replace('<figcaption itemprop="caption description">',"")
                cnt = cnt.replace('<span class="icon-photo">',"")
                cnt = cnt.replace('Foto: David Šavli',"")
                if (cnt == ""): continue
                contents.append(cnt)
    else:
        print("content1 not found")
    
    #return []
    data_record = dict()

    data_record["Author"] = authors[0]
    data_record["Title"] = titles[0]
    data_record["PublishedTime"] = publishedTimes[0]

    data_record["SubTitle"] = subtitles[0]
    data_record["Lead"] = leads[0]
    data_record["Content"] = contents[0]

    json_data_record = json.dumps(data_record, ensure_ascii=False)
    return json_data_record
    return [titles, subtitles, leads, authors, publishedTimes, contents]

def extract_with_regex_imdb(text):
    ranks = []
    titles = []
    years = []
    ratings = []

    rank1 = re.findall('<td class="titleColumn">(.+?)<a', text, flags=re.DOTALL)
    if rank1:
        for rank in rank1:
            #print(title)
            if rank != '':
                ranks.append(' '.join(rank.split()))
    else:
        print("rank1 not found")

    title1 = re.findall('''class="titleColumn">(.+?)" title="(.+?)">(.+?)</a>''', text, flags=re.DOTALL)
    if title1:
        #print(title1)
        for title in title1:
            if title != '':
                titles.append(' '.join(title[2].split()))
    else:
        print("title1 not found")

    year1 = re.findall('<span class="secondaryInfo">[(](.+?)[)]</span>', text, flags=re.DOTALL)
    if year1:
        #print(lead1)
        for year in year1:
            if year != '':
                years.append(' '.join(year.split()))
    else:
        print("year1 not found")

    rating1 = re.findall(' user ratings">(.+?)</strong>', text, flags=re.DOTALL)
    if rating1:
        for rating in rating1:
            if rating != '':
                ratings.append(' '.join(rating.split()))
    else:
        print("rating1 not found")

    data_records = []

    for rank, title, year, rating in zip(ranks, titles, years, ratings):
        data_record = dict()

        data_record["Rank"] = rank
        data_record["Title"] = title
        data_record["Year"] = year
        data_record["Rating"] = rating

        data_records.append(data_record)

    return data_records



def main():
    rtv_html_names = ["Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
                 "Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html" ]

    overstock_html_names = ["jewelry01.html", "jewelry02.html"]

    imdb_html_names = ["IMDb Top 250 - IMDb.html", "IMDb Top 250 TV - IMDb.html"]

    for rtv_html_name in rtv_html_names:
        #f = codecs.open(r'..\input-extraction\rtvslo.si\' + rtv_html_name, 'r', encoding='utf-8')
        f = codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'input-extraction', 'rtvslo.si',
                                     rtv_html_name), 'r', encoding='utf-8')
        page_html = f.read()
        extracted_data = extract_with_regex_rtv(page_html)
        print(rtv_html_name + ":", extracted_data)

    for overstock_html_name in overstock_html_names:
    #f = codecs.open("../input-extraction/overstock.com/" + overstock_html_name, 'r', encoding='iso-8859-1')
        f = codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'input-extraction', 'overstock.com',
                                     overstock_html_name), 'r', encoding='iso-8859-1')
        page_html = f.read()
        extracted_data = extract_with_regex_overstock(page_html)
        print(overstock_html_name + ":", extracted_data)


    for imdb_html_name in imdb_html_names:
        f = codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'input-extraction', 'imdb.com',
                                     imdb_html_name), 'r', encoding='utf-8')
        page_html = f.read()
        extracted_data = extract_with_regex_imdb(page_html)
        print(imdb_html_name + ":", extracted_data)

if __name__ == "__main__":
    main()