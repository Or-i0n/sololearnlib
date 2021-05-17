#TODO:
# - Make output of some of the functions more targeted i.e. remove unnecessary
#   data.

from sololearnlib._worker import _Worker
import re
import json


class Courses(_Worker):
    def __init__(self):
        super().__init__()
        self.subdomain = "/learning"
        self.soup = None

    def _parse(self, subdomain):
        """Get data out of the course page in json format."""

        self.soup = self._get_soup(subdomain)

        # The data about courses is stored inside a script tag.
        # Get data out of script tag using regex.
        scripts = self.soup.find_all("script")
        for script in scripts:
            if initial_data := re.search(r"window.initialData = (\{.*\})", str(script)):
                data = initial_data.group(1)
                return json.loads(data)
    
    def get_courses(self):
        """Get data about courses available on sololearn."""

        # Format of courses ->
        # {"getCourses":{
        #         "success":true,
        #         "errors":[],
        #         "data":[
        #     {
        #         "name":"Python Core",
        #         "description":"Learn Python, one of...",
        #         "metaDescription":"Python is one of...",
        #         "iconUrl":"https://sololearnuploads...",
        #         "learnersCount":7215058,
        #         "language":"py",
        #         "progress":0,
        #         "modules":[
                
        #         ],
        #         "id":1073
        # }, ...
        courses = self._parse(self.subdomain)
        return courses

    def get_lessons(self, course_id=1073):
        """Get lessons of any course, just enter the course_id.
        Default course_id is 1073 for python course.
        You can get other course_id from self.get_courses()."""

        # Format of lessons ->
        # {"getCourse":{
        #     "success":true,
        #     "errors":[
                
        #     ],
        #     "data":{
        #         "name":"Python Core",
        #         "description":"Learn Python, one of today's...",
        #         "metaDescription":"Python is one of the ...",
        #         "iconUrl":"https://sololearnuploads...",
        #         "learnersCount":0,
        #         "language":"py",
        #         "progress":0,
        #         "modules":[
        #             {
        #             "name":"Basic Concepts",
        #             "allowShortcut":false,
        #             "iconUrl":"https://sololearnuploads...",
        #             "codeCoaches":[
        #                 {
        #                     "title":"Exponentiation",
        #                     "difficulty":"easy",
        #                     "iconUrl":"https://api.sololearn...",
        #                     "isPro":false,
        #                     "rewardXp":10,
        #                     "moduleId":1220,
        #                     "type":"EOM",
        #                     "id":115
        #                 }
        #             ],
        #             "lessons":[
        #                 {
        #                     "courseId":0,
        #                     "moduleId":0,
        #                     "name":"Welcome to Python",
        #                     "type":"lesson",
        #                     "orderRank":1,
        #                     "quizzesCount":2,
        #                     "quizzes":[
                                
        #                     ],
        #                     "id":2269
        #                 }, ...
        lessons = self._parse(f"{self.subdomain}/{course_id}")
        return lessons







    
        