from flask import request, jsonify, redirect, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import pugsql

app = FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])
    
def create_user(username, email, password):
    if username is None:
        message = "Missing 'username'"
        raise exceptions.ParseError(message)
    
    if email is None:
        message = "Missing 'email'"
        raise exceptions.ParseError(message)

    if password is None:
        message = "Missing 'password'"
        raise exceptions.ParseError(message)

    user = {'username': username, 'email': email, 'password': password}

    try:
        user['password'] = generate_password_hash(user['password'])
        user['user_id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return user, status.HTTP_201_CREATED, {
        'Location': f'/users/{username}'
    }

def filter_users(query_parameters):
    user_id = query_parameters.get('user_id')
    username = query_parameters.get('username')
    email = query_parameters.get('email')

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

    if not (user_id or username or email):
        raise exceptions.NotFound()
    
    query = query[:-4] + ';'
    results = queries.engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))

def add_follower(username, usernameToFollow):
    userFollowing = user(username)
    userToFollow = user(usernameToFollow)
    queries.add_follower(follower_id=userFollowing['user_id'], followed_id=userToFollow['user_id'])

    return userToFollow, status.HTTP_201_CREATED, {
        'Location': f'/users/{username}/following/add'
    }

def remove_follower(username, usernameToRemove):
    userRemoving = user(username)
    userToRemove = user(usernameToRemove)
    queries.remove_follower(follower_id=userRemoving['user_id'], followed_id=userToRemove['user_id'])

    return userToRemove, status.HTTP_206_PARTIAL_CONTENT, {
        'Location': f'/users/{username}/following/remove'
    }

def show_following(username):
    return list(queries.show_following(follower_id=user(username)['user_id'])) 

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries.engine.raw_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        alice = create_user("Alice", "aliceinwonderland@gmail.com", "DownThaRabbitHole")[0]
        bob = create_user("Bob", "bobthebuilder@gmail.com", "CanWeFixIt?")[0]
        karen = create_user("Karen", "MayISpeak@themanger.com", "St0pKarenS0Much!!!")[0]
        charlie = create_user("Charlie", "charliebrown@csu.fullerton.edu", "AnswersArentInTheBack")[0]
        tom = create_user("Tom", "friendswitheveryone@myspace.com", "BringMYSPACEBack2020")[0]
        mary = create_user("Mary", "marypoppin@aol.com", "BLESS_ME_Je$u$")[0]
        

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


@app.route('/users/all', methods=['GET'])
def all_users():
    return list(queries.all_users())

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data['username'], request.data['email'], request.data['password'])

@app.route('/users/<string:username>', methods=['GET'])
def user(username):
    user = queries.user_by_username(username=username)
    if user:
        return user
    else:
        raise exceptions.NotFound()

@app.route('/users/<string:username>/auth/<string:password>', methods=['GET'])
def authenicate_user(username, password):
    user_password = user(username)['password']
    is_authenicated = check_password_hash(user_password, password)
    return jsonify(is_authenicated)

@app.route('/users/<string:username>/following/add', methods=['GET', 'POST'])
def add_followers(username):
    if request.method == 'POST':
        return add_follower(username, request.data['username'])
    elif request.method == 'GET':
        return show_following(username)

@app.route('/users/<string:username>/following/remove', methods=['GET', 'POST'])
def remove_followers(username):
    if request.method == 'POST':
        return remove_follower(username, request.data['username'])
    elif request.method == 'GET':
        return show_following(username)