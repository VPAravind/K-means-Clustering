Dataset source: https://datasets.imdbws.com/ . 

Note: Pre-processing was done prior to applying the clustering model. Pre-processing involved, data intergration and data cleaning steps. MongoDB was used as the database. The data was uploaded to the database using Studio3T. 

# K-means-Clustering
The program implements k-means clustering algorithm on the movies.json dataset given.

The program initially samples to data set based on certain conditions. This allows use to efficiently test our kmeans algorithm.
You must to run the code called preparing data, as this program adds an important field called kmeansNorm to each documents from the filtered dataset obtained from the movies.json file. The kmneansNorm field is the coordinates of that particular document. 

After running the prepare_data program given in the src directory, you can run the k-means-clustering program. 

The program runs the clustering alogrithm separately on four different genres: 'Action', 'Horror', 'Romance', 'Sci-Fi', 'Thriller' present in the filtered data set. Additionally, the program runs the algorithms for different k-values and up until the centroids don't move for each k-value. 

For each of the k-value, we then calculate the sum of squared mean error and plot a graph between the sum of squared mean and the different k-values for each genres. The program then generate a graph where the graph of each genre has the sum of squared means on the y-axis and the genre on the x-axis. We can then find the elbow point by either eye-balling it or thorugh some basic calculus to find where there is sharp fall in the rate of decrease on the slope in the graph of each genre. This gives the approriate k-value for the graph.

