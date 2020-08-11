
# sololearnlib

  

sololearnlib is a library for retrieving public data from [Sololearn](https://www.sololearn.com).

  

- Easy to use.

- Lightweight.

- Object Oriented.

- Json-compatible data.

  

# Features

  

- Retrieve Blog articles.

- Get Leaderboard data.

- Retrieve 'Hot Today' codes from Code Playground.

- Find out what are the trending, most recent and most popular codes.

- Get courses info and lessons data.

- Retrieve 'Hot Today' discussions.

- Find out what are the trending, most recent and unanswered discussions.

  

### Tech

  

sololearn just uses [bs4](https://pypi.org/project/bs4/) (BeautifulSoup4).

  

### Installation

  

sololearnlib requires [Python 3](https://www.python.org/) v3.5+ to run.

  
  
  

```sh

$ pip install sololearnlib

```

### Usage
#### Retrieve *Blog* data
- Import
```py
from sololearnlib.sololearn import Blog
```

- Create a class object.
```py
blog = Blog()
```

- After creating an object you can use some of its attributes.
```py
print(blog.domain)
# "https://www.sololearn.com"

print(blog.recent_posts)
# [{'\n\nHabit-Forming Lear... Learning\n': '/Blog/73/habit-formi...-learning/'}, ...]

print(blog.recent_news)
# [{'\n\nSoloLearn’s Learn ...lay India\n': '/Blog/29/sololearn-s...lay-india/'}, ...}]
```
- Using methods/functions
```py
articles = blog.get_articles()
# [{'article_link': '/Blog/73/habit-formi...-learning/', 'content': ' \xa0For most of us, th...ss time.\xa0 ', 'date': '07 August 2020', 'image_link': 'https://api.sololear...ning_1.jpg', 'title': 'Habit-Forming Learni...d Learning'}, ...]

# Get the link of first article.
article_link = articles[0]["article_link"]
# '/Blog/73/habit-forming-learning-vs-forced-learning/'

full_text = blog.get_full_article(article_link)
# '\n\nDo you struggle when learning new things? Most people do -- even when receiving a formal education in school or attending college, it can be hard to make new concepts stick. ...'
```
#### Retrieve Code Playground Data
  - Import
```py
from sololearnlib.sololearn import CodePlayground
```

- Create a class object.
```py
ground = CodePlayground()
```
- After creating an object you can use some of its attributes.
```py
print(ground.hot_today)
# [{'Web Dev Quiz': 'https://code.sololea...zpmPj7kP/#'}, ...]
```
- Using methods/functions
```py
codes = ground.get_codes()
# [{'author_link': '/Profile/12942084', 'author_name': 'Aakaanksha 💕', 'code_link': 'https://code.sololea...oj07HPmq/#', 'code_name': 'Google Clone or Real? 😳💕', 'data_date': '8/9/2020 7:36:06 AM', 'votes': 1146},  ...]
```
#### Retrieve Courses Data
 - Import
```py
from sololearnlib.sololearn import Courses
```
- Create a class object.
```py
courses = Courses()
```
- After creating an object you can use some of its attributes.
```py
print(courses.courses)
# {'c': {'counts': {...}, 'description': '\nOur C tutorial cove...uch more.\n', 'icon': '/Icons/Courses/1089.png', 'link': '/Course/C/', 'title': 'C Tutorial'}, ...}
```
- Using methods/functions
```py
lessons = courses.get_lessons("python")
# {'Basic Concepts': ['Welcome to Python', 'Your First Program', 'Simple Operations', 'Floats', 'Other Numerical Operations', 'Strings', 'String Operations', 'Variables', 'Taking User Input', ...], ...}
```

#### Retrieve Discuss Data
 - Import
```py
from sololearnlib.sololearn import Discuss
```
- Create a class object.
```py
dis = Discuss()
```
- After creating an object you can use some of its attributes.
```py
print(dis.hot_today)
# [{'[SOLVED]C++ Challenge problem': '/Discuss/2437254/sol...e-problem/'}, {'[Solved] Does Earnin...ves us XP?': '/Discuss/2437589/sol...ves-us-xp/'}, ...]
```
- Using methods/functions
```py
posts = dis.get_posts()
# [{'answers': '24716', 'author_link': '/Profile/5056131/', 'author_name': 'benka', 'avatar_link': 'https://avatars.solo...b873e5.jpg', 'data_date': '7/6/2017 5:02:16 PM', 'post_link': '/Discuss/516185/мног...оговорящих', 'tags': [...], 'title': 'много ли тут нас, ру...говорящих?', 'votes': '1199'}, ...]
```
#### Retrieve Top Learners Data
 - Import
```py
from sololearnlib.sololearn import TopLearners
```
- Create a class object.
```py
top = TopLearners()
```
- After creating an object you can use some of its attributes.
```py
print(top.courses)
# {'c': {'link': '/Leaderboard/C', 'title': 'C Tutorial'}, ...}

print(top.leaderboard)
# {'1': {'name': 'JΞΜΔ 🇨🇩👑', 'points': 1070064}, ...}

print(top.leaderboard_title)
# 'Global Leaderboard'
```
- Using methods/functions
```py
board = top.get_leaderboard("python")
# {'1': {'name': '👑 Prometheus 🇸🇬', 'points': 193985}, ...}
```


### Development

  

Want to contribute? Great!

Head toward the github repository:

-  [sololearnlib](https://github.com/Or-i0n/sololearnlib)

  

### Todos

  

- Write MORE Tests.

- Add error handling.

- Make retrieval time faster.

  

License

----

  

MIT

  

**Free Software, Hell Yeah!**
