__author__ = 'Aravind Vicinthangal Prathivaathi'

import sys
from pymongo import MongoClient
from pprint import pprint


def main():
    """
    Samples the data from the movie and creates the kmeansNorm field for all the movies.
    :return:
    """

    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['imdb']



    # filter or cleaning the movie collection
    filter = db.movies.delete_many({'$or':[{'type':{'$ne':'movie'}},{'avgRating':{'$exists':False}}, {'startYear':{'$exists':False}}, {'numVotes':{'$lte':10000}}]})


    #find the maximum rating
    maxrate_query = db.movies.find().sort('avgRating', -1).limit(1)

    max_rating = 0
    for res in maxrate_query:
        max_rating = res['avgRating']

    #find the minimum rating
    minrate_query = db.movies.find().sort('avgRating', 1).limit(1)
    min_rating = 0
    for rest in minrate_query:
        min_rating = rest['avgRating']


    #find the maximum start year
    maxyear_query = db.movies.find().sort('startYear', -1).limit(1)
    max_start_year = 0

    for rest1 in maxyear_query:
        max_start_year = rest1['startYear']


    #find the minimum startyear
    minyear_query = db.movies.find().sort('startYear', 1).limit(1)
    min_start_year = 0

    for rest2 in minyear_query:
        min_start_year = rest2['startYear']




    query = db.movies.find()

    #create a new field called kmeansNorm and set it's values
    for q in query:
        id = q['_id']
        rating = q['avgRating']
        startYear = q['startYear']
        list = []
        n_rating = (rating - min_rating)/(max_rating - min_rating)
        print('Normalized Rating: ', n_rating)
        n_startYear = (startYear - min_start_year)/(max_start_year - min_start_year)
        print('Normalized Start Year: ', n_startYear)

        list.append(n_startYear)
        list.append(n_rating)

        query = db.movies.update_one({'_id':id}, {'$set':{'kmeansNorm': list}})


    find_query = db.movies.find()



if __name__ == '__main__':
    main()