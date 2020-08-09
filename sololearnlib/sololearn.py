# TODO:
# -- Make CodePlayground return data faster.
# -- Add Usage to README file.
# -- Fix: blog.get_articles("2")
#         TypeError: get_articles() takes 1 positional argument but 2 were given
# -- Add a more specific type to Courses._parse_lesson().
# -- Convert 'votes' and 'answers' count to int in Discuss.courses.

from urllib import request
from bs4 import BeautifulSoup as Soup, ResultSet

# Used for type referencing.
from bs4.element import NavigableString
from typing import Optional, Dict, List, Union, Iterable, Any
from http.client import HTTPResponse

# Custom Types:
# -----------------------------------------------------------------------------
# Used in CodePlayground.
DetailsList = List[Dict[str, Union[str, int]]]
# Used in Courses.
ParseType = Dict[str, Union[Dict[str, int], str]]
DetailsList2 = List[Dict[str, ParseType]]
# Used in Discuss.
ParseType2 = Dict[str, Union[str, int, List[str]]]
# Used in Courses.
CourseObj = Dict[str, ParseType]

# Utility Class:
# -----------------------------------------------------------------------------
class _Worker:
    """This class contains various utility methods used by main classes."""

    def __init__(self) ->  None:
        self.domain = "https://www.sololearn.com"
        self.raw_page: Optional[HTTPResponse] = None

    def _fetch_page(self, subdomain: str) -> None:
        """Assigns the HTTPResponse object to self.raw_page"""

        raw: HTTPResponse = request.urlopen(self.domain + subdomain)
        self.raw_page = raw

    def _get_soup(self, subdomain: str) -> Soup:
        """Returns a BeautifulSoup Object."""

        self._fetch_page(subdomain)
        soup = Soup(self.raw_page, "html.parser")
        return soup

    def _get_hot_today(self, soup: Soup) -> List[Dict[str, str]]:
        """Returns the 'Hot Today' names and links.
        
        Format of self.hot_today:
        -------------------------
        [{code_name: <CodeLink>}, ...]"""

        hot_today: List[Dict[str, str]] = []

        sidebar: NavigableString = soup.find("div", {"class": "sidebar"})
        list_wrapper: NavigableString = sidebar.find("div", {"class": "list"})
        list_items: ResultSet = list_wrapper.find_all("a")

        for item in list_items:
           link: str = item["href"]
           name: str  = item.span.string
           hot_today.append({name: link})
            
        return hot_today


