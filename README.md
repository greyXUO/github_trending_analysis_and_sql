# Github Trending Analysis & SQL practice
This project intends to use the data from github trending website to analyze popular repositories, programming languages. During this process, i will use python to do the website crawl and use localhost Mysql to store the date I get everyday into a database. 

After two weeks of collection, we will have enough data to do the analysis. Again, we use sql to get the data we need and do data cleaning, data analysis with python. 

## Stage 1: Data Collection
To do the analysis, we need cleaned data first. Of course we can get standard data from files like xlsx, csv, etc. However, trying to use the MySQL is also part of my purpose. And I did meet a few questions using MySQL and connecting that to python script.

First we need to create a database and table to store the data:
```Mysql
CREATE DATABASE github_data;
CREATE TABLE repositories(
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

## Stage 3: Data Analysis

## Extra SQL practice

