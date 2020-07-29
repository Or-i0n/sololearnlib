from sololearnlib._worker import _Worker

from bs4 import BeautifulSoup as Soup, ResultSet
from bs4.element import NavigableString
from typing import Dict, Iterable, List, Union

DetailsList = List[Dict[str, Union[str, int]]]


class CodePlayground(_Worker):
    def __init__(self) -> None:
        super().__init__()
        self.subdomain = "/Codes"
        self.soup: Soup = self._get_soup(self.subdomain)
        self.hot_today: List[Dict[str, str]] = self._get_hot_today(self.soup)
        self.trending: DetailsList = []
        self.most_recent: DetailsList = []
        self.most_popular: DetailsList = []
               
    def _parse_details(self, code: Soup) -> Dict[str, Union[str, int]]:
        """Parses a codeContainer and extracts all the info."""

        # Format of details ->
        # {code_link: <Link>, code_name: <CodeName>, votes: <Votes>,
        #  author_name: <AuthorName>, author_link: <Link>, 
        #  data_date: <DateTime>}
        details: Dict[str, Union[str, int]] = {}

        name_link: NavigableString = code.find("a", {"class": "nameLink"})
           
        details["code_link"] = name_link["href"]
        details["code_name"] = name_link.get_text()

        details_wrapper: Soup = code.find("div", {"class": "detailsWrapper"})
        vote: Soup = details_wrapper.find("div", {"class": "vote"})

        details["votes"] = int(vote.find("p").get_text())
        
        author_details: Soup = code.find("div", {"class": "authorDetails"})
        details["author_name"] = author_details.a.get_text()
        details["author_link"] = author_details.a["href"]
        details["data_date"] = author_details.p["data-date"]
        
        return details

    def _fill_codes(self, public_codes: Iterable[Soup], ordering: str) -> None:
        """Fills code data inside the specified attribute."""

        orders = {"Trending": self.trending, "MostRecent": self.most_recent, 
                  "MostPopular": self.most_popular}
        for code in public_codes:
            details: Dict[str, Union[str, int]] = self._parse_details(code)
            orders[ordering].append(details)
    
    def get_codes(self, ordering: str ="Trending", *, 
        language: str ="", query: str ="") -> None:
        """Get codes according to ordering, language or query."""

        soup: Soup = self._get_soup(f"{self.subdomain}?ordering={ordering}&"
                              f"language={language}&query={query}")

        public_codes: ResultSet = soup.find_all("div", 
            {"class", "codeContainer"})
        
        if ordering == "Trending":
            self._fill_codes(public_codes, ordering)
        elif ordering == "MostRecent":
            self._fill_codes(public_codes, ordering)
        elif ordering ==  "MostPopular":
            self._fill_codes(public_codes, ordering)
