import configparser
import sqlite3

from celery import Celery
import requests
from lxml import html
import cssselect

config = configparser.ConfigParser()
config.read("./config.ini")
redis_server = config['redis']

app = Celery('celery_test',
             broker='redis://{}:{}'.format(redis_server['host'],
                                           redis_server['port']))
app.config_from_object('cron.celeryconfig')

@app.task
def crawl_superstar():
    res = requests.get("https://nba.udn.com/nba/index?gr=www")
    tree = html.document_fromstring(res.text)
    news = tree.xpath("//div[@id='news_body']//dt")

    conn = sqlite3.connect("../superstar/db.sqlite3")
    c = conn.cursor()

    for new in news:
        title = new.cssselect('h3')[0].text
        print(title)
        url = "https://nba.udn.com" + new.cssselect('a')[0].attrib['href']
        print(url)
        c.execute("INSERT INTO news_news (title, url) VALUES ('{}', '{}')"
                  .format(title, url))

    conn.commit()
    conn.close()
