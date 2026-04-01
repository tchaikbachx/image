/*  +-------------+ 
    |  FILTERING  |
    +----- -------+*/


// these are scripts that control the filtering capabilities and contains
// helpers that aid the searching process. like everything else, nothing
// is named in a streamlined manner, sorry about that; will fix soon.


/**
 * This is the main filtering workhorse; it handles the larger search bar
 * and advanced search modal.
 */
function applyFilters() {
    const globalInput = document.getElementById('dashboardSearch').value.toLowerCase();
    // advanced input categories
    const advType = document.getElementById('adv_Type').value.toLowerCase();
    const advMake = document.getElementById('adv_Make').value.toLowerCase();
    const advGrade = document.getElementById('adv_Grade').value.toLowerCase();
    const advLoc = document.getElementById('adv_Loc').value.toLowerCase();
    const advSerial = document.getElementById('adv_Serial').value.toLowerCase();
    const maxPrice = parseFloat(document.getElementById('adv_PriceMax').value) || 9999;

    const cards = document.getElementsByClassName('instrument-card');

    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];

        const name = card.querySelector('.row-title')?.innerText.toLowerCase() || "";
        const type = card.querySelector('.col-type .row-data')?.innerText.toLowerCase() || "";
        const make = card.querySelector('.col-brand .row-data')?.innerText.toLowerCase() || "";

        // get model and price from the data attributes we just added
        const model = card.getAttribute('data-model')?.toLowerCase() || "";
        const price = parseFloat(card.getAttribute('data-price')) || 0;

        // get adv fields from the hidden spans
        const grade = card.querySelector('.col-grade .row-data')?.innerText.toLowerCase() || "";
        const serial = card.querySelector('.col-serial .row-data')?.innerText.toLowerCase() || "";
        const location = card.querySelector('.locker-info')?.innerText.toLowerCase() || "";

        // check if the input is in name, type, make, or model
        const matchesGlobal = !globalInput || 
            name.includes(globalInput) || 
            type.includes(globalInput) || 
            make.includes(globalInput) || 
            model.includes(globalInput);

        // adv filtering logic based on input
        const matchesAdv = (!advType || type.includes(advType)) &&
                           (!advMake || make.includes(advMake)) &&
                           (!advGrade || grade.includes(advGrade)) &&
                           (!advLoc || location.includes(advLoc)) &&
                           (!advSerial || serial.includes(advSerial)) &&
                           (price <= maxPrice);

        // visibility adjustments
        if (matchesGlobal && matchesAdv) {
            card.style.display = "flex";
        } else {
            card.style.display = "none";
        } // elif
    } // for
} // applyFilterss

/**
 * ...
 * @param {*} val 
 */
function updatePriceLabel(val) {
    document.getElementById('priceDisplay').innerText = `Max Price: $${val}`;
    applyFilters();
} // updatePriceLabel

/**
 * ...
 */
function openAdvancedModal() {
    document.getElementById('advancedFilterModal').classList.add('active');
} // openAdvancedModal

/**
 * ...
 */
function closeAdvancedModal() {
    document.getElementById('advancedFilterModal').classList.remove('active');
} // closeAdvancedModal

/**
 * ...
 */
function resetAllFilters() {
    document.getElementById('dashboardSearch').value = '';
    document.getElementById('adv_Type').value = '';
    document.getElementById('adv_Make').value = '';
    document.getElementById('adv_Grade').value = '';
    document.getElementById('adv_Loc').value = '';
    document.getElementById('adv_Serial').value = '';
    document.getElementById('adv_PriceMax').value = 9999;
    document.getElementById('priceDisplay').innerText = `Max Price: $9999`;
    applyFilters();
} // resetAllFilters