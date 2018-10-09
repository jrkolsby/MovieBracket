import math

from itertools import chain
from flask import Flask, request, jsonify
from flask import render_template

from db.data import Award, getAwards
from edge import edge

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

    def __str__(self):
        return str(self.exists) + \
    str(self.depth) + ': ' + \
    self.titleA + ' vs ' + \
    self.titleB + ' (' + \
    str(self.win) + ')'

    def __init__(self, titleA, titleB, depth=0):
        self.exists = True

        self.titleA = titleA
        self.titleB = titleB
        self.awardsA = getAwards(titleA)
        self.awardsB = getAwards(titleB)

        self.win = False # True :: A wins
        self.final = False

        self.depth = depth

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

def makeBracket(inputs):
    inputSize = len(inputs)

    bracketWidth = int(pow(2, math.ceil(math.log(inputSize,2))))
    bracketSize = bracketWidth * 2 # - 1

    bracket = [None] * bracketSize

    for i in range(inputSize):
        bracket[bracketSize-1-i] = inputs[i]

    for i in range(bracketSize-2, 1, -2):
        match = bracket[i]
        sibling = bracket[i+1]

        if (match is not None and sibling is not None):
            parent = Match(sibling.winner(), match.winner(), match.depth+1)
            bracket[i/2] = parent

        if (match is None and sibling is not None):
            jump = Match(sibling.titleA, sibling.titleB, sibling.depth+1)
            jump.exists = False
            jump.parent = sibling
            bracket[i/2] = jump

    return bracket;

def layout(bracket):

    def rec(i, bracket, output):
        if i >= len(bracket):
            return None

        node = bracket[i]

        if node is None or node.depth == 0:
            return None

        # left child
        rec(i*2+1, bracket, output)

        if node.exists:
            output.append(node)
        else:
            jumpWidth = 0 
            jumpNode = node.parent
            while not jumpNode.exists:
                jumpWidth += 1
                jumpNode = jumpNode.parent

        # right child
        rec(i*2, bracket, output)

    inOrderBracket = []
    rec(1, bracket, inOrderBracket)
    return inOrderBracket

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
        match = Match(thisRound[i], thisRound[i+1])
        inputs.append(match)

    bracket = makeBracket(inputs)
    final = bracket[1]
    final.final = True
    victor = final.winner()

    bracket = layout(bracket)

    edges = edge.get(len(inputs))
    i = 0
    for m in chain(inputs, bracket):
        if m is not final:
            m.edge = edges[i]
            i += 1

    return success({
        "input": render_template('results.html', matches=inputs),
        "results": render_template('results.html', matches=bracket) 
    });

# UPDATE
@app.route("/db/update")
def update():
    return "update"

@app.route("/db/delete")
def delete():
    return "delete"
