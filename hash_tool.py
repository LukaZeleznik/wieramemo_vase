import hashlib

class HashTool:
    def create_content_hash(self, html_content):
        try:
            m = hashlib.sha256()
            m.update(html_content.encode('utf-8'))
            return m.hexdigest()
        except Exception as error:
            print("     [CRAWLING] Error while creating content hash", error)
            return None