import db as db
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

'''Insert site'''
site_id = db.insert_site("test.com", "robotstext", "sitemaptext")[0]
print ("site_id:", site_id)

'''Insert page'''
page_id = db.insert_page(site_id, PAGE_TYPE_CODES[0], "test.com/index.html", "html_content", "300", "040521")[0]
print ("pageid :", page_id)

'''Insert image'''
image_id = db.insert_image(page_id, "slika.jpg", "image/jpg", "asd", "040521")[0]
#image_id = db.insert_image("3", "slika.jpg", "image/jpg", "asd", "040521")[0]
print("image_id", image_id)

'''Insert page_data'''
page_data_id = db.insert_page_data(page_id, "slika.jpg", "image/jpg", "asd", "040521")[0]
#page_data_id = db.insert_page_data("3", DATA_TYPES[0], "asd")[0]
print("page_data_id", page_data_id)

'''Insert link'''
link = db.insert_link("6", "3")
print("link", link)

print("get_sites()", db.get_sites())
print("get_pages()", db.get_pages())
print("get_images()", db.get_images())
print("get_page_data()", db.get_page_data())
print("get_links()", db.get_links())