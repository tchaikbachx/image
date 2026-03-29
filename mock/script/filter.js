/*  +-------------+ 
    |  FILTERING  |
    +----- -------+*/

// search
function filterDash() {
    let input = document.getElementById('dashboardSearch').value.toLowerCase();
    let cards = document.getElementsByClassName('card');
    for (let i = 0; i < cards.length; i++) {
        let text = cards[i].innerText.toLowerCase();
        // show matching texts
        cards[i].style.display = text.includes(input) ? "block" : "none";
    } // for
} // filterDash

// filter
function filterCategory(category) {
    let cards = document.getElementsByClassName('card');
    for (let i = 0; i < cards.length; i++) {
        if (category === 'all') {
            cards[i].style.display = "block";
        } else {
            // show matching category
            cards[i].style.display = cards[i].getAttribute('data-category') === category ? "block" : "none";
        } // elif
    } // for
} // filterCategory