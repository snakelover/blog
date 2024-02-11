import os
import sys
sys.path.append(os.getcwd())
# print(sys.path)
from main import app, db  # noqa

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
