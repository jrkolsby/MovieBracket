import csv
import os

from data import createMovie, createAward, createJoin 

cwd = os.path.dirname(os.path.realpath(__file__)) 

def getData(csvPath, createDataWithLine):
    with open(csvPath) as data:
        reader = csv.reader(data, delimiter=',')

        line = 0
        for row in reader:
            if line > 100:
                break

            createDataWithLine(row)
            line += 1

def createAcademyAward(row): 
    entity = "Oscar"
    win = True 
    name = row[1].decode('utf-8', 'ignore').encode('utf-8')
    movie = row[2].decode('utf-8', 'ignore').encode('utf-8')

    print "created academy award for " + movie 

    createJoin(createMovie(movie), createAward(entity, name, win))

getData(cwd + '/csv/academyawards.csv', createAcademyAward)

