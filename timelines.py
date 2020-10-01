import click

from flask import Flask, g
from users import get_db

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

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