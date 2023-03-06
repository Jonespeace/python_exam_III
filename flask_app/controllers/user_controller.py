from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.sighting_model import Sighting

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def register():
    return render_template('login.html')

@app.route('/create', methods=['POST'])
def create():

    if not User.validate(request.form):
        return redirect('/')

    User.create(request.form)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'uid' in session:
        flash("Access Denied! Need Login Credentials!")
        return redirect('/')

    return render_template('user_page.html', sightings=Sighting.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login_page', methods=['POST'])
def login():

    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect('/dashboard')

    session['uid'] = logged_in_user.id
    session['name'] = logged_in_user.first_name
    return redirect('/dashboard')

@app.route('/secure')
def secure():
    if not 'uid' in session:
        return redirect('/')
    return render_template('user_page.html')