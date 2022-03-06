# Import classes from files to directly access them when initializing 
# sololearnlib.

from datetime import date

__name__="sololearnlib"
__version__ = "4.0.2"
__description__="Library that retrieves public data from sololearn.com"
__author__ = "OR!ON"
__copyright__ = f"Copyright 2020-{date.today().year}"
__license__ = "MIT"
__maintainer__ = "OR!ON"
__status__ = "Beta"

from sololearnlib.blog import Blog
from sololearnlib.code_playground import CodePlayground
from sololearnlib.discuss import Discuss
from sololearnlib.top_learners import TopLearners
