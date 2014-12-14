# coding=utf-8
from selenium import webdriver
import time
import MySQLdb as myDB
import ConfigParser
import datetime

config = ConfigParser.ConfigParser()
config.read('info.config')
con = myDB.connect(config.get('db', 'host'), config.get('db', 'username'),
                   config.get('db', 'password'), config.get('db', 'schema'))
con.set_character_set('utf8mb4')
cur = con.cursor()
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8mb4;')
cur.execute('SET character_set_connection=utf8mb4;')

query = 'select distinct url ' \
        'from main_articles ' \
        'where url not in (select distinct url from twitter)'

cur.execute(query)
# urls = cur.fetchall()

urls = (("climate-science-is-not-settled", ), )

for url in urls:
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.private.browsing.autostart", True)
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("https://twitter.com/search?f=realtime&q=" + url[0])
    for i in range(300):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    twitter_dates = driver.find_elements_by_xpath("//div[@class='content']/div/small/a")
    twitter_ids = driver.find_elements_by_xpath("//li[@data-item-type='tweet']")
    twitter_usernames = driver.find_elements_by_xpath("//div[@class='content']/div/a/span[2]/b")
    twitter_fullnames = driver.find_elements_by_xpath("//div[@class='content']/div/a/strong")
    twitter_contents = driver.find_elements_by_xpath("//div[@class='content']/p")
    if len(twitter_dates)== 0:
        cur.execute('INSERT INTO twitter '
                    '(url) '
                    'values (%s)', (url))
    for i in range(0, len(twitter_dates)):
        if twitter_dates[i].get_attribute("title") == '':
            cur.execute('INSERT INTO twitter '
                    '(url, id, date, username, fullname, html, text) '
                    'values (%s, %s, %s, %s, %s, %s, %s)',
                    (url[0], twitter_ids[i].get_attribute("data-item-id"),
                     '2000-01-01',
                     twitter_usernames[i].text, twitter_fullnames[i].text,
                     twitter_contents[i].get_attribute('innerHTML'), twitter_contents[i].text))
        else:
            cur.execute('INSERT INTO twitter '
                    '(url, id, date, username, fullname, html, text) '
                    'values (%s, %s, %s, %s, %s, %s, %s)',
                    (url[0], twitter_ids[i].get_attribute("data-item-id"),
                     datetime.datetime.strptime(twitter_dates[i].get_attribute("title"), '%I:%M %p - %d %b %Y').strftime('%Y-%m-%d %H:%M'),
                     twitter_usernames[i].text, twitter_fullnames[i].text,
                     twitter_contents[i].get_attribute('innerHTML'), twitter_contents[i].text))
    con.commit()
    driver.quit()