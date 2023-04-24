# Most liked twitter post for SunuKorite2023 :)
import tweepy
import configparser


config = configparser.ConfigParser()
config.read('config_.ini')

consumer_key = config['Twitter']['consumer_key']
consumer_secret = config['Twitter']['consumer_secret']
access_token = config['Twitter']['access_token']
access_token_secret = config['Twitter']['access_token_secret']

# Connection to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Hashtag to search for...
hashtags = ["#sunukorite2023", "#SunuselfieKorité2023", "SunuSelfieKorite2023"]

# Iterate over each hashtag and search for the top ten most liked tweets
for hashtag in hashtags:
    # Search for tweets with the given hashtag and sort by number of likes
    tweets = api.search_tweets(q=hashtag, count=1000, result_type="popular")

    if tweets:
        # Sort the tweets by number of likes in descending order
        sorted_tweets = sorted(tweets, key=lambda tweet: tweet.favorite_count, reverse=True)

        # Print the top ten most liked tweets
        print("Hashtag:", hashtag)
        for i in range(10):
            if i < len(sorted_tweets):
                tweet = sorted_tweets[i]
                # Extract the name and Twitter handle of the user who posted the tweet
                user_name = tweet.user.name
                user_handle = tweet.user.screen_name
                # Print the tweet's text, number of likes, name, and handle
                print("Tweet", i+1, ":", tweet.text)
                print("Number of likes:", tweet.favorite_count)
                print("Posted by:", user_name, "(" + user_handle + ")\n")
    else:
        print("No popular tweets found for hashtag", hashtag)
