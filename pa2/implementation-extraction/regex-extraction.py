import re, os, sys, codecs

f = codecs.open(r"c:\Users\lukaz\Desktop\faks\ieps\wieramemo_vase\pa2\input-extraction\overstock.com\jewelry01.html", 'r')
text = f.read()

title1=listPrice1=price1=saving1=savingPercent1=content1 = ""

matchTitle = re.search('PROD_ID=157105"><b>(.+?)</b>', text, flags=re.DOTALL)
if matchTitle:
    title1 = ' '.join(matchTitle.group(1).split())
    print(title1)
else:
    print("title1 not found")

matchListPrice = re.search('''List Price:</b></td>
                                                <td align="left" nowrap="nowrap"><s>(.+?)</s>''', text, flags=re.DOTALL)
if matchListPrice:
    listPrice1 = ' '.join(matchListPrice.group(1).split())
    print(listPrice1)
else:
    print("listPrice1 not found")