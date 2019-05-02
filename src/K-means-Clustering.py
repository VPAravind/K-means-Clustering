__author__ = 'Aravind Vicinthangal Prathivaathi'


from pymongo import MongoClient
import math
import matplotlib.pyplot as plt

"""
Code that implements the full k-means algorithm for 5 different genres and 9 different values of k which is number of clusters. 
For each genre and for each cluster, we do over 100 iterations and find the Standard Error. 
"""
def main():
    """
    Main function which establishes connection with the database and implments the k-means clustering.
    :return:
    """
    client = MongoClient('localhost', 27017)
    db = client['imdb']

    genre_list = ['Action', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']

    for i in range(len(genre_list)):
        genre = genre_list[i]
        k_list = []
        sse_list = []
        glist = []
        glist.append(genre)
        # k = 10

        # for k values from 10 to 50
        for k in range(10,55,5):
            print('********************************************')
            print('********************************************')
            print('For sample size:', k)
            print('********************************************')
            print('********************************************')

            centroid_list = []

            # query to get k samples from movies to set them as the initial centroids
            result = db.movies.aggregate([{'$match': {'genres': genre}}, {'$sample': {'size': k}}])

            j = 1

            for res in result:
                # print('Creating the centroid collection')

                kmeansNorm = res['kmeansNorm']
                # print(res['genres'])
                # print(res['title'])
                tup = (kmeansNorm[0], kmeansNorm[1], j)

                centroid_list.append(tup)


                centroid = {'_id': j, 'kmeansNorm': kmeansNorm}
                # create k centroid collections
                db.centroids.insert_one(centroid)
                j += 1

            # get the movies that match with the current genre

            # run k-means algorithm for 100 iterations or till convergence
            for l in range(100):
                m_result = db.movies.aggregate([{'$match': {'genres': genre}}])

                flag = False
                # print('Inside 100 iterations')

                # for each document for this particular genre
                for m_res in m_result:
                    list = []

                    # get the kmeansNorm array of the current movie
                    kmeansNorm = m_res['kmeansNorm']

                    # get the movie id
                    movie = m_res['_id']

                    # print("Movie id", movie)
                    # print("k Means Norm", kmeansNorm)

                    # query the centroid collections and get all it's documents
                    centroid_doc = db.centroids.find()

                    # get the distance between each centroid and the current movie
                    for cent in centroid_doc:
                        centroid_pt = cent['kmeansNorm']

                        # calculate the euclidian distance

                        mh_dist = math.sqrt(
                            ((kmeansNorm[0] - centroid_pt[0]) ** 2) + ((kmeansNorm[1] - centroid_pt[1]) ** 2))
                        t = (mh_dist, cent['_id'])
                        list.append(t)

                    # sort the list in the ascending order w.r.t distance between centroid and data point
                    list.sort()
                    # print('Manhattan Distance and centroid Id', list)
                    # print(list)
                    # get id of the centroid within the shortest distance
                    centroid_id = list[0][1]
                    # print('Cluster ID', centroid_id)

                    # update the movie collection with a new field corresponding to the closest centroid
                    db.movies.update_one({'_id': movie}, {'$set': {'cluster': centroid_id}})

                # list of the co-ordinates of the centroids
                mean_list = []
                # try to move the centroid or update the centroid by taking the mean of all the points under that centroid

                # do k calculations to get new set of k centroids
                for m in range(k):
                    cid = m + 1

                    # print("Trying for convergence, creating means", cid)
                    # get the document with the average of the x and y co-ordinates that belong to the same cluster
                    avg_query = db.movies.aggregate([

                        {'$match': {'cluster': cid}},
                        {'$unwind': '$kmeansNorm'},
                        {'$group': {
                            '_id': '$_id',
                            'xcor': {'$first': '$kmeansNorm'},
                            'ycor': {'$last': '$kmeansNorm'}
                        }},

                        {'$group': {
                            '_id': 0,
                            'xAvg': {'$avg': '$xcor'},
                            'yAvg': {'$avg': '$ycor'}
                        }}

                    ])

                    # iterate through the selected documents and assign the x and y co-ordinate
                    for result in avg_query:
                        avg_tuple = (result['xAvg'], result['yAvg'], cid)
                        mean_list.append(avg_tuple)

                # print(mean_list)
                # print(centroid_list)
                if mean_list == centroid_list:
                    flag = True
                    break
                else:
                    for tuple in mean_list:
                        normlist = []
                        normlist.append(tuple[0])
                        normlist.append(tuple[1])
                        clust_id = tuple[2]
                        db.centroids.update_many({'_id': clust_id}, {'$set': {'kmeansNorm': normlist}})
                        centroid_list = mean_list[:]

            # calculate the sum of sqaure error and append it to a list
            sse_list.append(plot_sse(db, k, genre))

            k_list.append(k)

            db.centroids.drop()

            k += 5
        # sse_list.sort(reverse = True)
        if(genre == 'Romance'):
            sse_list = remove_outlier(sse_list)
        # print('SError',sse_list)
        plt.plot(k_list, sse_list)
        print(genre)
        img_name = genre + '.png'
        print(img_name)
        plt.savefig(img_name)
        plt.close()


def plot_sse(db, k, genre):
    """
    Calculate the sum of square error for every k
    :param db: cursor to the database
    :param k: number of centroids or clusters
    :param genre: genre type
    :return: sum of the squared errors
    """

    print('Calculating SSE')
    result1 = db.movies.aggregate([{'$match': {'genres': genre}}])
    sum = 0
    for res1 in result1:

        data_point = res1['kmeansNorm']

        cluster_id = res1['cluster']

        query1 = db.centroids.find({'_id': cluster_id})

        centroid_arr = []
        for docs in query1:
            centroid_arr = docs['kmeansNorm']


        distance = ((data_point[0] - centroid_arr[0]) ** 2) + ((data_point[1] - centroid_arr[1]) ** 2)

        sum += distance

    return sum

def remove_outlier(sse_list):
    for i in range(len(sse_list)-1):
        while sse_list[i] < sse_list[i+1]:
            list.pop(i)
            i-=1

    return sse_list





if __name__ == '__main__':
    main()
