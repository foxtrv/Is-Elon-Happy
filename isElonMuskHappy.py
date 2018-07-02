import json
import requests
import csv
import tweepy
import pandas as pd

# using Sentiment Analysis API found at http://text-processing.com
def sentimentAnalysis(text, dict):
    data = [
        ('text', text),
    ]
    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    data = json.loads(str(response.json()).replace('\'', '"'))
    label = str(data['label'])
    if (label == 'neutral'):
        dict['neutral'] += 1
    elif (label == 'pos'):
        dict['pos'] += 1
    elif (label == 'neg'):
        dict['neg'] += 1



def main():

    # read tweets
    # perform sentiment analysis on them
    # store results (tweet + result) in db

    dict = {"pos": 0,
            "neg": 0,
            "neutral": 0}

    df = pd.read_csv('elonmusk_tweets.csv')
    saved_column = df['text']  # you can also use df['column_name']

    counter = 0
    for row in saved_column:
        # print(row)
        sentimentAnalysis(row, dict)
        print(dict)
        counter += 1

    # check which is highest of the counts, that will be the overall sentiment
    print('Overall, Elon Musk is: ' + max(dict, key=dict.get))


# taken from https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    CONSUMER_KEY = 'secret'
    CONSUMER_SECRET = 'secret'
    ACCESS_TOKEN = 'secret'
    ACCESS_TOKEN_SECRET = 'secret'

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass


if __name__ == "__main__":
    # already ran this
    # get_all_tweets("elonmusk")
    main()
