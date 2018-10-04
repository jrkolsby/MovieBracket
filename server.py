from flask import Flask, request, jsonify
from flask import render_template

from db.data import createMovie, createAward, createJoin 
from db.data import compareMovies

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def success(payload): 
    response = {
        "type": "SUCCESS",
        "payload": payload
    }
    return jsonify(response)

def error(payload):
    response = {
        "type": "ERROR",
        "payload": payload 
    }
    return jsonify(response)

# CREATE
@app.route("/db/add/")
def add():
    return "add"

# READ
@app.route("/db/compare/", methods=['GET', 'POST', 'DELETE'])
def compare():
    thisround = request.form.getlist('round[]')

    if thisround == []:
        return error("No round")

    if '' in thisround:
        return error("Incomplete round")

    results = [None] * (len(thisround)/2)

    return success(results) 

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
