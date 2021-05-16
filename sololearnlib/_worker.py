from urllib import request
from bs4 import BeautifulSoup as Soup


class _Worker:
    """This class contains various utility methods used by main classes."""

    def __init__(self):
        self.domain = "https://www.sololearn.com"
        self.raw_page = None

    def _fetch_page(self, subdomain):
        """Assigns the HTTPResponse object to self.raw_page"""

        self.raw_page = request.urlopen(self.domain + subdomain)

    def _get_soup(self, subdomain):
        """Returns a BeautifulSoup Object."""

        self._fetch_page(subdomain)
        soup = Soup(self.raw_page, "html.parser")
        return soup

    def _get_hot_today(self, soup):
        """Returns the 'Hot Today' names and links.
        
        Format of self.hot_today:
        -------------------------
        [{code_name: <CodeLink>}, ...]"""

        hot_today = []

        sidebar = soup.find("div", {"class": "sidebar"})
        list_wrapper = sidebar.find("div", {"class": "list"})
        list_items = list_wrapper.find_all("a")

        for item in list_items:
           link: str = item["href"]
           name: str  = item.span.string
           hot_today.append({name: link})
            
        return hot_today