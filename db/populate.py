import csv

from data import session, Movie, Award, Join

def getData():
    with open('./csv/academyawards.csv') as awardData:
        reader = csv.reader(awardData, delimiter=',')
        line = 0

        for row in reader:
            if line > 0 and line < 100:

                awardName = "Academy Award"
                awardRank = row[4] == 'YES'
                awardCategory = row[1].decode('utf-8', 'ignore').encode('utf-8')
                movieName = row[3].decode('utf-8', 'ignore').encode('utf-8')

                movie = Movie()
                movie.name = movieName 
                session.add(movie)

                award = Award()
                award.name = awardName
                award.rank = awardRank
                award.category = awardCategory

                session.add(award)
                session.flush()

                join = Join()
                join.award = award.id
                join.movie = movie.id
                session.add(join)

                session.commit()

            line += 1;

        print("Created " + str(line) + " awards")

getData()
