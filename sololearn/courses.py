# TODO:
# -- Make a separate dict for counts.
# -- Add specific type to lesson_link: Any = self.courses[course]["link"].

from sololearn._worker import _Worker

from typing import List, Dict, Union, Any
from bs4 import BeautifulSoup as Soup, ResultSet
from bs4.element import NavigableString

ParseType = Dict[str, Union[Dict[str, int], str]]
CourseObj = Dict[str, ParseType]


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

    def _parse_lesson(self, lesson_link: str):
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

    def get_lessons(self, course: str):
        """Puts lessons data inside sel.courses and self.lessons."""

        lesson_link: Any = self.courses[course]["link"]
        lesson_data = self._parse_lesson(lesson_link)
        # self.courses[course]["lessons"] = lesson_data
        self.lessons = lesson_data
