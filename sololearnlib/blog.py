from sololearnlib._worker import _Worker
import re
import json
from bs4 import BeautifulSoup as Soup 


class Blog(_Worker):
    """Retrieve blog posts from SoloLearn Blog"""

    def __init__(self):
        super().__init__()
        self.subdomain = "/blog"
        self.soup = None 

    def get_articles(self):
        """Returns the article info about the latest blog posts.
        Format of article info ->
       {'getTopics': {'success': 1, 'errors': [...], 'data': [...]}, 
       'getBlogPosts': {'paging': {...}, 'success': 1, 'errors': [...], 'data': [...]}}"""

        self.soup = self._get_soup(self.subdomain)

        regex_data = r"window.initialData=(\{.+\})</script>"
        match = re.search(regex_data, str(self.soup))
    
        if match:
            # Convert javascript dictionary into json.
            # Add double quote to the keys {key: "value"} => {"key": "value"}.
            key_regex = r'({|,)(\w+):'
            replaced = re.sub(key_regex, r'\1"\2":', match.group(1))
            # Replace invalid value.
            replaced = replaced.replace("!0", "1")
            # Replace single quote (') with doubl quote (").
            replaced = replaced.replace("'", '"')
            # Replace annoyoing tag. 
            replaced = replaced.replace('<span style="font-weight: 400;">', "")
            
            jsoned_data = json.loads(replaced)

            return jsoned_data

    def get_full_article(self, article_link):
        """Returns the full text of an article."""

        article = self._get_soup(article_link)

        # Parse raw article data from javascript
        article_content = {}
        for script in article.find_all("script"):
            if data := re.findall(r"window.initialData = (\{.*\})", str(script)):
                article_content = json.loads(data[0])["getBlogPost"]["data"]
        cleaned = Soup(article_content["fullContent"], "html.parser")
        return cleaned.get_text()