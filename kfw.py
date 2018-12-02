#!usr/bin/python

from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint

# Create an instance of Flask called app in the current file
# This is the beginning of a new web application
app = Flask(__name__)


# Define the default page
@app.route("/")
# The function activated from the default page
def index():
    return "Flask App!"

# Define the about page
@app.route("/about/")
def about():
    return render_template('about.html')

# Define parameterized page
@app.route("/hello/<string:name>/")
def hello(name):
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]
    return render_template('test.html', **locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 80, debug=True)