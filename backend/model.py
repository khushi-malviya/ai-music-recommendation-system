from recommender import MusicRecommender

if __name__ == "__main__":
    recommender = MusicRecommender("data/spotify_tracks.csv")

    song = "Blinding Lights"  # try any song from dataset
    recommendations = recommender.recommend(song)

    print(f"\nRecommendations for '{song}':\n")
    for r in recommendations:
        print(f"{r['song']} by {r['artist']} (score: {r['similarity']})")
