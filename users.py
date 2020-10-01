from flask_api import FlaskAPI
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