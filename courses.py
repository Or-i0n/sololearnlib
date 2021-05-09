from sololearnlib._worker import _Worker
import re
import json

class Courses(_Worker):
    def __init__(self):
        super().__init__()
        self.subdomain = "/learning"
        self.soup = None
        self.courses = {}
        self.lessons = {}

    def _parse(self):
        """Get data out of the course page and put it in self.courses."""
        
        # The data about courses is stored inside a script tag.
        # Get data out of script tag using regex.
        scripts = self.soup.find_all("script")
        for script in scripts:
            if initial_data := re.search(r"window.initialData = (\{.*\})", str(script)):
                data = initial_data.group(1)
                self.courses = json.loads(data)
                # print(self.courses)
    
    def get_courses(self):
        """Get data about courses available on sololearn."""

        # Format of self.courses ->
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
        
        self.soup = self._get_soup(self.subdomain)
        self._parse()
        return self.courses

    
        