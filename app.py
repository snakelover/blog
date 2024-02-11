from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import sys
# print(sys.path)
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
