from sololearnlib._worker import _Worker
from bs4 import BeautifulSoup as Soup

class CodePlayground(_Worker):
    def __init__(self):
        super().__init__()
        self.subdomain = "/Codes"
        self.soup = None
        self.trending = []
        self.most_recent = []
        self.most_popular = []
               
    def _parse_details(self, code):
        """Parses a codeContainer and extracts all the info.
        
        Format of details ->
        {code_link: <Link>, code_name: <CodeName>, votes: <Votes>,
         author_name: <AuthorName>, author_link: <Link>, 
         data_date: <DateTime>}"""

        details = {}

        name_link = code.find("a", {"class": "nameLink"})
           
        details["code_link"] = name_link["href"]
        details["code_name"] = name_link.get_text()

        details_wrapper= code.find("div", {"class": "detailsWrapper"})
        vote = details_wrapper.find("div", {"class": "vote"})

        details["votes"] = int(vote.find("p").get_text())
        
        author_details = code.find("div", {"class": "authorDetails"})
        details["author_name"] = author_details.a.get_text()
        details["author_link"] = author_details.a["href"]
        details["data_date"] = author_details.p["data-date"]
        
        return details

    def _fill_codes(self, public_codes, ordering):
        """Fills code data inside the specified attribute."""

        orders = {"Trending": self.trending, "MostRecent": self.most_recent, 
                  "MostPopular": self.most_popular}
        for code in public_codes:
            details = self._parse_details(code)
            orders[ordering].append(details)
    
    def get_codes(self, ordering="Trending", *, 
        language="", query=""):
        """Return codes according to ordering, language or query."""

        self.soup = self._get_soup(f"{self.subdomain}?ordering={ordering}&"
                              f"language={language}&query={query}")

        public_codes = self.soup.find_all("div", 
            {"class", "codeContainer"})
        
        if ordering == "Trending":
            self._fill_codes(public_codes, ordering)
            return self.trending
        elif ordering == "MostRecent":
            self._fill_codes(public_codes, ordering)
            return self.most_recent
        elif ordering ==  "MostPopular":
            self._fill_codes(public_codes, ordering)
            return self.most_popular
        return None

    def get_hot_today(self):
        """Get codes that are trending on sololearn."""
        
        # For performace improvement only load page if not loaded else skip.
        if not self.soup:
            self.soup = self._get_soup(self.subdomain)

        return self._get_hot_today(self.soup)