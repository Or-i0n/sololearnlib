# TODO:
# -- Make get_leaderboard() return data.

from sololearnlib._worker import _Worker

from bs4 import BeautifulSoup as Soup, ResultSet
from bs4.element import NavigableString
from typing import Any, Optional, Dict, Union


class TopLearners(_Worker):
    def __init__(self) -> None:
        """Initialises object."""

        super().__init__()
        self.subdomain = "/Leaderboard"
        self.url: str = self.domain + self.subdomain

        # Stores html of the self.leaderboard_link page.
        self.page: Soup = self._get_soup(self.subdomain)
        self.courses: Dict[str, Dict[str, str]] = {}
        self.leaderboard_title: str = ""
        self.leaderboard: Dict[str, Dict[str, Union[str, int]]] = {}
        
        # By default fetch the global leaderboard.
        self._fetch_global()

    def _get_courses(self) -> None:
        """Get a dict of available courses with their link and title."""

        leaderboard_courses: NavigableString = self.page.find("div",
                                             {"class": "leaderboardCourses"})
        courses: ResultSet = leaderboard_courses.find_all("a")
        for course in courses:
            course_title: str = course.get("title")
            course_link: str = course["href"]
            key: str = course_link.split("/")[-1].lower()
            self.courses[key] = {"link": course_link, "title": course_title}

    def _get_leaderboard_title(self) -> None:
        """Get the leaderboard title."""

        details: NavigableString = self.page.find("div", {"class": "details"})
        self.leaderboard_title: str = details.get_text(separator=" ", 
            strip=True)

    def _get_top_learners(self) -> None:
        """Get user info from leaderboard. It includes their
        rank, name and points."""

        leaderboard_list: NavigableString = self.page.find("div", 
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

    def get_leaderboard(self, course: str) -> None:
        """Get the leaderboard of
        a specific language.
        Use .courses attribute to get info
        about available courses and their
        leaderboard links.

        Some of the courses are:
        ['python', 'cplusplus', 'java',
        'javascript', 'csharp', 'c', 'sql',
        'machine-learning', 'data-science',
        'html', 'php', 'css', 'ruby',
        'jquery', 'fullstack', 'react',
        'swift']"""

        course_info = self.courses[course]
        course_link = course_info["link"]
        course_title = course_info["title"]

        self.leaderboard_link = course_link
        self.leaderboard_title = course_title

        self._fetch()


