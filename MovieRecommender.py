import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ageClassification import checker
from ast import literal_eval
from fuzzywuzzy import process
import omdb

omdb.set_default('apikey', 'a3e014fb')
omdbRes=omdb.search('True Grit')[0].get('poster')

def getPoster(title):
    try:
        #return 'https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png'
        return omdb.search(title)[0].get('poster')
    except:
        return 'https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png'

def get_title_from_index(index):
	return movies[movies.index == index]["title"].values[0]

def getDate(index):
	return movies[movies.index == index]["release_date"].values[0]

def get_index_from_title(title):
    return movies[movies.title == title]["index"].values[0]
##################################################

movies = pd.read_csv("movie_dataset.csv")

def combineFeatures(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print ("Error:", row)	



def levenshteinDistance(a:str,b:str) -> int:
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
    d2Memo = [[0 for i in range(lenB+1)] for k in range(lenA+1)]
    for i in range(1,lenA+1):
        for m in range(1,lenB+1):
            k = 0 if a[i-1] == b[m-1] else 2
            d2Memo[i][m] = min(d2Memo[i-1][m] + 1 ,
                                d2Memo[i][m-1] + 1 ,
                                d2Memo[i-1][m-1] + k
                                )
    return d2Memo[lenA][lenB]





def bestMovies(items = 20):
    #print(movieSort[['title', 'index', "vote_average"]])
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
    



#print(bestMovies())




def fuzzySearch(title, items = 10):
    index=[]
    temp =[]
    j=0
    for i in movies['title']:
        index.append([levenshteinDistance((title), (i)),j])
        j=j+1
    #return index
    for i in range(items):
        temp.append({"title":get_title_from_index(sorted(index)[i][1]),
                     "index":sorted(index)[i][1], 
                     "date":getDate(sorted(index)[i][1]),
                     "poster":getPoster(get_title_from_index(sorted(index)[i][1]))
                     })
        
    return temp


#print(process.extract("ironman", movies['title']))


#print("\nUSING DIY:")
#print(fuzzySearch("ironman"))







def recommendations(movieTitle, boolean = False):
    features = ['keywords','cast','genres','director', 'crew']
    result = []
    
    for feature in features:
        movies[feature] = movies[feature].fillna('')
    
    movies["combinedFeatures"] = movies.apply(combineFeatures, axis=1)

    #Count word frequency
    countVec = CountVectorizer(stop_words = 'english')
    countVec = CountVectorizer()
    countMatrix = countVec.fit_transform(movies["combinedFeatures"])
    
    #Convert Sparse Matrix to DataFrame
    termMatrix = countMatrix.todense()
    dataFrame = pd.DataFrame(termMatrix, columns= countVec.get_feature_names())
    
    #Calculating cosine similarities
    cosineSim = pd.DataFrame(cosine_similarity(dataFrame, dense_output=True))
    
    
    movie_user_likes = movieTitle

    movie_index = get_index_from_title(movie_user_likes)

    similar_movies =  list(enumerate(cosineSim[movie_index]))


    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
    
    i=0
    for element in sorted_similar_movies:
        result.append({
            "title" : get_title_from_index(element[0]),
            "index" :element[0],
            "date" : getDate(element[0]),
            "poster" : getPoster(get_title_from_index(element[0]))
                       })
        i=i+1
        if i>30:
            return result
        
    



print(recommendations("Iron Man"))
