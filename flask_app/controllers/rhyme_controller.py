from flask_app import app

# import all the features we need to run our app routes
from flask import render_template , redirect, request, session, flash 

# import all the models we will need to access for class/ static methods 
from flask_app.models.user_model import User
from flask_app.models.rhyme_model import Rhyme

@app.route('/add_entry')
def add_entry():
    if 'user_id' not in session:
        flash('You must register or log in to view content.')
        return redirect('/')
    user_id = session['user_id']
    return render_template('add_entry.html', user_id = user_id)

@app.route('/add_entry_post', methods=['POST'])
def add_entry_post():
    if not Rhyme.validate_create(request.form):
        return redirect('/add_entry')
    Rhyme.add_rhyme(request.form)
    return redirect('/dashboard')

@app.route('/edit_entry/<int:rhyme_id>')
def edit_entry(rhyme_id):
    if 'user_id' not in session:
        flash('You must register or log in to view content.')
        return redirect('/')
    data = {
        'id' : rhyme_id
    }
    rhymes = Rhyme.get_one_rhyme(data)
    rhyme = rhymes[0]
    return render_template('edit_entries.html', rhyme = rhyme)

@app.route('/edit_entry_post/<int:id>', methods=['POST'])
def edit_entry_post(id):
    if not Rhyme.validate_create(request.form):
        return redirect(f'/edit_entry/{id}')
    data = {
        'id': id,
        'title': request.form['title'],
        'type': request.form['type'],
        'content': request.form['content'],
    }
    Rhyme.edit_rhyme(data)
    return redirect(f'/edit_entry/{id}')


