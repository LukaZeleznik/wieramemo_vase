import db_methods as db
PAGE_TYPE_CODES = ["HTML","DUPLICATE","FRONTIER","BINARY"]
DATA_TYPES = ["DOC","DOCX","PDF","PPT","PPTX"]

'''Insert site'''
site = db.insert_site("test.com123", "robotstext", "sitemaptext")
print("inserted site:", site)

'''Insert page'''
page1 = db.insert_page(site[0], PAGE_TYPE_CODES[2], "test.com/index.html", "html_content", "300", "040521")
print("inserted page:", page1)

page2 = db.insert_page(site[0], PAGE_TYPE_CODES[2], "test1.com/index.html", "html_content2", "303", "040522")
print("inserted page:", page2)

updated_page1 = db.update_page_by_id(page1[0], page1[1], PAGE_TYPE_CODES[0], page1[3], page1[4], page1[5], page1[6])

updated_page2 = db.update_page_by_id(page2[0], page2[1], PAGE_TYPE_CODES[0], page2[3], page2[4], page2[5], page2[6])


print("getting all sites:", db.get_all_sites())
print("getting all pages:", db.get_all_pages())

print("deleting all pages:", db.delete_all_pages())
print("deleting all sites:", db.delete_all_sites())