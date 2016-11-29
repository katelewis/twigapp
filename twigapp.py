# all the imports
import os
import boto3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from boto3.dynamodb.conditions import Key, Attr

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    return dynamodb

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'dynamodb'):
        g.dynamodb = connect_db()
    return g.dynamodb

def get_current_table():
	db = get_db()
	table = db.Table('CurrentTable')
	return table

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    pass

@app.route('/')
def show_entries():
    table = get_current_table()
    entries = table.query(KeyConditionExpression=Key('deviceid').eq('2b0037001147343339383037'))
    print(entries)
    return render_template('show_entries.html', entries=entries['Items'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
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



