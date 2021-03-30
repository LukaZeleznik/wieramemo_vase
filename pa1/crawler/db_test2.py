import db_methods as db
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

'''Insert sites'''
site1 = db.insert_site("test.com123", "robotstext", "sitemaptext")
print("inserted site:", site1)

site2 = db.insert_site("test.com1223", "robotstext", "sitemaptext")
print("inserted site:", site2)

'''Insert pages'''
page1 = db.insert_page(site1[0], PAGE_TYPE_CODES[0], "test.com/index.html", "html_content", "300", "040521")
print("inserted page:", page1)

page2 = db.insert_page(site1[0], PAGE_TYPE_CODES[0], "test1.com/index.html", "html_content2", "303", "040522")
print("inserted page:", page2)

'''Insert images'''
image1 = db.insert_image(page1[0], "slika1.jpg", "image/jpg", "asd", "040521")
print("inserted image:", image1)

image2 = db.insert_image(page1[0], "slika2.jpg", "image/jpg", "asd", "040521")
print("inserted image:", image2)

'''Insert page_data'''
page_data1 = db.insert_page_data(page2[0], DATA_TYPES[0], "asd")
print("page_data_id:", page_data1)

page_data2 = db.insert_page_data(page1[0], DATA_TYPES[0], "asd")
print("page_data_id:", page_data2)

'''Insert link'''
link = db.insert_link(page1[0], page2[0])
print("inserted link:", link)

sites = db.get_all_sites()
pages = db.get_all_pages()
images = db.get_all_images()
page_data = db.get_all_page_data()
links = db.get_all_links()

# GET BY ID
for site_ in sites:
    print("getting site:", db.get_site_by_id(site_[0]))

for page_ in pages:
    print("getting page:", db.get_page_by_id(page_[0]))

for image_ in images:
    print("getting image:", db.get_image_by_id(image_[0]))

for page_data_ in page_data:
    print("getting page_data:", db.get_page_data_by_id(page_data_[0]))

# DELETE BY ID

for page_data_ in page_data:
    print("deleting page_data:", db.delete_page_data_by_id(page_data_[0]))

for image_ in images:
    print("deleting image:", db.delete_image_by_id(image_[0]))

print("deleting links: ", db.delete_all_links())

for page_ in pages:
    print("deleting page:", db.delete_page_by_id(page_[0]))

for site_ in sites:
    print("deleting site:", db.delete_site_by_id(site_[0]))

print("getting all sites:", db.get_all_sites())
print("getting all pages:", db.get_all_pages())
print("getting all images:", db.get_all_images())
print("getting all page data:", db.get_all_page_data())
print("getting_all_links:", db.get_all_links())
