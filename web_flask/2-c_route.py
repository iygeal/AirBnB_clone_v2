#!/usr/bin/python3
"""This python scripts starts a Flask web app with defined routes"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Method that displays greeting"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Method that displays HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Method that displays C followed by text"""
    text = text.replace("_", " ")  # replace _ with space in text
    return f"C {text}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
