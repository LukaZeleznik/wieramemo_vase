import urllib
site = "http://www.spot.gov.si/"
current_site_url_obj = urllib.parse.urlparse(site)
current_saved_site_url = current_site_url_obj.netloc

print(current_saved_site_url)
