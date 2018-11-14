from flask import render_template, request

from app import app


@app.route('/')
def homepage():
    name = request.args.get('name')
    return render_template('homepage.html', name=name)
