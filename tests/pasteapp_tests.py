from os.path import abspath
import unittest
from pasteapp import create_app
from pasteapp.database import db_session, init_db, clear_db, User

class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.app = create_app(abspath('config_testing.py'))
        super(TestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        init_db()
        user = User('test_user', 'test_user@example.com', 'password')
        db_session.add(user)
        db_session.commit()

    def tearDown(self):
        clear_db()
        self.ctx.pop()

class HomePageTest(TestCase):

    def test_home_page_rendering(self):
        rv = self.client.get('/')
        assert 'Simple Code Sharing' in rv.data

class AboutPageTestCase(TestCase):

    def test_about_page_rendering(self):
        rv = self.client.get('/about')
        assert 'About' in rv.data

class RegisterPageTestCase(TestCase):

    def register(self, username, email, password,
                 confirm, redirect=True):
        """
        Helper function to make a post request to the register method.
        Saves on duplication in the tests.
        """
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirmPassword': confirm
        }, follow_redirects=redirect)

    def test_register_page_rendering(self):
        rv = self.client.get('/register')
        assert 'Register Now' in rv.data

    def test_login_message_if_account_holder(self):
        """
        This test checks that the user can go straight to the login page if
        they already have an account.
        """

        msg = 'Already have an account? Log in now.'
        rv = self.client.get('/register')
        assert msg in rv.data

    def test_username_field(self):
        """
        This test checks that the registration form has a username field.
        """

        rv = self.client.get('/register')
        assert 'Username' in rv.data

    def test_email_address_field(self):
        """
        This test checks that the registration form has an email address
        field.
        """

        rv = self.client.get('/register')
        assert 'Email Address' in rv.data

    def test_password_field(self):
        """
        This test checks that the registration form has a password field.
        """

        rv = self.client.get('/register')
        assert 'Password' in rv.data

    def test_confirm_password_field(self):
        """
        This test checks that the registration form has a field to confirm
        the password that the user entered.
        """

        rv = self.client.get('/register')
        assert 'Confirm Password' in rv.data

    def test_valid_user_registration(self):
        """
        This test checks that a user is successfully registered if they provide \
        valid user information during registration.
        """
        msg = 'You have successfully registered and can now log in.'
        # Checking the boundary maximum length here for the username
        rv = self.register('a'*100, 'mister_test@example.com',
                           'somesecurepassword', 'somesecurepassword')
        assert msg in rv.data

    def test_too_short_username_registration(self):
        """
        This test checks that the correct error message is displayed if the
        user attempts to register using a username that is too short.
        """
        errorMsg = 'The username must be between 3 and 100 chars long.'
        rv = self.register('bb', 'mister_test@example.com',
                           'password', 'password')
        assert errorMsg in rv.data

    def test_too_long_username_registration(self):
        """
        This test checks that the correct error message is displayed if the
        user attempts to register using a username that is too long.
        """
        errorMsg = 'The username must be between 3 and 100 chars long.'
        rv = self.register('a'*101, 'mister_test@example.com',
                           'password', 'password')
        assert errorMsg in rv.data

    def test_username_required_registration(self):
        """
        This test checks that an error message is displayed if the user
        attempts to register without providing a username.
        """
        errorMsg = 'The username field is required.'
        rv = self.register('', 'mister_test@example.com', 'password',
                           'password')
        assert errorMsg in rv.data

    def test_email_required_registration(self):
        """
        This test checks that an error message is displayed if the user tries
        to register without providing an email address.
        """
        errorMsg = 'The email address field is required.'
        rv = self.register('mister_test', '', 'password', 'password')
        assert errorMsg in rv.data

    def test_email_too_short_registration(self):
        """
        This test checks that an error message is displayed if the user tries
        to register with an email address that is too short.
        """
        errorMsg = 'The email address must be between 4 and 100 chars long.'
        rv = self.register('mister_test', 'a@b', 'password', 'password')
        assert errorMsg in rv.data

    def test_email_too_long_registration(self):
        """
        This test checks that an error message is displayed if the user tries
        to register with an email address that is too long.
        """
        errorMsg = 'The email address must be between 4 and 100 chars long.'
        rv = self.register('mister_test', 'a'*101, 'password', 'password')
        assert errorMsg in rv.data

    def test_password_required_registration(self):
        """
        This test checks that an error message is displayed if the user tries
        to register without providing a password.
        """
        errorMsg = 'The password field is required.'
        rv = self.register('mister_test', 'mister_test@example.com',
                           '', 'password')
        assert errorMsg in rv.data

    def test_passwords_must_match_registration(self):
        """
        This test checks that the correct error message is displayed if the
        two passwords do not match.
        """
        errorMsg = 'The two passwords must match.'
        rv = self.register('mister_test', 'mister_test@example.com',
                           'password1', 'password2')
        assert errorMsg in rv.data

    def test_password_length_registration(self):
        """
        This test checks that the correct error message is displayed if the
        user tries to register using a short password.
        """
        errorMsg = 'The password must be at least 8 characters long.'
        rv = self.register('mister_test', 'mister_test@example.com',
                           '1234567', '1234567')
        assert errorMsg in rv.data

    def test_duplicate_username_registration(self):
        """
        This test checks that the correct error message is displayed if the
        user tries to register using a username that is already in use.
        """
        errorMsg = 'Username has already been taken.'
        rv = self.register('test_user', 'user@example.com', 'password',
                           'password')
        assert errorMsg in rv.data

    def test_duplicate_email_registration(self):
        """
        This test checks that the correct error message is displayed if the
        user tries to register using a username that is already in use.
        """
        errorMsg = 'Email address has already been used.'
        rv = self.register('mister_test', 'test_user@example.com', 'password',
                           'password')
        assert errorMsg in rv.data

