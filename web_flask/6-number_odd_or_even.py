#!/usr/bin/python3
"""Script that starts a Flask web app with defined routes"""

from flask import Flask, render_template

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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """Method that displays Python followed by text"""
    text = text.replace("_", " ")  # replace _ with space in text
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Method that displays n if n is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Method that displays an HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Method that displays an HTML page only if n is an integer"""
    parity = "even" if n % 2 == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n, parity=parity)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
