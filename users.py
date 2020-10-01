from flask import request, jsonify
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import pugsql

app = FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries.engine.raw_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    
def create_user(user):
    posted_fields = {*user.keys()}
    required_fields = {'username', 'email', 'password'}

    if not required_fields <= posted_fields:
        message = f'Missing fields: {required_fields - posted_fields}'
        raise exceptions.ParseError(message)
    try:
        user['password'] = generate_password_hash(user['password'])
        user['user_id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return user, status.HTTP_201_CREATED, {
        'Location': f'/users/{user["user_id"]}'
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

@app.route('/users/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data)

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