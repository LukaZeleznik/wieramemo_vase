import urllib.robotparser
import requests

robotstxt = requests.get("https://www.gov.si/robots.txt")
print(robotstxt.status_code)
if robotstxt.status_code != 200:
    return "",""
 
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://www.luki.ml/robots.txt")
rp.read()
sitemap = rp.site_maps()

robotstxt = requests.get("https://www.luki.ml/robots.txt").content.decode("utf-8") 
#if sitemap[0]: sitemap = requests.get(sitemap[0]).content.decode("utf-8")
#else: sitemap = ""

print(robotstxt)