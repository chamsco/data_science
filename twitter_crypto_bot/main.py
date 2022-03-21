import tweepy
from textblob import TextBlob
from auth.twitter_auth import *



def main():
    api = create_api()

    #Step 3 - Retrieve Tweets
    public_tweets = api.search('Trump')


    #CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
    #and label each one as either 'positive' or 'negative', depending on the sentiment
    #You can decide the sentiment polarity threshold yourself


    for tweet in public_tweets:
        print(tweet.text)

        #Step 4 Perform Sentiment Analysis on Tweets
        analysis = TextBlob(tweet.text)
        print(analysis.sentiment)
        print("")


if __name__ == "__main__":
    main()
