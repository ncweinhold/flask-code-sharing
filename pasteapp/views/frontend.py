from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, abort
)

frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['GET', 'POST'])
def index():
    """
    The root of the application. This should render a template showing
    a form so that the user can create a new anonymous paste, plus should
    show a list of the 10 or so most recently created pastes.
    """
    return render_template('index.html')

@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/paste/<int:paste_id>')
def view_paste(paste_id):
    return render_template('view_paste.html')
