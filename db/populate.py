import csv
import os

from data import createMovie, createAward, createJoin 

cwd = os.path.dirname(os.path.realpath(__file__)) 

def addData(csvPath, createDataWithLine):
    with open(csvPath) as data:
        reader = csv.reader(data, delimiter=',')

        line = 0
        for row in reader:
            line += 1

            if line == 1:
                continue;

            if line > 100:
                break;

            createDataWithLine(row)

def createAcademyAward(row): 
    entity = "Oscar"
    win = row[2] == 'True'
    name = row[1].decode('utf-8', 'ignore').encode('utf-8')
    movie = row[3].decode('utf-8', 'ignore').encode('utf-8')

    print "created academy award for " + movie 

    createJoin(createMovie(movie), createAward(entity, name, win))

def createGoldenGlobe(row):
    entity = "Golden Globe"
    win = row[3] == 'yes'
    name = row[1].decode('utf-8', 'ignore').encode('utf-8')
    movie = row[2].decode('utf-8', 'ignore').encode('utf-8')

    print "created academy award for " + movie 

    createJoin(createMovie(movie), createAward(entity, name, win))

addData(cwd + '/csv/academyawards.csv', createAcademyAward)

addData(cwd + '/csv/goldenglobes.csv', createGoldenGlobe)
