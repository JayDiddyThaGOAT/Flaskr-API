from flask import request, jsonify, redirect, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import pugsql

# Configure microservice to app for showing user's data
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

# Display users table that match the parameters
def filter_users(query_parameters):
    # Get the user's parameters and store them in their variables
    user_id = query_parameters.get('user_id')
    username = query_parameters.get('username')
    email = query_parameters.get('email')

    # Add valid query parameters into a list
    query = "SELECT * FROM users WHERE"
    to_filter = []

    if user_id:
        query += ' user_id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if email:
        query += ' email=? AND'
        to_filter.append(email)

    # Run error if query parameter doesn't exist
    if not (user_id or username or email):
        raise exceptions.NotFound()
    
    # In the query, replace final ' AND' w/ semi-colon, then run it
    query = query[:-4] + ';'
    results = queries.engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))

# Start following a new user
def add_follower(username, usernameToFollow):

     # Add the usernames in the parameters into the Relationships table
    queries.add_follower(follower_name=username, followed_name=usernameToFollow)

    # Show who the user followed
    return user(usernameToFollow), status.HTTP_201_CREATED, {
        'Location': f'/users/{username}/following/add'
    }

# Stop following a new user
def remove_follower(username, usernameToRemove):
    # Remove the relationship between these two users out of the Relationships table
    queries.remove_follower(follower_name=username, followed_name=usernameToRemove)

    # Show who the user removed
    return user(usernameToRemove), status.HTTP_206_PARTIAL_CONTENT, {
        'Location': f'/users/{username}/following/remove'
    }

# Display the user's (with the matching username) following list
def show_following(username):
    return list(queries.show_following(follower_name=username))

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

# Display all of the users in the Users table
@app.route('/users/all', methods=['GET'])
def all_users():
    return list(queries.all_users())

# Homepage where the users microservice functions are run
@app.route('/users', methods=['GET', 'POST'])
def users():
    # Filter Users table with arguments requsted
    if request.method == 'GET':
        return filter_users(request.args)

    # Add user to the Users table with the requested data
    elif request.method == 'POST':
        return create_user(request.data['username'], request.data['email'], request.data['password'])

# Find user with the username in the URL then display its data if found
@app.route('/users/<string:username>', methods=['GET'])
def user(username):
    user = queries.user_by_username(username=username)
    if user:
        return user
    else:
        raise exceptions.NotFound()

# Returns true if the supplied password matches the hashed password stored for that username in the database. 
@app.route('/users/<string:username>/auth/', methods=['GET', 'POST'])
def authenicate_user(username):
    if request.method == 'POST':
        try:
            user_password = user(username)['password']
            is_authenicated = check_password_hash(user_password, request.data['password'])
            if is_authenicated:
                return {"is_authenicated" : True}, status.HTTP_302_FOUND
            else:
                return {"is_autenicated": False}, status.HTTP_404_NOT_FOUND
        except Exception as e:
            return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return {"is_authenicated": "Type in a password in POST"}

# Page where users can add followers (Displays user's follow list by default)
@app.route('/users/<string:username>/following/add', methods=['GET', 'POST'])
def add_followers(username):
    if request.method == 'POST':
        return add_follower(username, request.data['username'])
    elif request.method == 'GET':
        return show_following(username)

# Page where users can remove followers (Displays user's follow list by default)
@app.route('/users/<string:username>/following/remove', methods=['GET', 'POST'])
def remove_followers(username):
    if request.method == 'POST':
        return remove_follower(username, request.data['username'])
    elif request.method == 'GET':
        return show_following(username)