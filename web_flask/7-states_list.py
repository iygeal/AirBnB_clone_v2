#!/usr/bin/python3
"""Python script that starts a Flask web app"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Method that displays states list"""
    states = storage.all(State).values()  # get all states
    states = sorted(states, key=lambda k: k.name)  # sort by name
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session"""
    storage.close()
