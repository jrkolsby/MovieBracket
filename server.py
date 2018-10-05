from flask import Flask, request, jsonify
from flask import render_template

from db.data import Award, getAwards

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template('index.html')

# CREATE
@app.route("/db/add/")
def add():
    return "add"

def compare(a, b):

    if len(a["awards"]) > len(b["awards"]):
        a["win"] = True
        b["win"] = False
        return a.copy()

    a["win"] = False
    b["win"] = True
    return b.copy()


# READ
@app.route("/results/", methods=['GET', 'POST', 'DELETE'])
def getResults():
    thisRound = request.form.getlist('round[]')
    thisSize = len(thisRound) / 2

    if thisRound == []:
        return error("No round")

    if '' in thisRound:
        return error("Incomplete round")

    inputs = list(map(lambda m: { \
            "name": m,  
            "awards": list(map(lambda a: { \
                    "entity": a.entity,
                    "name": a.name,
                    "win": a.win
                }, getAwards(m)))
        }, thisRound))

    results = []

    for i in range(0, len(inputs), 2):
        results.append(compare(inputs[i], inputs[i+1])) #Mutates!!

    inputEdges = []

    if thisSize is 4:
        inputEdges = ["down right", "up right", "down right", "up right"]
        results.append(compare(results[0], results[1]))
        results.append(compare(results[2], results[3]))
        results.append(compare(results[4], results[5]))
        
    print list(map(lambda m: m['name'], results))

    return success({
        "input": render_template('input.html', movies=inputs, edges=inputEdges),
        "results": render_template('results.html', size=thisSize, bracket=results) 
    });

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
