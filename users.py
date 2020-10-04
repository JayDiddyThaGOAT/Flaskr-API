#Name: Jalen Jackson
#Email: jaydiddy72@csu.fullerton.edu
#Project 2: Microblog-Microservices

from flask import request, jsonify, redirect, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import pugsql

# Configure user's microservice to this app
app = FlaskAPI(__name__)

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module('queries/')
queries.connect('sqlite:///database.db')

# Registers a new account
def create_user(username, email, password):
    # Check if all fields are available
    if username is None:
        message = "Missing 'username'"
        raise exceptions.ParseError(message)
    
    if email is None:
        message = "Missing 'email'"
        raise exceptions.ParseError(message)

    if password is None:
        message = "Missing 'password'"
        raise exceptions.ParseError(message)

    # Store fields in a dictionary
    user = {'username': username, 'email': email, 'password': password}

    # Encrypt password then register the user into the database
    try:
        user['password'] = generate_password_hash(user['password'])
        user['user_id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    # Show the user's data in the API
    return user, status.HTTP_201_CREATED, {
        'Location': f'/users/{username}'
    }

# Start following a new user
def add_follower(username, usernameToFollow):

     # Add the usernames in the parameters into the Relationships table
    queries.add_follower(follower_name=username, followed_name=usernameToFollow)

    # Show who the user followed
    return user(usernameToFollow), status.HTTP_201_CREATED, {
        'Location': f'/users/{username}/following?username={usernameToFollow}'
    }

# Stop following a new user
def remove_follower(username, usernameToRemove):
    # Remove the relationship between these two users out of the Relationships table
    queries.remove_follower(follower_name=username, followed_name=usernameToRemove)

    # Show who the user removed
    return user(usernameToRemove), status.HTTP_206_PARTIAL_CONTENT, {
        'Location': f'/users/{username}/following?username={usernameToFollow}'
    }


# Recreate database
@app.cli.command('init')
def init_db():
    with app.app_context():
        # Run the schema query
        db = queries.engine.raw_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        # Populate the Users table with this testing data
        alice = create_user("Alice", "aliceinwonderland@gmail.com", "DownThaRabbitHole")[0]
        bob = create_user("Bob", "bobthebuilder@gmail.com", "CanWeFixIt?")[0]
        karen = create_user("Karen", "MayISpeak@themanger.com", "St0pKarenS0Much!!!")[0]
        charlie = create_user("Charlie", "charliebrown@csu.fullerton.edu", "AnswersArentInTheBack")[0]
        tom = create_user("Tom", "friendswitheveryone@myspace.com", "BringMYSPACEBack2020")[0]
        mary = create_user("Mary", "marypoppin@aol.com", "BLESS_ME_Je$u$")[0]
        
        # Populate the Relationships table with this testing data
        add_follower(alice['username'], mary['username'])
        add_follower(mary['username'], alice['username'])

        add_follower(karen['username'], alice['username'])
        add_follower(karen['username'], mary['username'])

        add_follower(bob['username'], charlie['username'])
        add_follower(charlie['username'], tom['username'])

        add_follower(tom['username'], alice['username'])
        add_follower(tom['username'], bob['username'])
        add_follower(tom['username'], karen['username'])
        add_follower(tom['username'], charlie['username'])
        add_follower(tom['username'], mary['username'])

# Display all of the users in the Users table. This page also creates new users
@app.route('/', methods=['GET', 'POST'])
def all_users():
    if request.method == 'POST':
        create_user(request.data['username'], request.data['email'], request.data['password'])
    
    return list(queries.all_users())

# Find user with the username in the URL then display its data if found
@app.route('/<string:username>', methods=['GET'])
def user(username):
    user = queries.user_by_username(username=username)
    if user:
        return user
    else:
        raise exceptions.NotFound()

# Returns true if the supplied password matches the hashed password stored for that username in the database. 
@app.route('/<string:username>/authenticate', methods=['GET'])
def authenticate_user(username):
    try:
        user_password = user(username)['password']
        supplied_password = request.args.get('password')

        is_authenicated = check_password_hash(user_password, supplied_password)
        if is_authenicated:
            return {"is_authenicated" : True}, status.HTTP_302_FOUND
        else:
            return {"is_autenicated": False}, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {"is_autenicated": "Password not found" }, status.HTTP_409_CONFLICT

# Page where users can add, remove, or see who they follow 
@app.route('/<string:username>/following/', methods=['GET', 'POST', 'DELETE'])
def following(username):
    if request.method == 'POST' and 'username' in request.data:
        usernameToFollow = request.data.get('username')
        add_follower(username, usernameToFollow)
    elif request.method == 'DELETE' and 'username' in request.args:
        usernameToRemove = request.args.get('username')
        remove_follower(username, usernameToRemove)

    return list(queries.show_following(follower_name=username))