from urllib.parse import urlparse
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app import app
from app import login_manager
from forms import LoginForm

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash("Successfully logged in as %s." % form.user.email, "success")
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for("homepage")
            return redirect(next_page)
    else:
        form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    next_page = request.args.get("next")
    if not next_page or urlparse(next_page).netloc != '':
        next_page = url_for("homepage")
    return redirect(next_page)
