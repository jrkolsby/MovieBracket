import json
from flask import Flask, request
from flask import render_template

from db.data import createMovie, createAward, createJoin 
from db.data import compareMovies

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('index.html')

# CREATE
@app.route("/db/add/")
def add():
    return "add"

# READ
@app.route("/db/compare/")
def compare():
    a = request.args.get('a')
    b = request.args.get('b')

    result = compareMovies(a,b)
    print(result)

    if result is None:
        return "No results"
    else:
        return str(result.id)

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
