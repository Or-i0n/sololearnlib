from _worker import _Worker

# Used for type referencing.
from typing import List, Dict
from bs4 import BeautifulSoup as Soup, ResultSet
from bs4.element import NavigableString


class Blog(_Worker):
    def __init__(self) -> None:
        super().__init__()
        self.subdomain = "/Blog"
        self.soup: Soup = self._get_soup(self.subdomain)
        
        self.recent_posts: List[Dict[str, str]] = []
        self.recent_news: List[Dict[str, str]] = []

    def _get_sidebar(self, sidebar_name: str) -> None:
        """Get the two sidebars 'Recent Posts' & 'Recent News'."""

        recent: NavigableString = self.soup.find("div", {"class": sidebar_name})
        articles: ResultSet = recent.find_all("a")

        for article in articles:
            link: str = article["href"]
            title: str = article.get_text()
            if sidebar_name == "recentArticles":
                self.recent_posts.append({title: link})
            elif sidebar_name == "archives":
                self.recent_news.append({title: link})
    
    def _fill_sidebars(self) -> None:
        """Fills data in self.recent_articles & self.recent_posts."""

        for barname in ("recentArticles", "archives"):
            self._get_sidebar(barname)

    def get_articles(self, *, page: str ="1") -> List[Dict[str, str]]:
        """Returns the article info about blog articles.

        Format of article info ->
        [{"date": <Date>, "title": "<Title>, 
          "image_link": <ImageLink>, "content": <Content>, 
          "article_link": <ArticleLink>},
         ...]"""

        articles_info: List[Dict[str, str]] = []
        articles: ResultSet

        if int(page) > 1:
            self.soup = self._get_soup(f"{self.subdomain}?page={page}")
            articles = self.soup.find_all("div", {"class": "article"})
        else:
            articles = self.soup.find_all("div", {"class": "article"})

        for article in articles:
            date: str = article.div.span.string
            title: str = article.div.h1.a.string

            content_wrapper: NavigableString = article.find("div", 
                {"class": "articleContent"})
            image_link: str
            try:
                image_link = content_wrapper.find("img")["src"]
            except TypeError:
                image_link = ""

            # Get article content skipping the first <p> that has <img>.
            # But if there is no image do otherwise.
            paras: List[ResultSet]
            if image_link == "":
                paras = list(content_wrapper.find_all("p"))
            else:
                paras = list(content_wrapper.find_all("p"))[1:]

            
            content_para = ""
            for para in paras:
                content_para += para.get_text() + " "
            
            more_button: NavigableString = article.find("div", 
                {"class": "blogMoreButton"})
            article_link: str = more_button.a["href"]

            articles_info.append({"date": date, "title": title, 
                "image_link": image_link, "content": content_para,
                "article_link": article_link})

        return articles_info

    def get_full_article(self, article_link: str) -> str:
        """Returns the full text of an article."""

        article: Soup = self._get_soup(article_link)

        article_content: NavigableString = article.find("div", 
            {"class": "articleContent"})
        article_text: str = article_content.get_text()

        return article_text
