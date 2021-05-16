from sololearnlib._worker import _Worker

class Discuss(_Worker):
    def __init__(self) -> None:
        super().__init__()
        self.subdomain = "/Discuss"
        self.soup = self._get_soup(self.subdomain)

        
        self.hot_today= self._get_hot_today(self.soup)

        # Format of self.trending ->
        # [{votes: 1184, answers: 24077, title: <Title>, tags: [<Tags>, ...],
        #   author: <AuthorName>, profile_link: <Link>, data_date: <DateTime>,
        #   avatar: <Link>}, ...]
        self.trending = []
        self.most_recent = []
        self.unanswered = []

    def _parse_details(self, code):
        """Parses a codeContainer and extracts all the info.
        
        Format of details ->
        {votes: 1184, answers: 24077, post_link: <PostLink> title: <Title>, 
         tags: [<Tags>, ...], author_name: <AuthorName>, author_link: <Link>, 
         data_date: <DateTime>, avatar_link: <Link>}"""

        details = {}
        post_stats = code.find("div", {"class": "postStats"})
        post_stats_children = list(post_stats.children)
        
        details["votes"] = post_stats_children[1].p.string
        # There is a spelling mistake in the page source.
        # Note the spelling of <a class='postAnsewers'.
        # 'Answers' is written as 'Anserwers'.
        details["answers"] = post_stats_children[3].p.string

        post_details = code.find("div", 
            {"class": "postDetails"})
        
        details["post_link"] = post_details.p.a["href"]
        details["title"] = post_details.p.a.string

        tags_wrapper = list(post_details.children)[3]
        tags = tags_wrapper.find_all("span")
        tag_list = []
        for tag in tags:
            tag_list.append(tag.string)

        details["tags"] = tag_list
              
        author_details = code.find("div", 
            {"class": "authorDetails"})
        details["author_name"] = author_details.div.a.string
        details["author_link"] = author_details.div.a["href"]
        details["data_date"] = author_details.p["data-date"]
        details["avatar_link"] = list(author_details.children)[3].img["src"]
        
        return details

    def _fill_posts(self, public_codes, ordering) -> None:
        """Fills code data inside the specified attribute."""

        orders = {"Trending": self.trending, 
            "MostRecent": self.most_recent, 
            "Unasnswered": self.unanswered}
        for code in public_codes:
            details: ParseType2 = self._parse_details(code)
            orders[ordering].append(details)

    def get_posts(self, ordering="Trending", *, 
        query=""):
        """Return codes according to ordering, language or query."""

        soup: Soup = self._get_soup(f"{self.subdomain}?ordering={ordering}&"
                            f"query={query}")

        questions = soup.find_all("div", {"class", "question"})
        
        if ordering == "Trending":
            self._fill_posts(questions, ordering)
            return self.trending
        elif ordering == "MostRecent":
            self._fill_posts(questions, ordering)
            return self.most_recent
        elif ordering ==  "Unanswered":
            self._fill_posts(questions, ordering)
            return self.unanswered
        return None