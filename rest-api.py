from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import MovieRecommender as mr



app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['GET'])
@cross_origin()
def hello():
    return jsonify("Hello World")


@app.route("/search/<string:title>", methods=['GET'])
@cross_origin()
def getTitle(title):
    return jsonify({"movies":mr.fuzzySearch(title, 15)}), 200


@app.route("/allbest", methods=["GET"])
@cross_origin()
def getHighestRating():
    return jsonify({"movies": mr.bestMovies()})


@app.route('/recommend', methods=["GET"])
@cross_origin()
def getRecommendation():
    getVal = request.headers.get('watched')
    return jsonify({"movies":mr.recommendations(getVal)})



if __name__ == '__main__':
    app.run(debug=True)