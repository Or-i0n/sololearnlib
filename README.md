
# sololearnlib

  

sololearnlib is a library for retrieving public data from [Sololearn](https://www.sololearn.com).

  

- Easy to use.

- Lightweight.

- Object Oriented.

- Json-compatible data.

  

# New Features!

  

- Retrieve Blog articles.

- Get Leaderboard data.

You can also:

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

#### Retrieve Discuss Data

#### Retrieve Top Learners Data



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
