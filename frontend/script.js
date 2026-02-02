const API_BASE_URL = "http://127.0.0.1:5000";

/* ---------------- DOM READY ---------------- */
document.addEventListener("DOMContentLoaded", () => {
    setupTabs();
    setupButtons();
});

/* ---------------- TAB LOGIC ---------------- */
function setupTabs() {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            document.getElementById(tab.dataset.tab).classList.add("active");
        });
    });
}

/* ---------------- BUTTON EVENTS ---------------- */
function setupButtons() {
    document.getElementById("songBtn").addEventListener("click", getSongRecommendations);
    document.getElementById("moodBtn").addEventListener("click", getMoodRecommendations);
    document.getElementById("textBtn").addEventListener("click", getTextRecommendations);
}

/* ---------------- LOADING ---------------- */
function setLoading(isLoading) {
    const resultsArea = document.getElementById("resultsArea");
    const buttons = document.querySelectorAll(".card button");

    buttons.forEach(btn => btn.disabled = isLoading);

    if (isLoading) {
        resultsArea.innerHTML = "<p>⏳ AI is thinking...</p>";
    }
}

/* ---------------- SONG ---------------- */
function getSongRecommendations() {
    const song = document.getElementById("songInput").value.trim();
    if (!song) return showMessage("Please enter a song name");

    setLoading(true);
    fetch(`${API_BASE_URL}/recommend/song?query=${encodeURIComponent(song)}`)
        .then(r => r.json())
        .then(renderResults)
        .finally(() => setLoading(false));
}

/* ---------------- MOOD ---------------- */
function getMoodRecommendations() {
    const mood = document.getElementById("moodSelect").value;
    if (!mood) return showMessage("Please select a mood");

    setLoading(true);
    fetch(`${API_BASE_URL}/recommend/mood?mood=${encodeURIComponent(mood)}`)
        .then(r => r.json())
        .then(renderResults)
        .finally(() => setLoading(false));
}

/* ---------------- AI TEXT ---------------- */
function getTextRecommendations() {
    const query = document.getElementById("textQueryInput").value.trim();
    if (!query) return showMessage("Please enter a query");

    setLoading(true);
    fetch(`${API_BASE_URL}/recommend/text?query=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(renderResults)
        .finally(() => setLoading(false));
}

/* ---------------- RENDER ---------------- */
function renderResults(res) {
    const area = document.getElementById("resultsArea");

    if (res.status !== "success") {
        area.innerHTML = `<p>${res.message}</p>`;
        return;
    }

    const items = res.data.results;
    if (!items.length) {
        area.innerHTML = "<p>No results found.</p>";
        return;
    }

    area.innerHTML = `
        <ul>
            ${items.map(i => `
                <li>
                    <strong>${i.song}</strong><br/>
                    <em>${i.artist}</em>
                    ${i.score !== undefined ? `<br/>Score: ${i.score}` : ""}
                </li>
                <hr/>
            `).join("")}
        </ul>
    `;
}

/* ---------------- MESSAGE ---------------- */
function showMessage(msg) {
    document.getElementById("resultsArea").innerHTML = `<p>${msg}</p>`;
}
