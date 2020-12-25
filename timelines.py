#Name: Jalen Jackson
#Email: jaydiddy72@csu.fullerton.edu
#Project 6: Caching

from flask import request, make_response
from flask_api import FlaskAPI, status, exceptions
from flask_caching import Cache
import pugsql

from users import queries, following

from time import sleep, mktime, strptime
from random import randrange

from wsgiref.handlers import format_date_time
from datetime import datetime

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 120
}

# Configure timelines microservice to this app
app = FlaskAPI(__name__)

# Tell Falsk to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

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
# Added HTTP caching to ensure safety returning posts slightly behind the real-time activity on the site.
@app.route('/', methods=['GET'])
def get_public_timeline():
    # Check for an If-Modified-Since: request header 
    if_modified_since_exists = 'If-Modified-Since' in request.headers 

    # Query the database for the public timeline
    resp = make_response(list(queries.public_timeline()))

    # Add a Last-Modified: header to responses containing the current date. 
    now = datetime.now()
    stamp = mktime(now.timetuple())
    resp.headers['Last-Modified'] = format_date_time(stamp)
    
    # If the header is present, check it against the current time and return HTTP 304 if the difference is less than 5 minutes.
    if if_modified_since_exists:
        # Convert the headers from string into datetimes
        http_time_format = '%a, %d %b %Y %H:%M:%S GMT'
        last_modified = datetime.strptime(resp.headers['Last-Modified'], http_time_format)
        if_modified_since = datetime.strptime(request.headers['If-Modified-Since'], http_time_format)

        # Calculate minutes passed between last modified and if_modified_since timestamp
        minutes_passed = (last_modified - if_modified_since).total_seconds() / 60.0
        if minutes_passed < 5:
            resp.status_code = status.HTTP_304_NOT_MODIFIED
        else:
            resp.status_code = status.HTTP_200_OK
    else:
        resp.status_code = status.HTTP_200_OK

    
    return resp

# Returns recent tweets from all users that this user follows.
# Those tweets are returned from of their cache
@app.route('/<string:username>/home', methods=['GET'])
def get_home_timeline(username):
    # Store up to 25 tweets in this list
    home_timeline = []

    # Iterate through each user who is followed by user with username
    for user in following(username):
        # Iterate through those user's timelines and add it to home timeline list
        user_timeline = get_user_timeline(user['username'])
        for tweet in user_timeline:
            home_timeline.append(tweet)
    
    # Return the home timeline sorted by when the tweet was created in descending order
    return sorted(home_timeline, key = lambda tweet : mktime(strptime(tweet['created'], '%Y-%m-%d %H:%M:%S')), reverse=True)[:25]

# Returns recent tweets from a user. This page where user can preturn list(queries.user_timeline(username=username))ost their tweets
@app.route('/<string:username>/user', methods=['GET', 'POST'])
def get_user_timeline(username):
    if request.method == 'POST':
        post_tweet(username, request.data['tweet'])
        cache.set(username, list(queries.user_timeline(username=username)))
        app.logger.debug(f'Updated {username}\'s timeline in cache')
        return cache.get(username)

    # If the username is not in the cache, put the user's timeline into it
    if cache.get(username) == None:
        cache.set(username, list(queries.user_timeline(username=username)))
        app.logger.debug(f'Added {username}\'s timeline into cache')
    else:
        app.logger.debug(f'Retreived {username}\'s timeline from cache')
    
    # Otherwise just return the user's timeline in the cache
    return cache.get(username)