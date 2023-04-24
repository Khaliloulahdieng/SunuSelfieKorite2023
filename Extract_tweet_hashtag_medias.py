import tweepy
import os
import urllib.request
import streamlit as st
from PIL import Image
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

# Define the API instance...
api = tweepy.API(auth, wait_on_rate_limit=True)

# Hashtag to search for...
hashtag = ["#sunukorite2023"]

# Define the folder where the downloaded images will be saved
folder_name = "hashtag_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Define the maximum number of photos to download
max_photos = 10000

# Photo URLs...
photo_urls = set()

# Twitter API, search hashtag
tweets = tweepy.Cursor(api.search_tweets,
                       q=f"#{hashtag} -filter:retweets",
                       tweet_mode='extended',
                       include_entities=True).items(max_photos)

# Photos Download...
for tweet in tweets:
    if "media" in tweet.entities:
        for media in tweet.entities["media"]:
            if media["type"] == "photo" and media["media_url"] not in photo_urls:
                photo_urls.add(media["media_url"])
                image_file = os.path.join(folder_name, f"{tweet.user.screen_name}_{media['id']}.jpg")
                urllib.request.urlretrieve(media["media_url"], image_file)

# Get image files in the folder
image_files = [os.path.join(folder_name, file) for file in os.listdir(folder_name) if file.endswith(".jpg")]

# Number of photos to display in each row
num_cols = 3

# Height of the photos
photo_height = 200

# Images in a grid format...
st.set_page_config(page_title="#SunuSelfieKorite2023", page_icon=":camera:")
st.title("#SunuSelfieKorite2023")

if len(image_files) == 0:
    st.warning("No images found.")
else:
    num_rows = int((len(image_files) - 1) / num_cols) + 1
    for i in range(num_rows):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index = i * num_cols + j
            if index < len(image_files):
                image_file = image_files[index]
                image = Image.open(image_file)
                username = image_file.split("_")[0][1:]
                image_width, image_height = image.size
                image = image.resize((int(image_width/image_height*photo_height), photo_height))
                cols[j].image(image, use_column_width=True, caption=f"@{username}")
