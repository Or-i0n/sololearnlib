from urllib import request
from bs4 import BeautifulSoup as Soup, ResultSet

from bs4.element import NavigableString
from typing import Optional, Dict, List
from http.client import HTTPResponse


__author__ = "OR!ON"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.4.0"
__maintainer__ = "OR!ON"
__status__ = "Prototype"


class _Worker:
    def __init__(self) ->  None:
        self.domain = "https://www.sololearn.com"
        self.raw_page: Optional[HTTPResponse] = None

    def _fetch_page(self, subdomain: str) -> None:
        """Returns the HTTPResponse object to self.raw_page"""

        raw: HTTPResponse = request.urlopen(self.domain + subdomain)
        self.raw_page = raw

    def _get_soup(self, subdomain: str) -> Soup:
        """Returns a BeautifulSoup Object."""

        self._fetch_page(subdomain)
        soup = Soup(self.raw_page, "html.parser")
        return soup

    def _get_hot_today(self, soup: Soup) -> List[Dict[str, str]]:
        """Returns the 'Hot Today' names and links."""

        # Format of self.hot_today ->
        # [{code_name: <CodeLink>}, ...]
        hot_today: List[Dict[str, str]] = []

        sidebar: NavigableString = soup.find("div", {"class": "sidebar"})
        list_wrapper: NavigableString = sidebar.find("div", {"class": "list"})
        list_items: ResultSet = list_wrapper.find_all("a")

        for item in list_items:
           link: str = item["href"]
           name: str  = item.span.string
           hot_today.append({name: link})
            
        return hot_today
