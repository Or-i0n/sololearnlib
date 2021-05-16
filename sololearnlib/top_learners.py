#TODO:
# - get_learderboard() not working with some courses.

from sololearnlib._worker import _Worker

class TopLearners(_Worker):
    def __init__(self):
        """Initialises object."""

        super().__init__()
        self.subdomain = "/Leaderboard"
        self.url = self.domain + self.subdomain

        # Stores html of the self.leaderboard_link page.
        self.soup = self._get_soup(self.subdomain)
        self.courses = {}
        self.leaderboard_title = ""
        self.leaderboard = {}
        
        # By default fetch the global leaderboard.
        self._fetch_global()

    def _get_courses(self):
        """Get a dict of available courses with their link and title."""

        leaderboard_courses = self.soup.find("div",
                                             {"class": "leaderboardCourses"})
        courses = leaderboard_courses.find_all("a")
        for course in courses:
            course_title = course.get("title")
            course_link = course["href"]
            key = course_link.split("/")[-1].lower()
            self.courses[key] = {"link": course_link, "title": course_title}

    def _get_leaderboard_title(self):
        """Get the leaderboard title."""

        details = self.soup.find("div", {"class": "details"})
        self.leaderboard_title = details.get_text(separator=" ", 
            strip=True)

    def _get_top_learners(self):
        """Get user info from leaderboard. It includes their
        rank, name and points."""

        leaderboard_list = self.soup.find("div", 
            {"class": "leaderboardList"})
        items = leaderboard_list.find_all("div", {"class": "item"})

        
        for item in items:
            rank, name, points = item.get_text(separator=",",
                                               strip=True).split(",")
            points_int: int = int(points[:-2].strip())
            self.leaderboard[rank] = {"name": name, "points": points_int}

    def _fetch(self):
        """Fetches page, leaderboard title and top learners."""

        self._get_leaderboard_title()
        self._get_top_learners()

    def _fetch_global(self):
        """Fetch global leaderboard page and get a data about
        available courses and their leaderboard links."""

        self._fetch()
        self._get_courses()

    def get_leaderboard(self, course):
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