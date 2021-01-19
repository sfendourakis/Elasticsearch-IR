import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class Clustering:

    def __init__(self, movies_file, ratings_file):
        self.movies_file = movies_file
        self.ratings_file = ratings_file

    def get_movies(self):
        movies = pd.read_csv(self.movies_file,
            sep=',',
            names=['MovieID','Title','Genres'],
            engine='python',
            header=0
            )
        return movies

    def get_ratings(self):
        ratings = pd.read_csv(self.ratings_file,
            sep=',',
            names=['UserID','MovieID','Rating', 'Timestamp'],
            parse_dates=['Timestamp'],
            engine='python',
            header=0
            )
        ratings = ratings.drop("Timestamp", axis=1)
        return ratings

    def get_genres(self, dataframe):
        genres = set()
        genre_list = list(dataframe['Genres'].str.split('|'))
        for x in genre_list:
            for i in x:
                genres.add(i)
        return genres

    def merge_genres(self, movies, ratings):
        movie_ratings = pd.merge(movies, ratings, on='MovieID')
        Genre = movie_ratings['Genres']
        Genre = Genre.str.get_dummies()
        movie_ratings_genres = pd.concat([movie_ratings.drop(['Genres'], axis=1), Genre], axis=1,)
        return movie_ratings_genres

    def get_gernes_avg(self, movies, movie_ratings_genres):
        genrecols = list(self.get_genres(movies))
        #melting dataframe to form one hot encoding dataframe
        mdf = pd.melt(movie_ratings_genres[['UserID', 'Rating'] + genrecols], id_vars=['UserID', 'Rating'], var_name='Genre')
        #keeping only 1 values for every user at every genre
        mdf = mdf[mdf['value']==1][['UserID', 'Rating', 'Genre']]
        #pivoting the dataframe and calculating avarage rating for every genre by every user
        movie_genres_avg_rating = pd.pivot_table(mdf, columns = ['Genre'], index = ['UserID'], values = ['Rating'], aggfunc = np.mean)
        movie_genres_avg_rating = movie_genres_avg_rating.round(decimals=2)
        return movie_genres_avg_rating

    def clustering(self, clusters, dataframe):
        dataframe = dataframe.fillna(0)
        kmeans = KMeans(n_clusters=clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
        predictions = kmeans.fit_predict(dataframe)
        return predictions
        
    def merge_pivot(self, movie_ratings, user_cluster):
        movie_ratings_cluster = pd.merge(movie_ratings, user_cluster, on='UserID')

        movie_ratings_cluster = movie_ratings_cluster.drop(columns=['Genres', 'Title', 'UserID'], axis=1)
        #melting dataframe to form one hot encoding dataframe
        udf = pd.melt(movie_ratings_cluster, id_vars=['MovieID', 'Rating'], value_name='Cluster')
        #pivot to calculate the average rating for every movie by every cluster
        movies_cluster_avg = pd.pivot_table(udf, columns='Cluster', index='MovieID', values=['Rating'], aggfunc=np.mean)
        movies_cluster_avg = movies_cluster_avg.round(decimals=2)
        return movies_cluster_avg
    
foo = Clustering("C:\\Users\\30694\\Desktop\\PROJECTS\\ProjectIR\\movies.csv", "C:\\Users\\30694\\Desktop\\PROJECTS\\ProjectIR\\ratings.csv")
movies = foo.get_movies()
ratings = foo.get_ratings()
merged_genres = foo.merge_genres(movies, ratings)
genre_avg = foo.get_gernes_avg(movies, merged_genres)
user_cluster = pd.DataFrame(index=genre_avg.index)
clustering = foo.clustering(20, genre_avg)
user_cluster['Cluster'] = clustering
merged = pd.merge(movies, ratings, on='MovieID')
final = foo.merge_pivot(merged, user_cluster)
#foo = list(final.columns.get_level_values(1))
#new = pd.DataFrame(index=final.index, columns=foo)
foo = final['Rating']
foo.fillna(0)
print(foo)
foo.to_csv('movies_cluster_avg.csv')
user_cluster.to_csv('user_cluster.csv')
