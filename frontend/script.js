const API_BASE_URL = "http://127.0.0.1:5000";

/* ---------------- SONG BASED ---------------- */
function getSongRecommendations() {
    const songName = document.getElementById("songInput").value.trim();
    const resultsArea = document.getElementById("resultsArea");

    if (!songName) {
        resultsArea.innerHTML = "<p>Please enter a song name.</p>";
        return;
    }

    resultsArea.innerHTML = "<p>Loading recommendations...</p>";

    fetch(`${API_BASE_URL}/recommend/song?query=${encodeURIComponent(songName)}`)
        .then(res => res.json())
        .then(data => renderResults(data))
        .catch(() => {
            resultsArea.innerHTML = "<p>Error connecting to server.</p>";
        });
}

/* ---------------- MOOD BASED ---------------- */
function getMoodRecommendations() {
    const mood = document.getElementById("moodSelect").value;
    const resultsArea = document.getElementById("resultsArea");

    if (!mood) {
        resultsArea.innerHTML = "<p>Please select a mood.</p>";
        return;
    }

    resultsArea.innerHTML = "<p>Loading recommendations...</p>";

    fetch(`${API_BASE_URL}/recommend/mood?mood=${encodeURIComponent(mood)}`)
        .then(res => res.json())
        .then(data => renderResults(data))
        .catch(() => {
            resultsArea.innerHTML = "<p>Error connecting to server.</p>";
        });
}

/* ---------------- AI TEXT BASED ---------------- */
function getTextRecommendations() {
    const query = document.getElementById("textQueryInput").value.trim();
    const resultsArea = document.getElementById("resultsArea");

    if (!query) {
        resultsArea.innerHTML = "<p>Please enter a text query.</p>";
        return;
    }

    resultsArea.innerHTML = "<p>Loading AI recommendations...</p>";

    fetch(`${API_BASE_URL}/recommend/text?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => renderResults(data))
        .catch(() => {
            resultsArea.innerHTML = "<p>Error connecting to server.</p>";
        });
}

/* ---------------- COMMON RENDERER ---------------- */
function renderResults(apiResponse) {
    const resultsArea = document.getElementById("resultsArea");

    if (apiResponse.status !== "success") {
        resultsArea.innerHTML = `<p>${apiResponse.message}</p>`;
        return;
    }

    const results = apiResponse.data.results;

    if (!results || results.length === 0) {
        resultsArea.innerHTML = "<p>No recommendations found.</p>";
        return;
    }

    let html = "<ul>";
    results.forEach(item => {
        html += `
            <li>
                <strong>${item.song}</strong><br/>
                <em>${item.artist}</em>
                ${item.score !== undefined ? `<br/>Score: ${item.score}` : ""}
            </li>
            <hr/>
        `;
    });
    html += "</ul>";

    resultsArea.innerHTML = html;
}
