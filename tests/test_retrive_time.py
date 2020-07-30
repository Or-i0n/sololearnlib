# TODO:
# -- Make CodePlaground faster, retrieval time should be less than ~2 secs.

import time
from sololearnlib.blog import Blog
from sololearnlib.code_playground import CodePlayground
from sololearnlib.courses import Courses 
from sololearnlib.discuss import Discuss
from sololearnlib.top_learners import TopLearners

clock = time.perf_counter()
courses = Courses()
print("Courses -> Time taken:", time.perf_counter() - clock)

clock = time.perf_counter()
play = CodePlayground()
print("Play -> Time taken:", time.perf_counter() - clock)

clock = time.perf_counter()
top = TopLearners()
# print(top.leaderboard)
# top.get_leaderboard("python")
# print(top.leaderboard)
print("Top -> Time taken:", time.perf_counter() - clock)

clock = time.perf_counter()
dis = Discuss()
# d.get_posts(query="prime")
# print(d.trending)
print("Dis -> Time taken:", time.perf_counter() - clock)