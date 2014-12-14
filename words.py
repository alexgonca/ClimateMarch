import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import MySQLdb as myDB
import ConfigParser
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

config = ConfigParser.ConfigParser()
config.read('info.config')
con = myDB.connect(config.get('db', 'host'), config.get('db', 'username'),
                   config.get('db', 'password'), config.get('db', 'schema'))
con.set_character_set('utf8mb4')
cur = con.cursor()
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8mb4;')
cur.execute('SET character_set_connection=utf8mb4;')

query = 'select text ' \
        'from twitter ' \
    'where url ="climate-science-is-not-settled"'
#        'where url = "http://www.nytimes.com/2014/09/22/nyregion/new-york-city-climate-change-march.html"'
#        'where url = "http://gothamist.com/2014/09/22/climate_march_trash.php"'


cur.execute(query)
tweets = cur.fetchall()
text = ''

for tweet in tweets:
    text = " || " + text + tweet[0]

text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
text = re.sub(r"([@])(\w+)", '', text)
text = text.lower()
text = text.replace("obama's", "obama")

stopwords = STOPWORDS
stopwords.add("koonin")
stopwords.add("science")
stopwords.add("settled")
stopwords.add("climate")
stopwords.add("say")
stopwords.add("via")
stopwords.add("says")
stopwords.add("wsj")
stopwords.add("steven")
stopwords.add("koonin")
stopwords.add("change")
stopwords.add("wall")
stopwords.add("street")
stopwords.add("journal")
stopwords.add("read")
stopwords.add("write")
stopwords.add("article")
stopwords.add("climatechange")
stopwords.add("globalwarming")
stopwords.add("settled'")
stopwords.add("make")
stopwords.add("write")
stopwords.add("steve")
stopwords.add("warming")
stopwords.add("writes")
stopwords.add("e")

#testimonial = TextBlob(text.decode('utf-8'), analyzer=NaiveBayesAnalyzer())
#print testimonial.sentiment

wordcloud = WordCloud(width=2000, height=1000, stopwords=stopwords).generate(text)
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")
plt.show()