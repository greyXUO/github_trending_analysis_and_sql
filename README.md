# Github Trending Analysis & SQL practice
This project intends to use the data from github trending website to analyze popular repositories, programming languages. During this process, i will use python to do the website crawl and use localhost Mysql to store the date I get everyday into a database. 
Github Policy allows

After two weeks of collection, we will have enough data to do the analysis. Again, we use sql to get the data we need and do data cleaning, data analysis with python. 

## Stage 1: Data Collection
To do the analysis, we need cleaned data first. Of course we can get standard data from files like xlsx, csv, etc. However, trying to use the MySQL is also part of my purpose. And I did meet a few questions using MySQL and connecting that to python script.

First we need to create a database and table to store the data:
```Mysql
CREATE DATABASE github_data;
CREATE TABLE `repositories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `language` varchar(255) DEFAULT NULL,
  `stars` int DEFAULT NULL,
  `forks` int DEFAULT NULL,
  `today_stars` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
```

And here are the packages we need for stage 1: 
 ``` python 
import requests
import mysql.connector
from bs4 import BeautifulSoup
```

Then we can read the content of the trending page with requests and beautiful soup🍲!
 ``` python 
# get the content of website
url = "https://github.com/trending"
response = requests.get(url, timeout=(5, 30))
html_content = response.text

# get the html content of the page
soup = BeautifulSoup(html_content, "html.parser")
```

Then connect to local host MySQL with the mysql connector.
 ``` python 
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='******',
    database='github_data'
)
# check if connection works
if cnx.is_connected():
    print("Successfully connected to MySQL database.")
else:
    print("Failed to connect to MySQL database.")
```
With a cursor from the connection, we are now able to INSERT records into the local table.

## Stage 2: Crawling Coding

After connecting the localhost sql, now we need to get the data. First, after observing the inspect view of github trending, 
```python

items = soup.find_all('article', class_='Box-row')

# iterate to get the info in each item
for item in items:
    repo_name_tag = item.find('h2', class_='h3 lh-condensed').find('a')
    repo_name = repo_name_tag.text.strip()
    # delete space and enter
    repo_name = repo_name.replace('\n', '').replace(' ', '')

    # get programming language
    language_tag = item.find('span', itemprop="programmingLanguage")
    language = language_tag.text.strip()

    # get stars
    stars_tag = item.find('a', href=lambda x: x and x.endswith('/stargazers'))
    stars = stars_tag.text.strip()
    stars = stars.replace(',', '')

    # get forks
    forks_tag = item.find('a', href=lambda x: x and x.endswith('/forks'))
    forks = forks_tag.text.strip()
    forks = forks.replace(',', '')

    # get stars today
    stars_today_tag = item.find('span', class_='d-inline-block float-sm-right')
    today_stars = stars_today_tag.text.strip().split()[0]
    today_stars = today_stars.replace(',', '')
    
    print(f"Title: {repo_name}, language: {language}, Stars: {stars}, Forks: {forks}, Stars Today: {today_stars}")

```

And to INSERT data into table, we need to pair the value with the column names

```python
    sql = "INSERT INTO repositories (repo_name, language, stars, forks, today_stars) VALUES (%s, %s, %s, %s, %s)"
    val = (repo_name, language, stars, forks, today_stars)
    cursor.execute(sql, val)

# commit change and close cursor
cnx.commit()
cursor.close()
```
## Stage 3: Data Analysis
TBC

## Extra SQL practice


