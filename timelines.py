from flask_api import FlaskAPI

import pugsql
from users import queries

app = FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')