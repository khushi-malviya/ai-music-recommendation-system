import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

class MusicRecommender:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

        self.features = [
            'danceability', 'energy', 'loudness',
            'speechiness', 'acousticness',
            'instrumentalness', 'liveness',
            'valence', 'tempo'
        ]

        self.scaler = StandardScaler()
        self.model = None
        self.feature_matrix = None

        self._prepare_model()

    def _prepare_model(self):
        # Drop rows with missing values
        self.data = self.data.dropna(subset=self.features).reset_index(drop=True)

        # Scale features
        scaled_features = self.scaler.fit_transform(self.data[self.features])
        self.feature_matrix = scaled_features

        # Train KNN model
        self.model = NearestNeighbors(
            n_neighbors=6,
            metric='cosine',
            algorithm='brute'
        )
        self.model.fit(self.feature_matrix)

    def recommend(self, song_name, n_recommendations=5):
        if song_name not in self.data['name'].values:
            return []

        idx = self.data[self.data['name'] == song_name].index[0]
        distances, indices = self.model.kneighbors(
            [self.feature_matrix[idx]],
            n_neighbors=n_recommendations + 1
        )

        recommendations = []

        for i, dist in zip(indices[0][1:], distances[0][1:]):
            recommendations.append({
                "song": self.data.iloc[i]['name'],
                "artist": self.data.iloc[i]['artists'],
                "similarity": round(1 - dist, 3)
            })

        return recommendations
