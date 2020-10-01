import sqlite3

import click
from flask import Flask, g

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._users_database = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
    
    return db

@app.teardown_appcontext
def close_users_db(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.cli.command("init")
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode("utf8"))
        db.commit()
    
    click.echo('Initalized database')