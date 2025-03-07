# Movie Recommendation System
A movie recommendation system using content based recommendation for Intelligent System Final Project.

### Made By:
- Alvian Wijaya
- Andreas Sukardi Teja
- Davin Pratama Chandra

![](https://github.com/alviancode/IS-Final-Project/blob/main/preview/preview.png?raw=true)

## Implementation
We choose to create a content based recommendation based on movie keywords, cast, genres, and director.

For searching the movie, we implemented Approximate String Matching using `Levenshtein Distance`. This allow the user to search a movie without have to input the exact movie's title.

For the User Interface we implemented Single Page Application with REST-API. We choose `React` for the frontend and `flask` as our backend.

For the recommender part, we use `pandas`, `numpy`, `sklearn`, and `ast`. Because our dataset doesn't have the movie poster, we use `omdb` library which take the posters from IMDB.

## Dataset
The dataset we use is from [Code Heroku](https://www.youtube.com/watch?v=3ecNC-So0r4). It contains around 4500 movies.

## Installation
### Backend
For backend, you have to install `sklearn` and `flask` using `pip`. To get the movie poster, you have change `API KEY` for OMDB API. You can go to `MovieRecommender.py` and change `API KEY` with your OMDB API key.
```
omdb.set_default('apikey', 'API KEY')
```
To run the backend, you can run it from `rest-api.py`. The default PORT is `5000`. To check it you can open your internet browser and go to `localhost:5000`.

### Frontend
For frontend make sure you installed `Node.js`. You can download it from [Node.js](https://nodejs.org/en/download/) and install it according to your platform.

 To run it, first you have to install all the dependencies using `npm install`. Aftter that, run `npm start` to start the server. The default port for the server is at port `3000`. To check it, you can open your browser and go to `localhost:3000`.