# Main Classes:
# -----------------------------------------------------------------------------
class Blog(_Worker):
    """This class contains various methods to retrieve data from sololearn
    blogs."""

    def __init__(self) -> None:
        super().__init__()
        self.subdomain = "/Blog"
        self.soup: Soup = self._get_soup(self.subdomain)
        
        self.recent_posts: List[Dict[str, str]] = []
        self.recent_news: List[Dict[str, str]] = []

        # Assign data to self.recent_posts and self.recent_news
        self._fill_sidebars()

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
        """Returns the article info about blog articles from the specified page.

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
        """Parses a codeContainer and extracts all the info.
        
        Format of details ->
        {code_link: <Link>, code_name: <CodeName>, votes: <Votes>,
         author_name: <AuthorName>, author_link: <Link>, 
         data_date: <DateTime>}"""

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
        language: str ="", query: str ="") -> Union[DetailsList, None]:
        """Return codes according to ordering, language or query."""

        soup: Soup = self._get_soup(f"{self.subdomain}?ordering={ordering}&"
                              f"language={language}&query={query}")

        public_codes: ResultSet = soup.find_all("div", 
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

class Courses(_Worker):
    def __init__(self) -> None:
        super().__init__()

        self.subdomain = "/Courses"
        # Assign a BeautifulSoup object
        self.soup: Soup = self._get_soup(self.subdomain)

        # Format of self.courses ->
        # {"python":{"link":"/Course/Python/",
        #            "icon":"/Icons/Courses/1073.png",
        #            "title":"Python 3 Tutorial",
        #            "description":"\nLearn Python, one of ..."
        #            "counts":{"learners":6720354,
        #                      "lessons":92,
        #                      "quizzes":275},
        #             },
        # "cplusplus": ...}
        self.courses: CourseObj= {}
        
        # Format of self.lessons ->
        # {"Basic Concepts": ["What is Python?", ...],
        #  "Control Structures": ["Boolean & Comparisons", ...],
        #  ...}
        
        self.lessons: Dict[str, List[str]] = {}

        self._get_courses()

    def _parse(self, course: NavigableString) -> ParseType:
        """Parses course to get its link & icon url, title, description
        counts and stores.
        :course: BeautifulSoup Object"""

        info = {"link": "", "icon": "", "title": "", "description": "",
                "counts": {}}

        info["link"] = course.a["href"]
        info["icon"] = course.a.img["src"]

        description: NavigableString = course.a.div
        info["title"] = description.div.get_text()
        info["description"] = description.p.get_text()

        counts: NavigableString =  course.find("div", {"class": "courseCounts"})
        counts_data: ResultSet = counts.find_all("li")
        for data in counts_data:
            name: str = data.span.get_text().lower()
            val: str = data.find("p").get_text()
            info["counts"][name] = int(val.replace(",", ""))

        return info

    def _update(self, course_name: str,  newdata: ParseType) -> None:
        """Inserts course and its data to self.courses."""

        self.courses[course_name] = newdata

    def _get_courses(self) -> None:
        """Get the course related html from page & put it inside a dict."""

        courses_content: NavigableString = self.soup.find("div", 
            {"class": "coursesContent"})
        course_items: ResultSet = courses_content.find_all("div", 
            {"class": "courseItem"})

        for item in course_items:
            course_name: str = item.a["href"].split("/")[-2].lower()
            course_data: ParseType = self._parse(item)
            self._update(course_name, course_data)

    def _parse_lesson(self, lesson_link: str) -> dict:
        """Get lesson data out of the link page and returns it as dict."""

        lesson_page: Soup = self._get_soup(lesson_link)
        lesson_content: NavigableString = lesson_page.find("div", 
            {"class": "moduleContent"})
        course_divs: ResultSet = lesson_content.find_all("div")

        data = {}
        module = ""
        for div in course_divs:
            if div["class"][0] == "courseModule":
                module = div.p.get_text().split(":")[-1].strip()
                data[module] = []
            elif div["class"][0] == "courseLesson":
                lesson_title = div.find("span", {"class": "courseLessonTitle"})
                data[module].append(lesson_title.get_text().strip())
        
        return data

    def get_lessons(self, course: str) -> Dict[str, List[str]]:
        """Returns lesson data."""

        lesson_link: Any = self.courses[course]["link"]
        lesson_data = self._parse_lesson(lesson_link)
        self.lessons = lesson_data
        return self.lessons

class Discuss(_Worker):
    def __init__(self) -> None:
        super().__init__()
        self.subdomain = "/Discuss"
        self.soup: Soup = self._get_soup(self.subdomain)

        
        self.hot_today: List[Dict[str, str]] = self._get_hot_today(self.soup)

        # Format of self.trending ->
        # [{votes: 1184, answers: 24077, title: <Title>, tags: [<Tags>, ...],
        #   author: <AuthorName>, profile_link: <Link>, data_date: <DateTime>,
        #   avatar: <Link>}, ...]
        self.trending: DetailsList2 = []
        self.most_recent: DetailsList2 = []
        self.unanswered: DetailsList2 = []

    def _parse_details(self, code: NavigableString) -> ParseType2:
        """Parses a codeContainer and extracts all the info.
        
        Format of details ->
        {votes: 1184, answers: 24077, post_link: <PostLink> title: <Title>, 
         tags: [<Tags>, ...], author_name: <AuthorName>, author_link: <Link>, 
         data_date: <DateTime>, avatar_link: <Link>}"""

        details: ParseType2 = {}
        post_stats: NavigableString = code.find("div", {"class": "postStats"})
        post_stats_children = list(post_stats.children)
        
        details["votes"] = post_stats_children[1].p.string
        # There is a spelling mistake in the page source.
        # Note the spelling of <a class='postAnsewers'.
        # 'Answers' is written as 'Anserwers'.
        details["answers"] = post_stats_children[3].p.string

        post_details: NavigableString = code.find("div", 
            {"class": "postDetails"})
        
        details["post_link"] = post_details.p.a["href"]
        details["title"] = post_details.p.a.string

        tags_wrapper: NavigableString = list(post_details.children)[3]
        tags: ResultSet = tags_wrapper.find_all("span")
        tag_list: List[str] = []
        for tag in tags:
            tag_list.append(tag.string)

        details["tags"] = tag_list
              
        author_details: NavigableString = code.find("div", 
            {"class": "authorDetails"})
        details["author_name"] = author_details.div.a.string
        details["author_link"] = author_details.div.a["href"]
        details["data_date"] = author_details.p["data-date"]
        details["avatar_link"] = list(author_details.children)[3].img["src"]
        
        return details

    def _fill_posts(self, public_codes: ResultSet, ordering: str) -> None:
        """Fills code data inside the specified attribute."""

        orders: Dict[str, Any] = {"Trending": self.trending, 
            "MostRecent": self.most_recent, 
            "Unasnswered": self.unanswered}
        for code in public_codes:
            details: ParseType2 = self._parse_details(code)
            orders[ordering].append(details)

    def get_posts(self, ordering: str="Trending", *, 
        query: str="") -> Union[DetailsList2, None]:
        """Return codes according to ordering, language or query."""

        soup: Soup = self._get_soup(f"{self.subdomain}?ordering={ordering}&"
                            f"query={query}")

        questions: ResultSet = soup.find_all("div", {"class", "question"})
        
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

class TopLearners(_Worker):
    def __init__(self) -> None:
        """Initialises object."""

        super().__init__()
        self.subdomain = "/Leaderboard"
        self.url: str = self.domain + self.subdomain

        # Stores html of the self.leaderboard_link page.
        self.soup: Soup = self._get_soup(self.subdomain)
        self.courses: Dict[str, Dict[str, str]] = {}
        self.leaderboard_title: str = ""
        self.leaderboard: Dict[str, Dict[str, Union[str, int]]] = {}
        
        # By default fetch the global leaderboard.
        self._fetch_global()

    def _get_courses(self) -> None:
        """Get a dict of available courses with their link and title."""

        leaderboard_courses: NavigableString = self.soup.find("div",
                                             {"class": "leaderboardCourses"})
        courses: ResultSet = leaderboard_courses.find_all("a")
        for course in courses:
            course_title: str = course.get("title")
            course_link: str = course["href"]
            key: str = course_link.split("/")[-1].lower()
            self.courses[key] = {"link": course_link, "title": course_title}

    def _get_leaderboard_title(self) -> None:
        """Get the leaderboard title."""

        details: NavigableString = self.soup.find("div", {"class": "details"})
        self.leaderboard_title: str = details.get_text(separator=" ", 
            strip=True)

    def _get_top_learners(self) -> None:
        """Get user info from leaderboard. It includes their
        rank, name and points."""

        leaderboard_list: NavigableString = self.soup.find("div", 
            {"class": "leaderboardList"})
        items: ResultSet = leaderboard_list.find_all("div", {"class": "item"})

        rank: str 
        name: str
        points: str

        for item in items:
            rank, name, points = item.get_text(separator=",",
                                               strip=True).split(",")
            points_int: int = int(points[:-2].strip())
            self.leaderboard[rank] = {"name": name, "points": points_int}

    def _fetch(self) -> None:
        """Fetches page, leaderboard title and top learners."""

        self._get_leaderboard_title()
        self._get_top_learners()

    def _fetch_global(self) -> None:
        """Fetch global leaderboard page and get a data about
        available courses and their leaderboard links."""

        self._fetch()
        self._get_courses()

    def get_leaderboard(self, 
        course: str) -> Dict[str, Dict[str, Union[str, int]]]:
        """Get the leaderboard of a specific language.
        Use .courses attribute to get info about available courses and their
        leaderboard links.

        Some of the courses are:
        ['python', 'cplusplus', 'java', 'javascript', 'csharp', 'c', 'sql',
        'machine-learning', 'data-science', 'html', 'php', 'css', 'ruby',
        'jquery', 'fullstack', 'react', 'swift']"""

        course_info = self.courses[course]
        course_link = course_info["link"]
        course_title = course_info["title"]

        self.subdomain = course_link
        self.leaderboard_title = course_title
        self.soup = self._get_soup(self.subdomain)

        self._fetch()

        return self.leaderboard
