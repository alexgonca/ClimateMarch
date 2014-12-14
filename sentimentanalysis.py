import numpy as np
import MySQLdb as myDB
import ConfigParser

def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row
    
    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    return happy_log_probs, sad_log_probs

def classifySentiment(words, happy_log_probs, sad_log_probs):
    # Get the log-probability of each word under each sentiment
    happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
    sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
    tweet_happy_log_prob = np.sum(happy_probs)
    tweet_sad_log_prob = np.sum(sad_probs)

    # Calculate the probability of the tweet belonging to each sentiment
    prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
    prob_sad = 1 - prob_happy

    return prob_happy, prob_sad

def main():
    # We load in the list of words and their log probabilities
    happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')

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
            'where url = "http://www.breitbart.com/Big-Government/2014/09/22/Al-Gore-Leaves-Climate-March-in-Chevy-Suburban-SUV"'

    cur.execute(query)
    tweets = cur.fetchall()
    text = ''
    total_sum_happy = 0
    total_sum_sad = 0

    for tweet in tweets:
        tweet_tuple = tweet[0].split()
        #print tweet_tuple
        tweet_happy_prob, tweet_sad_prob = classifySentiment(tweet_tuple, happy_log_probs, sad_log_probs)
        #print tweet_happy_prob
        total_sum_happy += tweet_happy_prob
        total_sum_sad += tweet_sad_prob

    print "The probability that url is happy is ", total_sum_happy / len(tweets), "and the probability that it is sad is ", total_sum_sad / len(tweets)

if __name__ == '__main__':
    main()
