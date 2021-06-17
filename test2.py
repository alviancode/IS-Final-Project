import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import time
from fuzzywuzzy import process
from rapidfuzz import process as rapidProcess
from functools import lru_cache


def get_title_from_index(index):
	return movies[movies.index == index]["title"].values[0]

def getDate(index):
	return movies[movies.index == index]["release_date"].values[0]

def get_index_from_title(title):
    return movies[movies.title == title]["index"].values[0]
##################################################

movies = pd.read_csv("movie_dataset.csv")


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



def fuzzySearch(title, items = 10):
    begin = time.time()
    index=[]
    temp =[]
    j=0
    for i in movies['title']:
        index.append([levenshteinDistance2((title), (i)),j])
        j=j+1

    for i in range(items):
        temp.append(get_title_from_index(sorted(index)[i][1]))
    end = time.time()
    print(f"Time needed:{end-begin}")
    return temp

def levenshteinDistance2(a:str,b:str) -> int:
    
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
    d = [[0 for i in range(lenB+1)] for k in range(lenA+1)]
    
    '''d = np.zeros((lenA+1, lenB+1), dtype=int)
    
    for i in range(lenA+1):
        d[i, 0] = i
        
    for j in range(lenB+1):
        d[0, j] = j'''
    
    for i in range(1,lenA+1):
        for m in range(1,lenB+1):
            if a[i-1] == b[m-1]:
                cost = 0
            else:
                cost = 1

            d[i][m] = min(d[i-1][m] + 1 ,     # deletion.
                                d[i][m-1] + 1 ,    # insertion.
                                d[i-1][m-1] + cost    # substitution.
                                )
    return d[lenA][lenB]


print(levenshteinDistance2("al", "alis"))

title="night"

print("rapidfuzz")
begin=time.time()
print(rapidProcess.extract(title, movies['title'], limit=10))
end=time.time()
print(f"Time needed:{end-begin}\n")

print("fuzzywuzzy")
begin=time.time()
print(process.extract(title, movies['title'], limit=10))
end=time.time()
print(f"Time needed:{end-begin}\n")

print("Levensthein Distance")
print(fuzzySearch(title))


