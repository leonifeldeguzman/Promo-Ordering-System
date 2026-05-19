async function searchPromos() {

    const budget = document.getElementById('budgetInput').value;

    const response = await fetch(`/promos/budget/${budget}`);

    const data = await response.json();

    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = '';

    data.forEach(promo => {

        resultsDiv.innerHTML += `
            <div class="promo-card">
                <h3>${promo.name}</h3>
                <p>Category: ${promo.category}</p>
                <p>Price: ₱${promo.price}</p>
                <p>${promo.description}</p>
            </div>
        `;
    });
}