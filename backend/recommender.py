import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib


class MusicRecommender:
    def __init__(self, data_path, sample_size=30000):
        self.data = pd.read_csv(data_path)

        # Sample for development (industry practice)
        if len(self.data) > sample_size:
            self.data = self.data.sample(sample_size, random_state=42)

        self.audio_features = [
            'danceability', 'energy', 'loudness',
            'speechiness', 'acousticness',
            'instrumentalness', 'liveness',
            'valence', 'tempo'
        ]

        self.scaler = StandardScaler()
        self.audio_model = None
        self.audio_matrix = None

        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_embeddings = None

        self._prepare_models()

    def _prepare_models(self):
        self.data = self.data.dropna(subset=self.audio_features).reset_index(drop=True)

        # ---------- AUDIO ----------
        self.audio_matrix = self.scaler.fit_transform(self.data[self.audio_features])

        self.audio_model = NearestNeighbors(
            n_neighbors=10,
            metric="cosine",
            algorithm="brute"
        )
        self.audio_model.fit(self.audio_matrix)

        # ---------- NLP (CACHED) ----------
        cache_path = "data/text_embeddings.pkl"

        if os.path.exists(cache_path):
            self.text_embeddings = joblib.load(cache_path)
        else:
            corpus = (self.data["name"] + " " + self.data["artists"].astype(str)).tolist()
            self.text_embeddings = self.text_model.encode(
                corpus, batch_size=64, show_progress_bar=True
            )
            joblib.dump(self.text_embeddings, cache_path)

    # ---------- SONG BASED (FUZZY MATCH) ----------
    def recommend_by_song(self, song_query, top_n=5):
        song_query = song_query.lower()

        matches = self.data[
            self.data["name"].str.lower().str.contains(song_query, na=False)
        ]

        if matches.empty:
            return []

        idx = matches.index[0]

        distances, indices = self.audio_model.kneighbors(
            [self.audio_matrix[idx]], n_neighbors=top_n + 1
        )

        return [
            {
                "song": self.data.iloc[i]["name"],
                "artist": self.data.iloc[i]["artists"],
                "score": round(float(1 - dist), 3)
            }
            for i, dist in zip(indices[0][1:], distances[0][1:])
        ]

    # ---------- MOOD BASED ----------
    def recommend_by_mood(self, mood, top_n=5):
        mood_map = {
            "happy": {"valence": (0.6, 1.0), "energy": (0.6, 1.0)},
            "sad": {"valence": (0.0, 0.4), "energy": (0.0, 0.5)},
            "energetic": {"energy": (0.7, 1.0)},
            "chill": {"energy": (0.0, 0.4), "acousticness": (0.4, 1.0)}
        }

        if mood not in mood_map:
            return []

        df = self.data.copy()
        for f, (lo, hi) in mood_map[mood].items():
            df = df[(df[f] >= lo) & (df[f] <= hi)]

        df = df.sample(min(top_n, len(df)))

        return [
            {"song": r["name"], "artist": r["artists"], "mood": mood}
            for _, r in df.iterrows()
        ]

    # ---------- NLP BASED ----------
    def recommend_by_text(self, query, top_n=5):
        q_emb = self.text_model.encode([query])
        scores = cosine_similarity(q_emb, self.text_embeddings)[0]
        idxs = np.argsort(scores)[::-1][:top_n]

        return [
            {
                "song": self.data.iloc[i]["name"],
                "artist": self.data.iloc[i]["artists"],
                "score": round(float(scores[i]), 3)
            }
            for i in idxs
        ]
