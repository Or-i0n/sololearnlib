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
from sololearnlib import Blog
```
- Create a class object.

```py
blog = Blog()
```

- Using methods/functions

```py
# Get data about all the articles.
articles = blog.get_articles()
# [{'id': 175, 'date': '2021-05-15T00:00:00.000Z', 'topic': 'Insights', 'title': 'The Growth of Learni...on Mobile ', 'content': 'What is responsible ... industry.', 'article_link': '/Blog/175', 'image_link': 'https://api.sololear...log_01.jpg'}, ...]

# Get the link of first article.
article_link = articles[0]["article_link"]
# '/Blog/175'

# Get the full text of an article.
full_text = blog.get_full_article(article_link)
# 'The COVID-19 pandemic has upended much of what was considered normal and routine in everyday life around the globe. Business, healthcare, transportation, travel - the massive disruptions in industries ...'
```

#### Retrieve Code Playground Data

- Import

```py
from sololearnlib import CodePlayground
```

- Create a class object.

```py
ground = CodePlayground()
```

- Using methods/functions

```py
# Get hot codes.
hot = ground.get_hot_today()
# [{'😄Pure css Emoji😄😊': 'https://code.sololearn.com/WVo6hshrJ3p6/#'}, {'⚔️Assasin Custom UI Cover ⚔️': 'https://code.sololearn.com/WdNImK2M9ush/#'}, ...]

# Get all other codes.
codes = ground.get_codes()
# [{'code_link': 'https://code.sololearn.com/WZmG081162lG/#', 'code_name': 'Water sort puzzle game 🔥', 'votes': 638, 'author_name': 'Namit Jain [INACTIVE]', 'author_link': '/Profile/18109487', 'data_date': '4/23/2021 6:17:25 AM'}, ...]
```

#### Retrieve Courses Data
- Import

```py
from sololearnlib import Courses
```

- Create a class object.
```py
courses = Courses()
```

- Using methods/functions

```py
# Get a list of all the available courses.
course_list = courses.get_courses()
# {'getCourses': {'success': True, 'errors': [...], 'data': [...]}}

# Get lessons of a course.
lessons = courses.get_lessons("python")
# {'getCourse': {'success': True, 'errors': [...], 'data': {...}}}

```

#### Retrieve Discuss Data
- Import

```py
from sololearnlib import Discuss
```

- Create a class object.

```py
dis = Discuss()
```

- Using methods/functions

```py
# Get posts available for discussion.
posts = dis.get_posts()
# [{'votes': '0', 'answers': '0', 'post_link': '/Discuss/2760604/trying-to-pull-individual-values-from-a-dataframe-but-pulls-arrays-instead', 'title': 'Trying to pull individual values from a dataframe but pulls arrays instead', 'tags': [...], 'author_name': 'Hernando Abella', 'author_link': '/Profile/1478871/', 'data_date': '4/20/2021 4:12:36 PM', 'avatar_link': 'https://blob.sololearn.com/avatars/e97c267a-e433-4c47-81f3-6d32dcd30570.jpg'}, ...]

# Trending topics on discussions.
hot_discuss = dis.get_hot_today()
# [{'Can we obtain graphs in node code here at sololearn ?': '/Discuss/2784363/can-we-obtain-graphs-in-node-code-here-at-sololearn/'}, {'Why R code is necessary?': '/Discuss/2784479/why-r-code-is-necessary/'}, ...]

```

#### Retrieve Top Learners Data
- Import

```py
from sololearnlib import TopLearners
```

- Create a class object.

```py
top = TopLearners()
```

- After creating an object you can use some of its attributes.

```py
print(top.courses)
# {'c': {'link': '/Leaderboard/C', 'title': 'C Tutorial'}, ...}

print(top.leaderboard_title)
# 'Global Leaderboard'
```

- Using methods/functions

```py
# List of user who top the 'react' leaderboard.
board = top.get_leaderboard("react")
# {'1': {'name': 'Arthur', 'points': 2000}, '2': {'name': 'Accountz5', 'points': 794}, '3': {'name': 'Hayk Tester1', 'points': 760}, ...}
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