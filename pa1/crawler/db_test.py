import db_methods as db
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

'''Insert site'''
site = db.insert_site("test.com123", "robotstext", "sitemaptext")
print("inserted site:", site)

'''Insert page'''
page1 = db.insert_page(site[0], PAGE_TYPE_CODES[0], "test.com/index.html", "html_content", "300", "040521")
print("inserted page:", page1)

page2 = db.insert_page(site[0], PAGE_TYPE_CODES[0], "test1.com/index.html", "html_content2", "303", "040522")
print("inserted page:", page2)

'''Insert image'''
image = db.insert_image(page1[0], "slika.jpg", "image/jpg", "asd", "040521")
print("inserted image:", image)

'''Insert page_data'''
page_data = db.insert_page_data(page2[0], DATA_TYPES[0], "asd")
print("page_data_id:", page_data)

'''Insert link'''
link = db.insert_link(page1[0], page2[0])
print("inserted link:", link)

print("getting all sites:", db.get_all_sites())
print("getting all pages:", db.get_all_pages())
print("getting all images:", db.get_all_images())
print("getting all page data:", db.get_all_page_data())
print("getting_all_links:", db.get_all_links())


print("deleting all links:", db.delete_all_links())
print("deleting all page data:", db.delete_all_page_data())
print("getting all images:", db.delete_all_images())
print("deleting all pages:", db.delete_all_pages())
print("deleting all sites:", db.delete_all_sites())
