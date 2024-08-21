import requests
import mysql.connector
from bs4 import BeautifulSoup

# 获取页面内容
url = "https://github.com/trending"
response = requests.get(url, timeout=(100, 30))
html_content = response.text

# get the html content of the page
soup = BeautifulSoup(html_content, "html.parser")

# 连接到 MySQL 数据库
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='413413',
    database='github_data'
)

# 检查是否成功连接到数据库
if cnx.is_connected():
    print("Successfully connected to MySQL database.")
else:
    print("Failed to connect to MySQL database.")

cursor = cnx.cursor()

items = soup.find_all('article', class_='Box-row')

# 遍历所有项目并提取名称和数量，然后将数据插入到 items 表中
# 遍历每个项目并提取信息
for item in items:
    repo_name_tag = item.find('h2', class_='h3 lh-condensed').find('a')
    repo_name = repo_name_tag.text.strip()
    # # 去除项目内的空格和换行符
    repo_name = repo_name.replace('\n', '').replace(' ', '')

    # # 提取编程语言
    language_tag = item.find('span', itemprop="programmingLanguage")
    language = language_tag.text.strip()

    # # 提取Star数
    stars_tag = item.find('a', href=lambda x: x and x.endswith('/stargazers'))
    stars = stars_tag.text.strip()
    # # 去除逗号
    stars = stars.replace(',', '')

    # # 提取Fork数
    forks_tag = item.find('a', href=lambda x: x and x.endswith('/forks'))
    forks = forks_tag.text.strip()
    # # 去除逗号
    forks = forks.replace(',', '')

    # # 提取今天的Star数
    stars_today_tag = item.find('span', class_='d-inline-block float-sm-right')
    today_stars = stars_today_tag.text.strip().split()[0]
    # # 去除逗号
    today_stars = today_stars.replace(',', '')
    
    print(f"Title: {repo_name}, language: {language}, Stars: {stars}, Forks: {forks}, Stars Today: {today_stars}")

    # # 插入数据到数据库
    sql = "INSERT INTO repositories (repo_name, language, stars, forks, today_stars) VALUES (%s, %s, %s, %s, %s)"
    val = (repo_name, language, stars, forks, today_stars)
    cursor.execute(sql, val)

# 提交更改并关闭数据库连接
cnx.commit()
cursor.close()