class LoginPageTestCase(TestCase):

    def login(self, username, password, redirect=True):
        """
        Helper method to make a login post request.
        """
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=redirect)

    def logout(self, redirect=True):
        return self.client.get('/logout', follow_redirects=redirect)

    def test_login_valid_credentials(self):
        msg = 'You have logged in successfully.'
        rv = self.login('test_user', 'password')
        assert msg in rv.data

    def test_login_wrong_username(self):
        msg = 'Invalid username or password'
        rv = self.login('test', 'password')
        assert msg in rv.data

    def test_login_wrong_password(self):
        msg = 'Invalid username or password'
        rv = self.login('test_user', 'wrong')
        assert msg in rv.data

    def test_logout_not_logged_in(self):
        msg = 'Logged out successfully'
        rv = self.logout()
        assert msg not in rv.data

    def test_logout_logged_in(self):
        msg = 'Logged out successfully'
        self.login('test_user', 'password')
        rv = self.logout()
        assert msg in rv.data

    def test_dashboard_only_when_logged_in(self):
        rv = self.client.get('/dashboard', follow_redirects=True)
        assert 'You must log in first' in rv.data

    def test_dashboard_logged_in(self):
        self.login('test_user', 'password')
        rv = self.client.get('/dashboard', follow_redirects=True)
        assert 'Your Overview' in rv.data

class SnippetTestCase(TestCase):

    def create_snippet(self, title, language, raw_content, redirect=True):
        """
        Helper function.
        """
        return self.client.post('/snippet/new', data={
            'title': title,
            'language': language,
            'raw_content': raw_content
        }, follow_redirects=redirect)

    def login(self, username, password, redirect=True):
        """
        Helper method to make a login post request.
        """
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=redirect)

    def logout(self, redirect=True):
        return self.client.get('/logout', follow_redirects=redirect)

    def test_create_snippet_successfully(self):
        msg = 'The new snippet has been successfully created.'
        self.login('test_user', 'password')
        rv = self.create_snippet("Python Hello World", "python",
                                 "print 'hello world'")
        assert msg in rv.data

    def test_create_snippet_redirect(self):
        """
        This test checks that after a snippet has been successfully created
        the page is redirected to the url referring to the newly created
        snippet.
        """
        self.login('test_user', 'password')
        rv = self.create_snippet("Ruby Hello World", "ruby",
                                 "puts 'Hello World'")
        assert "Ruby Hello World" in rv.data

    def test_create_snippet_no_content(self):
        msg = 'You must enter some source code.'
        self.login('test_user', 'password')
        rv = self.create_snippet('No content', 'php', '')
        assert msg in rv.data

    def test_create_snippet_no_title(self):
        msg = 'You must enter a title.'
        self.login('test_user', 'password')
        rv = self.create_snippet('', 'scheme', '(list 1 2 3)')
        assert msg in rv.data
