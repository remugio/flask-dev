import user
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from flask.ext.mysql import MySQL
from flask.ext.bcrypt import Bcrypt

##############
# App Config #
##############
DEBUG = True
SECRET_KEY = 'development key'

# Flask-MySQL configuration
MYSQL_DATABASE_HOST = 'localhost'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_DB = 'flaskr'
MYSQL_DATABASE_USER = 'admin'
MYSQL_DATABASE_PASSWORD = 'default'

##########################
# create the application #
##########################
mysql = MySQL()
app = Flask(__name__)
app.config.from_object(__name__)
mysql.init_app(app)
# TODO this doesn't actually need to be init'ed with app
bcrypt = Bcrypt(app)

###########################
# Application controllers #
###########################
# view the entries
@app.route('/')
def show_entries():
    cur = g.db.cursor()
    cur.execute('SELECT title, text FROM entries ORDER BY id DESC')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# create an entry
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.cursor().execute('INSERT INTO entries (title, text) values (%s, %s)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# create a user
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    error = None
    if request.method == 'POST':
        # TODO validation
        username = request.form['username']
        password = request.form['password']
        if user.username_taken(g.db, username):
            error = 'Username taken'
        else:
            passhash = pass_hash(password)
            user.create(g.db, username, passhash)
            flash('User account created')
            return redirect(url_for('login'))
    return render_template('create_user.html', error=error)

# login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        curr_user = user.get_one_by_username(g.db, username)
        if curr_user is None:
            error = 'No user!!!'
        elif not pass_match(password, curr_user.passhash):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

####################
# Security helpers #
####################
# TODO these should probably be in another module
BCRYPT_ROUNDS = 15
def pass_hash(password):
    return bcrypt.generate_password_hash(password, BCRYPT_ROUNDS)

def pass_match(password, passhash):
    return bcrypt.check_password_hash(passhash, password)

##############
# DB helpers #
##############
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.mysql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return mysql.connect()

def get_db():
    return mysql.get_db()

# before and after app requests, do the following
@app.before_request
def before_request():
    g.db = get_db()

# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()

###############
# entry point #
###############
if __name__ == '__main__':
    app.run()
