from recommender import MusicRecommender

if __name__ == "__main__":
    recommender = MusicRecommender("data/spotify_tracks.csv")

    print("\n--- SONG BASED ---")
    print(recommender.recommend_by_song("Blinding Lights"))

    print("\n--- MOOD BASED ---")
    print(recommender.recommend_by_mood("sad"))

    print("\n--- NLP BASED ---")
    print(recommender.recommend_by_text("sad hindi song"))
