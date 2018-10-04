from flask import Flask, request
from flask import render_template

from db.data import createMovie, createAward, createJoin 

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('index.html');
