from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, abort,
    session
)

from pasteapp.forms import RegistrationForm, LoginForm, SnippetForm
from pasteapp.database import User, db_session, Snippet

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    err = None
    if form.validate_on_submit():
        if username_taken(form.username.data):
            return render_template('register.html',
                                   form=form,
                                   err='Username has already been taken.')
        if email_taken(form.email.data):
            return render_template('register.html',
                                   form=form,
                                   err='Email address has already been used.')
        user = User(form.username.data,
                    form.email.data,
                    form.password.data)
        db_session.add(user)
        db_session.commit()
        flash('You have successfully registered and can now log in.')
        return redirect(url_for('frontend.login'))
    return render_template('register.html', form=form, err=err)

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    err = None
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if not user or not user.check_bcrypt_hash(form.password.data):
            err = "Invalid username or password"
            return render_template('login.html', form=form, err=err)
        else:
            session['user_id'] = user.id
            flash('You have logged in successfully.')
            return redirect(url_for('frontend.dashboard'))
    return render_template('login.html', form=form, err=err)

@frontend.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect(url_for('frontend.index'))
    flash('Logged out successfully')
    session.pop('user_id', None)
    return redirect(url_for('frontend.index'))

@frontend.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must log in first')
        return redirect(url_for('frontend.login'))
    else:
        return render_template('dashboard.html')

@frontend.route('/snippet/new', methods=['GET', 'POST'])
def new_snippet():
    if 'user_id' not in session:
        flash('You must log in first')
        return redirect(url_for('frontend.login'))
    form = SnippetForm()
    if form.validate_on_submit():
        snippet = Snippet(form.title.data,
                          form.language.data,
                          session['user_id'],
                          form.raw_content.data)
        db_session.add(snippet)
        db_session.commit()
        flash('The new snippet has been successfully created.')
        return redirect(url_for('frontend.view_snippet', snippet_id=snippet.id))
    return render_template('new_snippet.html', form=form)

@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/snippet/view/<int:snippet_id>')
def view_snippet(snippet_id):
    snippet = Snippet.query.filter(Snippet.id == snippet_id).first()
    if not snippet:
        return abort(404)
    return render_template('view_snippet.html', snippet=snippet)

def username_taken(username):
    return User.query.filter(User.username == username).first()

def email_taken(email):
    return User.query.filter(User.email == email).first()
