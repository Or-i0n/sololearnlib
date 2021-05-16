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
        [{"id": <ID>, "date": <Date>, "topic": <Topic>,
          "title": "<Title>, "content": <Content>,
          "article_link": <ArticleLink>, "image_link": <ImageLink>},
          ...]"""

        self.soup = self._get_soup(self.subdomain)

        # Parse raw article data from javascript.
        # (JSON data of blog posts within script tags)
        for script in self.soup.find_all("script"):
            if data := re.findall(r"\"getBlogPosts\".+\"data\":(\[.*\])", str(script)):
                raw_articles = data[0]

        article_list = []
        # Process the raw data and get the details
        for article in json.loads(raw_articles):
            blog = {}
            blog["id"] = article["id"]
            blog["date"] = article["createdDate"]
            blog["topic"] = article["topicName"]
            blog["title"] = article["title"]
            blog["content"] = article["metaDescription"]
            blog["article_link"] = f"/Blog/{blog['id']}"
            blog["image_link"] = article["mainImageUrl"]
            article_list.append(blog)
        return article_list

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