
function startVoiceRecognition() {

    const micBtn = document.getElementById('micBtn');
    const status = document.getElementById('status');
    const micIndicator = document.getElementById('micIndicator');
    const resultsDiv = document.getElementById('results');

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("SpeechRecognition not supported in this browser");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    // UI ON
    micBtn.style.background = "red";
    micIndicator.innerText = "Mic is ON 🔴 Listening...";
    micIndicator.style.color = "red";
    status.innerText = "Listening... speak now";

    recognition.onresult = async function(event) {

        const transcript = event.results[0][0].transcript.toLowerCase();
        status.innerText = "Heard: " + transcript;

        // extract budget
        const numbers = transcript.match(/\d+/);
        let budget = numbers ? numbers[0] : null;

        // detect category
        let category = "";

        if (transcript.includes("chicken")) category = "Chicken";
        else if (transcript.includes("burger")) category = "Burger";
        else if (transcript.includes("fries")) category = "Fries";
        else if (transcript.includes("rice")) category = "Rice Meal";
        else if (transcript.includes("drink")) category = "Drinks";

        // build API URL
        let url = "";

        if (category && budget) url = `/promos/${category}/${budget}`;
        else if (category) url = `/promos/category/${category}`;
        else if (budget) url = `/promos/budget/${budget}`;
        else url = `/promos`;

        try {

            const response = await fetch(url);
            const data = await response.json();

            resultsDiv.innerHTML = "";

            let reply = "";

            if (data.length === 0) {
                resultsDiv.innerHTML = "<p>No promos found.</p>";
                reply = "Sorry, no promos found.";
            } else {
                reply = `I found ${data.length} promos for you.`;

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

            // 🔊 SPEAK BACK (TEXT TO SPEECH)
            const speech = new SpeechSynthesisUtterance(reply);
            speech.lang = "en-US";
            speech.rate = 1;
            window.speechSynthesis.speak(speech);

        } catch (err) {
            console.error(err);
            status.innerText = "Error fetching promos.";
        }
    };

    recognition.onerror = function() {
        status.innerText = "Voice recognition error.";
    };

    recognition.onend = function() {
        micBtn.style.background = "#ffcc00";
        micIndicator.innerText = "Mic is OFF ⚪";
        micIndicator.style.color = "gray";
    };

    recognition.start();
}