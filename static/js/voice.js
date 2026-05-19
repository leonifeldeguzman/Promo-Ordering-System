function startVoiceRecognition() {

    const micBtn = document.getElementById('micBtn');
    const status = document.getElementById('status');
    const micIndicator = document.getElementById('micIndicator');
    const resultsDiv = document.getElementById('results');

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = 'en-US';
    recognition.interimResults = false;

    micBtn.style.background = "red";
    micIndicator.innerText = "Mic is ON 🔴 Listening...";
    micIndicator.style.color = "red";
    status.innerText = "Listening... speak now";

    recognition.onresult = async function(event) {

        const transcript = event.results[0][0].transcript;
        status.innerText = "Heard: " + transcript;

        const numbers = transcript.match(/\d+/);

        if (!numbers) {
            status.innerText = "No budget detected.";
            return;
        }

        const budget = numbers[0];

        // CALL BACKEND
        const response = await fetch(`/promos/budget/${budget}`);
        const data = await response.json();

        // SHOW RESULTS
        resultsDiv.innerHTML = "";

        if (data.length === 0) {
            resultsDiv.innerHTML = "<p>No promos found.</p>";
        } else {
            data.forEach(promo => {
                resultsDiv.innerHTML += `
                    <div class="promo-card">
                        <h3>${promo.name}</h3>
                        <p>${promo.category}</p>
                        <p>₱${promo.price}</p>
                        <p>${promo.description}</p>
                    </div>
                `;
            });
        }
    };

    recognition.onerror = function() {
        status.innerText = "Voice error. Try again.";
    };

    recognition.onend = function() {
        micBtn.style.background = "#ffcc00";
        micIndicator.innerText = "Mic is OFF ⚪";
        micIndicator.style.color = "gray";
    };

    recognition.start();
}