from flask import Flask, request
from flask import render_template

from db.data import session, Movie, Award, Join

app = Flask(__name__)

print "Movie Bracket!"

@app.route("/get")
def getStuff():
    getData()

    return "GOT IT!"

def compare(a, b):
    print a;
    print b;
    return a;

@app.route("/")
def index():
 
    bracket = request.args.get('b')

    if bracket is not None:
        bracket = bracket.split(',')
        round1 = [
                    compare(bracket[0], bracket[1]),
                    compare(bracket[2], bracket[3])
                ]

        winner = compare(round1[0], round1[1])

        return render_template('index.html',
            movieA=round1[0],
            movieB=winner,
            movieC=round1[1])

    return render_template('index.html');
