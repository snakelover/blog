import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
import models
import views

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
    app.run()
