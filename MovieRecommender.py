import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import omdb

# Read the dataset.
movies = pd.read_csv("movie_dataset.csv")

# OMDB API
omdb.set_default('apikey', 'API KEY')
omdbRes=omdb.search('True Grit')[0].get('poster')

# Function to return movie's poster from IMDB using OMDB API.
def getPoster(title):
    try:
        #return ''
        return omdb.search(title)[0].get('poster')
    except:
        return 'https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png'

# This function return the movie title from a given index.
def getTitleFromIndex(index):
	return movies[movies.index == index]["title"].values[0]

# This function return the date of the movie from a given index.
def getDate(index):
	return movies[movies.index == index]["release_date"].values[0]

# This function return the index of the movie from a given title.
def getIndexFromTitle(title):
    return movies[movies.title == title]["index"].values[0]
##################################################



# Create a combination of features from the movie.
def combineFeatures(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print ("Error:", row)	

# Function that recommend the movie.
def recommendations(movieTitle):
    features = ['keywords','cast','genres','director', 'crew']
    result = []
    
    # Create a column in the DataFram that store the combined features.
    for feature in features:
        movies[feature] = movies[feature].fillna('')
    movies["combinedFeatures"] = movies.apply(combineFeatures, axis=1)

    # Count word frequency
    countVec = CountVectorizer(stop_words = 'english')
    countMatrix = countVec.fit_transform(movies["combinedFeatures"])
    
    # Convert Sparse Matrix to DataFrame
    termMatrix = countMatrix.todense()
    dataFrame = pd.DataFrame(termMatrix, columns= countVec.get_feature_names())
    
    # Calculating cosine similarities
    cosineSim = pd.DataFrame(cosine_similarity(dataFrame, dense_output=True))
    
    movieUserLike = movieTitle

    movie_index = getIndexFromTitle(movieUserLike)

    # Calculate the similar movies.
    similarMovies =  list(enumerate(cosineSim[movie_index]))

    # Sorted the similar movie by the similarity value.
    sortedSimilarMovies = sorted(similarMovies,key=lambda x:x[1],reverse=True)
    
    i=0
    for element in sortedSimilarMovies:
        result.append({
            "title" : getTitleFromIndex(element[0]),
            "index" :element[0],
            "date" : getDate(element[0]),
            "poster" : getPoster(getTitleFromIndex(element[0]))
                       })
        i=i+1
        if i>20:
            return result
        
    

# Function for fuzzy serach.
def levenshteinDistance(a:str,b:str) -> int:
    
    # Filter the input title and also the dataset titles for better result.
    a, b = a.lower(), b.lower()
    punctuation = '''!()-[]{};:'"\, <>./?@#$%^&*_~ '''
    for element in a:
        if element in punctuation:
            a = a.replace(element, '')
    for element in b:
        if element in punctuation:
            b = b.replace(element, '')
    
    
    lenA = len(a)
    lenB = len(b)
    d = np.zeros((lenA+1, lenB+1), dtype=int)
    
    # Transforming source prefixes  into empty string
    # by dropping all characters.
    for i in range(lenA+1):
        d[i, 0] = i
    
    # Reaching the target prefixes from source prefix
    # by inserting each characters.
    for j in range(lenB+1):
        d[0, j] = j
    
        
    for i in range(1,lenA+1):
        for m in range(1,lenB+1):
            if a[i-1] == b[m-1]:
                cost = 0
            else:
                cost = 1

            d[i, m] = min(d[i-1, m] + 1 ,     # deletion.
                                d[i, m-1] + 1 ,    # insertion.
                                d[i-1, m-1] + cost    # substitution.
                                )
    return d[lenA][lenB]



# Function that return the best rating movies.
def bestMovies(items = 20):
    array = []
    C = movies["vote_average"].mean()
    m = movies['vote_count'].quantile(0.90)
    qMovies = movies.copy().loc[movies['vote_count'] >= m]
    
    def weightedRating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m)*R) + (m/(m+v)*C)
    qMovies['score'] = qMovies.apply(weightedRating, axis=1)
    qMovies = qMovies.sort_values("score", ascending=False)
    temp = qMovies[['title', 'release_date', 'index']].head(50)
    temp.values.tolist()
    for i in range(len(temp)):
        array.append({"title" : temp.values.tolist()[i][0],
                      "date" : temp.values.tolist()[i][1],
                      "index" : temp.values.tolist()[i][2],
                      "poster" : getPoster(temp.values.tolist()[i][0])
                      })
    return array



# Helper function for fuzzy search for REST API purposes.
def fuzzySearch(title, items = 10):
    index=[]
    temp =[]
    j=0
    for i in movies['title']:
        index.append([levenshteinDistance((title), (i)),j])
        j=j+1
    #return index
    for i in range(items):
        temp.append({"title":getTitleFromIndex(sorted(index)[i][1]),
                     "index":sorted(index)[i][1], 
                     "date":getDate(sorted(index)[i][1]),
                     "poster":getPoster(getTitleFromIndex(sorted(index)[i][1]))
                     })
    return temp