#Name: Jalen Jackson
#Email: jaydiddy72@csu.fullerton.edu
#Project 2: Microblog-Microservices

from flask import request
from flask_api import FlaskAPI
import pugsql

from users import queries

from time import sleep

from random import randrange
from datetime import datetime

# Configure timelines microservice to this app
app = FlaskAPI(__name__)

# Post a new tweet
def post_tweet(username, text, delay = 0):
    if delay > 0:
        print(f"Posting {username}'s tweet in {delay} seconds")
        sleep(delay)

    queries.post_tweet(author_name=username, tweet=text)
    
# Initialize user's timelines present in the Users table (Run init in users microservice before running this one)
@app.cli.command('init')
def init_timelines():
    post_tweet("Bob", "If you don't like toenails, you probably shouldn't look at your feet", randrange(1, 5))
    post_tweet("Charlie", "@Bob wonders if he should appreciate his toenail collection", randrange(1, 5))
    post_tweet("Mary", "It dawned on her that others could make her happier, but only she could make herself happy", randrange(1, 5))
    post_tweet("Alice", "People keep telling me 'orange' but I still prefer 'pink'", randrange(1, 5))
    post_tweet("Mary", "@Alice Of course, she loves her pink bunny slippers.", randrange(1, 5))
    post_tweet("Tom", "My role model is hard labor, and I want to drink beer. Let there be more dreamers, my friend. #coolism #randomtweet", randrange(1, 5))
    post_tweet("Karen", "I'm angry: when people ask me what's up, and I point, they groan.", randrange(1, 5))
    post_tweet("Bob", "I ate a sock because people on the Internet told me to", randrange(1, 5))
    post_tweet("Mary", "@Karen You have every right to be angry, but that doesn't give you the right to be mean", randrange(1, 5))
    post_tweet("Karen", "@Mary Don't piss in my garden and tell me you're trying to help my plants gro.", randrange(1, 5))
    post_tweet("Charlie", "Traveling became almost extinct during the pandemic", randrange(1, 5))
    post_tweet("Charlie", "Now I need to ponder my existence and ask myself if I'm truly real", randrange(1, 5))
    post_tweet("Alice", "@Tom Seek success, but always be prepared for random cats.", randrange(1, 5))
    post_tweet("Tom", "@Alice How funny is this - the cats love to do the people watching, never mind we all stop to look at the cats!", randrange(1, 5))
    post_tweet("Karen", "Sometimes you have to just give up and win by cheating.", randrange(1, 5))
    post_tweet("Mary", "I am counting my calories, yet I really want dessert", randrange(1, 5))
    post_tweet("Charlie", "I caught my dog rustling through my gym bag", randrange(1, 5))
    post_tweet("Bob", "I covered my friend in baby oil.", randrange(1, 5))
    post_tweet("Alice", "I really want to go to work, but I am too sick to drive.", randrange(1, 5))
    post_tweet("Tom", "The crowd yells and screams for more memes", randrange(1, 5))
    post_tweet("Karen", "I was very proud of my name throughout high school but today- I couldn’t be any different to what my name was.", randrange(1, 5))
    post_tweet("Bob", "Love is not like pizza!!!", randrange(1, 5))
    post_tweet("Mary", "My Mum tries to be cool by saying that she likes all the same things that I do", randrange(1, 5))
    post_tweet("Karen", "Every manager should be able to recite at least ten nursery rhymes backward", randrange(1, 5))
    post_tweet("Tom", "It's not possible to convince a monkey to give you a banana by promising it infinite bananas when they die", randrange(1, 5))
    post_tweet("Alice", "When I cook spaghetti, I like to boil it a few minutes past al dente so the noodles are super slippery", randrange(1, 5))

# Returns recent tweets from all users
@app.route('/', methods=['GET'])
def get_public_timeline():
    return list(queries.public_timeline())

# Returns recent tweets from all users that this user follows.
@app.route('/<string:username>/home', methods=['GET'])
def get_home_timeline(username):
    return list(queries.home_timeline(follower_name=username))

# Returns recent tweets from a user. This page where user can post their tweets
@app.route('/<string:username>/user', methods=['GET', 'POST'])
def get_user_timeline(username):
    if request.method == 'POST':
        post_tweet(username, request.data['tweet'])

    return list(queries.user_timeline(username=username))
