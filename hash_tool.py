import hashlib
from html_similarity import similarity

class HashTool:
    def create_content_hash(self, html_content):
        try:
            m = hashlib.sha256()
            m.update(html_content.encode('utf-8'))
            return m.hexdigest()
        except Exception as error:
            print("Hashing error", error)
            return None
    def calculate_similarity(self, html_content1, html_content2):
        return similarity(html_content1, html_content2)