// Voice Control + AI Integration for SpeakNSave

let recognition = null;
let isListening = false;

// Initialize speech recognition
function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-PH';  // Supports Filipino/English
        
        recognition.onresult = async (event) => {
            const command = event.results[0][0].transcript;
            console.log('Voice command:', command);
            document.getElementById('voiceStatus').innerText = `You said: "${command}"`;
            await handleVoiceCommand(command);
        };
        
        recognition.onerror = (event) => {
            console.error('Voice error:', event.error);
            document.getElementById('voiceStatus').innerText = 'Error: ' + event.error;
            isListening = false;
        };
        
        recognition.onend = () => {
            isListening = false;
            document.getElementById('voiceBtn').style.background = '#007bff';
        };
    } else {
        alert('Voice recognition not supported in this browser. Use Chrome.');
    }
}

// Start listening
function startListening() {
    if (recognition && !isListening) {
        recognition.start();
        isListening = true;
        document.getElementById('voiceBtn').style.background = '#28a745';
        document.getElementById('voiceStatus').innerText = 'Listening...';
    }
}

// Main voice command handler with AI integration
async function handleVoiceCommand(command) {
    const lowerCommand = command.toLowerCase();
    
    // ---- AI-POWERED FEATURES (Emerging Tech) ----
    
    // Check for AI recommendation requests
    if (lowerCommand.includes('recommend') || 
        lowerCommand.includes('suggest') || 
        lowerCommand.includes('what should i get') ||
        lowerCommand.includes('what do you recommend') ||
        lowerCommand.includes('help me decide')) {
        
        await getAIRecommendation(command);
        return;
    }
    
    // Check for AI promo suggestion
    if (lowerCommand.includes('best promo') || 
        lowerCommand.includes('suggest promo') ||
        lowerCommand.includes('value meal')) {
        
        await getAIPromoSuggestion(command);
        return;
    }
    
    // ---- REGULAR VOICE COMMANDS (Existing functionality) ----
    
    // Search by price
    const priceMatch = lowerCommand.match(/(?:under|below|less than|₱|peso)(\d+)/);
    if (priceMatch) {
        const price = parseInt(priceMatch[1]);
        searchByPrice(price);
        return;
    }
    
    // Search by category
    if (lowerCommand.includes('burger')) {
        searchByCategory('Burgers');
    } else if (lowerCommand.includes('drink')) {
        searchByCategory('Drinks');
    } else if (lowerCommand.includes('rice meal')) {
        searchByCategory('Rice Meals');
    }
    
    // Search promo
    else if (lowerCommand.includes('promo')) {
        searchPromos();
    }
    
    // Add item (admin only)
    else if (lowerCommand.includes('add') && lowerCommand.includes('item')) {
        // Extract name and price from voice
        const nameMatch = command.match(/add (.+?) (?:for|at|₱|price)/i);
        const priceMatchVoice = command.match(/(\d+)/);
        if (nameMatch && priceMatchVoice) {
            addItemViaVoice(nameMatch[1], priceMatchVoice[1]);
        }
    }
    
    else {
        document.getElementById('voiceResult').innerHTML = `🔍 Searching for: "${command}"`;
        searchByText(command);
    }
}

// ---- AI INTEGRATION FUNCTIONS (Emerging Tech) ----

async function getAIRecommendation(command) {
    showAILoader();
    
    try {
        const response = await fetch('/api/ai/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        });
        
        const data = await response.json();
        
        if (data.recommended_item && data.recommended_item !== 'none') {
            showAIResult(`
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; margin: 10px 0;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 2rem;">🤖</span>
                        <span style="font-weight: bold;">AI Recommendation (Gemini)</span>
                    </div>
                    <div style="font-size: 1.5rem; margin: 10px 0;">🍔 ${data.recommended_item}</div>
                    <div>💰 Price: ₱${data.price}</div>
                    <div>📂 Category: ${data.category}</div>
                    <div>💡 ${data.reason}</div>
                    <button onclick="addToCart('${data.recommended_item}', ${data.price})" style="margin-top: 10px; padding: 8px 16px; background: #ff5722; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        🛒 Add to Order
                    </button>
                </div>
            `);
            
            // Speak the recommendation aloud
            speakText(`I recommend ${data.recommended_item} for ${data.reason}`);
        } else {
            showAIResult(`
                <div style="background: #ff9800; color: white; padding: 15px; border-radius: 10px;">
                    🤖 ${data.reason || "No matching items found. Try saying 'meals under 150' or 'burger promo'"}
                </div>
            `);
        }
    } catch (error) {
        console.error('AI error:', error);
        showAIResult('⚠️ AI service unavailable. Using regular search instead.');
        searchByText(command);  // Fallback
    }
}

async function getAIPromoSuggestion(command) {
    showAILoader();
    
    try {
        const response = await fetch('/api/ai/suggest-promo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ craving: command })
        });
        
        const data = await response.json();
        
        showAIResult(`
            <div style="background: #e91e63; color: white; padding: 20px; border-radius: 15px;">
                <div>🏷️ BEST PROMO SUGGESTION</div>
                <div style="font-size: 1.3rem;">${data.suggestion} - ₱${data.price}</div>
                <div>${data.why}</div>
                <div>💎 ${data.savings}</div>
            </div>
        `);
    } catch (error) {
        console.error('Promo AI error:', error);
    }
}

// UI Helper Functions
function showAILoader() {
    const resultDiv = document.getElementById('voiceResult');
    if (resultDiv) {
        resultDiv.innerHTML = '<div style="text-align: center;">🤖 AI is thinking <span class="dot-animation">...</span></div>';
    }
}

function showAIResult(html) {
    const resultDiv = document.getElementById('voiceResult');
    if (resultDiv) {
        resultDiv.innerHTML = html;
    }
}

function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-PH';
        window.speechSynthesis.speak(utterance);
    }
}

// Your existing functions (searchByPrice, searchByCategory, etc.)
function searchByPrice(price) {
    // Your existing implementation
    window.location.href = `/menu?max_price=${price}`;
}

function searchByCategory(category) {
    window.location.href = `/menu?category=${category}`;
}

function searchPromos() {
    window.location.href = '/promos';
}

function searchByText(text) {
    window.location.href = `/menu?search=${encodeURIComponent(text)}`;
}

function addItemViaVoice(name, price) {
    // Your existing implementation
    fetch('/api/menu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ menu_name: name, price: price })
    });
}

function addToCart(item, price) {
    // Your existing cart implementation
    alert(`Added ${item} to order!`);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initVoiceRecognition();
    
    // Add microphone button to page if not exists
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.onclick = startListening;
    }
});