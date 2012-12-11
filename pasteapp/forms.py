from flask.ext.wtf import (
    Form, TextField, PasswordField, SubmitField, Required, Length,
    ValidationError, EqualTo, TextAreaField, SelectField
)

class RegistrationForm(Form):

    username = TextField('Username', validators = [
        Required(message='The username field is required.'),
        Length(min=3, max=100,
               message='The username must be between 3 and 100 chars long.')])
    email = TextField('Email Address', validators = [
        Required(message='The email address field is required.'),
        Length(min=4, max=100,
               message='The email address must be between 4 and 100 chars long.')])
    password = PasswordField('Password', validators = [
        Required(message='The password field is required.'),
        Length(min=8, message='The password must be at least 8 characters long.'),
        EqualTo('confirmPassword', message='The two passwords must match.')])
    confirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(Form):

    username = TextField('Username', validators = [
        Required(message='You must enter a username.')])
    password = PasswordField('Password', validators = [
        Required(message='You must enter a password.')])
    submit = SubmitField('Login')

class SnippetForm(Form):

    title = TextField('Title', validators = [
        Required(message='You must enter a title.')])
    language = SelectField('Programming Language',
                           choices=[
                               ('bash', 'Bash'),
                               ('c', 'C'),
                               ('csharp', 'C#'),
                               ('clj', 'Clojure'),
                               ('cl', 'Common Lisp'),
                               ('cpp', 'C++'),
                               ('css', 'CSS'),
                               ('erlang', 'Erlang'),
                               ('go', 'Go'),
                               ('haskell', 'Haskell'),
                               ('html', 'HTML'),
                               ('java', 'Java'),
                               ('javascript', 'Javascript'),
                               ('lua', 'Lua'),
                               ('ocaml', 'OCaml'),
                               ('perl', 'Perl'),
                               ('php', 'PHP'),
                               ('text', 'Plain Text'),
                               ('python', 'Python'),
                               ('ruby', 'Ruby'),
                               ('scheme', 'Scheme'),
                               ('sql', 'SQL')])
    raw_content = TextAreaField('Source Code', validators = [
        Required(message='You must enter some source code.')])
    submit = SubmitField('Submit Snippet')
