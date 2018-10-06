import math
import pprint

from flask import Flask, request, jsonify
from flask import render_template

from db.data import Award, getAwards

pp = pprint.PrettyPrinter(indent=4)

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

class Match():
    def __init__(self, titleA, titleB):
        self.exists = True

        self.titleA = titleA
        self.titleB = titleB
        self.awardsA = getAwards(titleA)
        self.awardsB = getAwards(titleB)

        self.win = False # True :: A wins

    def winner(self):
        if len(self.awardsA) > len(self.awardsB):
            self.win = True
            return self.titleA
        else:
            self.win = False
            return self.titleB
        
@app.route("/")
def index():
    return render_template('index.html')

# CREATE
@app.route("/db/add/")
def add():
    return "add"

# READ
@app.route("/results/", methods=['GET', 'POST', 'DELETE'])
def getResults():
    thisRound = request.form.getlist('round[]')

    if thisRound == []:
        return error("No round")

    if '' in thisRound:
        return error("Incomplete round") 

    inputs = []

    for i in range(0, len(thisRound), 2):
        inputs.append(Match(thisRound[i], thisRound[i+1]))

    inputSize = len(inputs)

    bracketWidth = int(pow(2, math.ceil(math.log(inputSize,2))))
    bracketSize = bracketWidth * 2 # - 1

    bracket = [None] * bracketSize

    for i in range(inputSize):
        bracket[bracketSize-1-i] = inputs[i]

    for i in range(bracketSize-2, 1, -2):
        print i
        match = bracket[i]
        sibling = bracket[i+1]

        if (match is not None and sibling is not None):
            bracket[i/2] = Match(match.winner(), sibling.winner()) 

        if (match is None and sibling is not None):
            fake = Match(sibling.titleA, sibling.titleB)
            fake.exists = False
            bracket[i/2] = fake

    pp.pprint(list(map(lambda m: (m.titleA + ' vs ' + m.titleB) if (m is not None and m.exists) else '', bracket)))

    return error(bracketSize)
    
    '''
    return success({
        "input": render_template('input.html', movies=inputs, edges=inputEdges),
        "results": render_template('results.html', size=thisSize, bracket=results) 
    });
    '''

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
