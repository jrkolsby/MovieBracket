from flask import Flask, request, jsonify
from flask import render_template

from db.data import Award, getAwards

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

    results = list(map(lambda m: { \
            "name": m,  
            "awards": list(map(lambda a: { \
                    "entity": a.entity,
                    "name": a.name,
                    "win": a.win
                }, getAwards(m)))
        }, thisround))

    return success(results) 

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
