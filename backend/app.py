from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import MusicRecommender
import os

app = Flask(__name__)
CORS(app)

# Load recommender once
recommender = MusicRecommender("data/spotify_tracks.csv")


def success_response(data):
    return jsonify({
        "status": "success",
        "data": data
    })


def error_response(message, code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), code


@app.route("/")
def home():
    return success_response({
        "message": "AI Music Recommendation API is running"
    })


# ---------------- SONG BASED ----------------
@app.route("/recommend/song", methods=["GET"])
def recommend_song():
    query = request.args.get("query")

    if not query:
        return error_response("Please provide a song name using ?query=")

    results = recommender.recommend_by_song(query)

    return success_response({
        "type": "song-based",
        "query": query,
        "results": results
    })


# ---------------- MOOD BASED ----------------
@app.route("/recommend/mood", methods=["GET"])
def recommend_mood():
    mood = request.args.get("mood")

    if not mood:
        return error_response("Please provide a mood using ?mood=")

    results = recommender.recommend_by_mood(mood.lower())

    return success_response({
        "type": "mood-based",
        "mood": mood,
        "results": results
    })


# ---------------- TEXT / AI BASED ----------------
@app.route("/recommend/text", methods=["GET"])
def recommend_text():
    query = request.args.get("query")

    if not query:
        return error_response("Please provide a text query using ?query=")

    results = recommender.recommend_by_text(query)

    return success_response({
        "type": "text-based-ai",
        "query": query,
        "results": results
    })


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)
