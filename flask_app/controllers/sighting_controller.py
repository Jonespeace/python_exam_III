from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.sighting_model import Sighting

@app.route('/new')
def new():
    return render_template('new_sighting.html', sightings=Sighting.get_all())

@app.route('/create/sighting', methods=['POST'])
def create_sighting():
    # print(request.form)
    if not Sighting.validate_sighting(request.form):
        return redirect('/new')
    data ={
        'location' : request.form['location'],
        'what_happened' : request.form['what_happened'],
        'date' : request.form['date'],
        'how_many' : request.form['how_many'],
        'user_id' : session['uid']
    }
    sighting_id = Sighting.save(data)
    return redirect('/dashboard')


@app.route('/sighting/show/<int:id>')
def show(id):
    data ={
        "id":id
    }
    return render_template("show_sighting.html", sighting=Sighting.get_one_with_user(data))


@app.route('/sighting/edit/<int:id>')
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit_sighting.html", sighting=Sighting.get_one_with_user(data))


@app.route('/sighting/update', methods=['POST'])
def update():
    print(request.form)
    Sighting.update(request.form)
    return redirect('/dashboard')


@app.route('/sighting/delete/<int:id>')
def delete(id):
    data={
        "id":id
    }
    Sighting.delete(data)
    return redirect('/dashboard')