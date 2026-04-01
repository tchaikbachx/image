/*  +-------------+ 
    |  FETCHING   |
    +----- -------+*/

let isDeleteMode = false;
let isEditMode = false;
let currentEditId = null;
let activeInstrument = null;

// the bulk of .js functions that interact with the (python) localhost server
// on port 5000. mostly, they deal with:
//      > deleting,
//      > adding, and
//      > editing entries
// in the instruments database.

// there are a lot of functions that have minimal and/or no comments; i will
// go back and write better comments later, in addition to cleaning it up a bit.


// +----------------------------------------------------------------------------+
// |                                                                   GENERAL  |
// +----------------------------------------------------------------------------+


/**
 * ...
 * @param {*} tabName 
 */
function switchTab(tabName) {
    // deal with the buttons
    document.getElementById('tab-details').classList.toggle('active', tabName === 'details');
    document.getElementById('tab-manage').classList.toggle('active', tabName === 'manage');

    // deal with restricted content visibility
    const detailsPane = document.getElementById('details-content');
    const managePane = document.getElementById('manage-content');

    if (tabName === 'details') {
        detailsPane.style.display = 'block';
        managePane.style.display = 'none';
    } else {
        detailsPane.style.display = 'none';
        managePane.style.display = 'block';
    } // elif
} // switchTab

/**
 * ...
 * @param {*} input 
 * @returns 
 */
function formatPrice(input) {
    let value = parseFloat(input.value);
    
    // val must be numerical
    if (isNaN(value)) {
        input.value = "0.00";
        return;
    } // if

    // val must be > 0
    if (value < 0) value = 0;

    // force 2 decimal places
    input.value = value.toFixed(2);
} // formatPrice

/**
 * ...
 * @param {*} type 
 * @returns 
 */
async function processTransaction(type) {
    if (!activeInstrument) {
        console.error("No active instrument selected for transaction.");
        return;
    } // if

    // build payload
    const payload = {
        item_id: activeInstrument.Name_ID,
        type: type // 'checkout' or 'checkin'
    };

    // validate and add fields if we are checking out
    if (type === 'checkout') {
        const emailInput = document.getElementById('checkout-email');
        const dateInput = document.getElementById('checkout-due');
        
        const email = emailInput ? emailInput.value.trim() : "";
        const dueDate = dateInput ? dateInput.value : "";

        if (!email.endsWith('@grinnell.edu')) {
            alert("Please enter a valid @grinnell.edu email address.");
            return;
        } // if

        if (!dueDate) {
            alert("Please select a due date.");
            return;
        } // if

        payload.borrower_email = email;
        payload.due_date = dueDate;
    } // if

    // process fetch for checkout/ins
    try {
        const response = await fetch('/api/transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert(`Instrument ${type === 'checkout' ? 'checked out' : 'returned'} successfully!`);
            location.reload(); // Refresh to update the UI status pills
        } else {
            const errorData = await response.json();
            alert("Error: " + (errorData.message || "The server could not process the transaction."));
        } // elif
    } catch (err) {
        console.error("Connection error:", err);
        alert("Failed to connect to the server. Check if your backend is running.");
    } // try/catch
} // processTransaction

/**
 * Fetches instruments from the server and loads in the grid, which
 * contains the instruments on display. This also includes logic for
 * sidebar selection, hovering, and mode-switching.
 */
async function loadInstruments() {
    const grid = document.getElementById('instrument-grid');
    if (!grid) return;

    try {
        const response = await fetch('/api/instruments');
        const instruments = await response.json();
        grid.innerHTML = ''; 

        instruments.forEach(item => {
            const card = document.createElement('div');
            card.className = 'instrument-card compact-row'; 
            card.dataset.id = item.Name_ID; 
            
            // store price as attribute for the slider
            card.setAttribute('data-price', item.Price || '0');
            // store model for search bar
            card.setAttribute('data-model', item.Model || '');

            const rawStatus = item.Status || item.status || '';
            const isAvailable = rawStatus.trim().toUpperCase() === 'IN';
            const statusClass = isAvailable ? 'status-in' : 'status-out';
            const statusLabel = isAvailable ? 'IN' : 'OUT';

            const rawLocation = item.Stored_In || 'No Location';
            const locationPrefix = !isNaN(parseFloat(rawLocation)) && isFinite(rawLocation) ? 'Locker:' : '';
            const locationDisplay = `${locationPrefix} ${rawLocation}`;

            card.innerHTML = `
                <div class="row-grid-container">
                    <div class="col-status">
                        <span class="status-indicator-pill ${statusClass}">${statusLabel}</span>
                    </div>
                    <div class="col-name">
                        <span class="row-title">${item.Name_ID}</span>
                    </div>
                    <div class="col-type">
                        <span class="row-label">TYPE</span>
                        <span class="row-data">${item.Type}</span>
                    </div>
                    <div class="col-brand">
                        <span class="row-label">MAKE</span>
                        <span class="row-data">${item.Make || '---'}</span>
                    </div>
                    <div class="col-end">
                        <div class="action-zone delete-zone">
                            <button class="mode-action-btn delete-btn" onclick="deleteInstrument('${item.Name_ID}', event)">REMOVE</button>
                        </div>
                        <div class="action-zone edit-zone">
                            <button class="mode-action-btn edit-btn" onclick="openUpdateModal(${JSON.stringify(item).replace(/"/g, '&quot;')})">MODIFY</button>
                        </div>
                        <div class="locker-info">${locationDisplay}</div>
                        
                        <span class="col-grade" style="display:none;"><span class="row-data">${item.Grade || ''}</span></span>
                        <span class="col-serial" style="display:none;"><span class="row-data">${item.Serial_Number || ''}</span></span>
                    </div>
                </div>
            `;

            card.onclick = (e) => {
                if (typeof isDeleteMode !== 'undefined' && (isDeleteMode || isEditMode)) return;
                if (e.target.closest('.mode-action-btn')) return;
                showDetails(item);
            };

            grid.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading instruments:", error);
    } // try/catch
} // loadInstruments


/**
 * Close modal if user clicks outside (e.g., background).
 * @param {*} event 
 */
window.onclick = function(event) {
    const modal = document.getElementById('addInstrumentModal');
    if (event.target == modal) closeAddModal();
} // window.onclick

/**
 * starting listening for instrument fluctuations
 */
window.addEventListener('DOMContentLoaded', loadInstruments);

// +----------------------------------------------------------------------------+
// |                                                                   EDITING  |
// +----------------------------------------------------------------------------+

/**
 * ...
 */
function toggleEditMode() {
    isEditMode = !isEditMode;
    const editBtn = document.getElementById('edit-mode-btn');
    if (isEditMode) {
        document.body.classList.add('edit-mode');
        editBtn.classList.add('edit-active');
        // if on, turn off delete mode; only one active mode can exist max
        isDeleteMode = false;
        document.body.classList.remove('delete-mode');
        document.getElementById('delete-mode-btn')?.classList.remove('delete-active');
    } else {
        document.body.classList.remove('edit-mode');
        editBtn.classList.remove('edit-active');
    } // elif
} // toggleEditMode

/**
 * ...
 */
function toggleDeleteMode() {
    isDeleteMode = !isDeleteMode;
    const deleteBtn = document.getElementById('delete-mode-btn');
    if (isDeleteMode) {
        document.body.classList.add('delete-mode');
        deleteBtn.classList.add('delete-active');
        // if on, turn off edit mode; only one active mode can exist max
        isEditMode = false;
        document.body.classList.remove('edit-mode');
        document.getElementById('edit-mode-btn')?.classList.remove('edit-active');
    } else {
        document.body.classList.remove('delete-mode');
        deleteBtn.classList.remove('delete-active');
    } // elif
} // toggleDeleteMode

/**
 * Controls the action of opening the modal & filling out any fields the
 * instrument already has.
 * @param {*} item 
 */
function openUpdateModal(item) {
    currentEditId = item.ID;
    
    // new modal title and text
    const modal = document.getElementById('addInstrumentModal');
    modal.querySelector('h2').textContent = "Update Instrument";
    const saveBtn = modal.querySelector('button[onclick="submitNewInstrument()"]');
    saveBtn.textContent = "Update Database";
    saveBtn.setAttribute('onclick', 'submitUpdate()');

    // get and fill all the fields
    document.getElementById('m_Name_ID').value = item.Name_ID || '';
    document.getElementById('m_Type').value = item.Type || '';
    document.getElementById('m_Make').value = item.Make || '';
    document.getElementById('m_Model').value = item.Model || '';
    document.getElementById('m_Grade').value = item.Grade || '';
    document.getElementById('m_Old_ID').value = item.Old_ID || '';
    document.getElementById('m_Serial').value = item.Serial_Number || '';
    document.getElementById('m_Price').value = item.Price || 0;
    document.getElementById('m_Stored').value = item.Stored_In || '';
    document.getElementById('m_Dept').value = item.Dept || '';

    modal.classList.add('active');
} // openUpdateModal

/**
 * ...
 * @returns 
 */
async function submitUpdate() {
    if (!currentEditId) return;
    // get all the updated instrument data
    const updatedData = {
        Name_ID: document.getElementById('m_Name_ID').value,
        Type: document.getElementById('m_Type').value,
        Make: document.getElementById('m_Make').value,
        Model: document.getElementById('m_Model').value,
        Grade: document.getElementById('m_Grade').value,
        Old_ID: document.getElementById('m_Old_ID').value,
        Serial_Number: document.getElementById('m_Serial').value,
        Price: parseFloat(document.getElementById('m_Price').value) || 0,
        Stored_In: document.getElementById('m_Stored').value,
        Dept: document.getElementById('m_Dept').value
    };

    try {
        // send put server request, hopefully it goes through
        const response = await fetch(`/api/instruments/${currentEditId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        });

        if (response.ok) {
            console.log("Update successful!");
            closeAddModal();
            loadInstruments();
        } else {
            const error = await response.json();
            alert("Update failed: " + error.message);
        } // elif
    } catch (err) {
        console.error("Error submitting update:", err);
    } // try/catch
} // submitUpdate

// +----------------------------------------------------------------------------+
// |                                                                  DELETING  |
// +----------------------------------------------------------------------------+

/**
 * ...
 * @param {*} id 
 * @param {*} event 
 * @param {*} item 
 */
function onCardClick(id, event, item) {
    if (isDeleteMode) {
        deleteInstrument(id, event);
    } else if (isEditMode) {
        openUpdateModal(item);
    } else {
        showDetails(item);
    } // elif
} // onCardClick

/**
 * ...
 * @param {*} id 
 * @param {*} event 
 * @returns 
 */
async function deleteInstrument(id, event) {
    if (event) event.stopPropagation();
    if (!confirm(`Confirm deletion of instrument #${id}?`)) return;
    try {
        const response = await fetch(`/api/instruments/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // remove entry, turn delete mode off
            event.target.closest('.instrument-card').remove();
            toggleDeleteMode(); 
        } else {
            alert("Delete failed on server.");
        } // elif
    } catch (err) {
        console.error("Error:", err);
    } // try/catch
} // deleteInstrument

// +----------------------------------------------------------------------------+
// |                                                                    ADDING  |
// +----------------------------------------------------------------------------+

/**
 * General modal UI controls.
 */
function openAddModal() {
    document.getElementById('addInstrumentModal').classList.add('active');
} // openAddModal

/**
 * ...
 */
function closeAddModal() {
    const modal = document.getElementById('addInstrumentModal');
    const form = document.getElementById('addInstrumentForm');
    
    // hide modal
    modal.classList.remove('active');
    
    // reset add behavior
    modal.querySelector('h2').textContent = "Add New Instrument";
    const saveBtn = modal.querySelector('button[onclick^="submit"]');
    saveBtn.textContent = "Save";
    saveBtn.setAttribute('onclick', 'submitNewInstrument()');

    // clear all input fields & tracking ID
    form.reset();
    currentEditId = null;
    
    // turn mode off
    if (isEditMode) toggleEditMode();
} // closeAddModal

/**
 * ...
 * @returns 
 */
async function submitNewInstrument() {
    // match the fields in instrument table
    const payload = {
        Name_ID: document.getElementById('m_Name_ID').value,
        Type: document.getElementById('m_Type').value,
        Make: document.getElementById('m_Make').value,
        Model: document.getElementById('m_Model').value,
        Grade: document.getElementById('m_Grade').value,
        Old_ID: document.getElementById('m_Old_ID').value,
        Serial_Number: document.getElementById('m_Serial').value,
        Price: document.getElementById('m_Price').value,
        Stored_In: document.getElementById('m_Stored').value,
        Dept: document.getElementById('m_Dept').value,
        Picture: ""
    };

    // validate fields poorly
    if (!payload.Name_ID || !payload.Type) {
        alert("Name and Type are required!");
        return;
    } // if

    // send payload data to the server
    try {
        const response = await fetch('/api/instruments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Instrument added successfully!");
            closeAddModal();
            location.reload();
        } else {
            const err = await response.json();
            alert("Error: " + err.message);
        } // elif
    } catch (error) {
        console.error("Submission failed:", error);
    } // try/catch
} // submitNewInstrument

/**
 * ...
 * @param {*} item 
 * @returns 
 */
function showDetails(item) {
    const sidebar = document.getElementById('details-sidebar');
    if (!sidebar) return;

    activeInstrument = item;
    
    // check role to determine visbility
    const isStaff = localStorage.getItem('isStaff') === 'true'; 
    const isAvailable = (item.Status || '').trim().toUpperCase() === 'IN';

    // reset UI state
    if (typeof switchTab === 'function') switchTab('details');
    document.getElementById('details-content').style.display = 'block';
    document.getElementById('manage-content').style.display = 'none';

    // this controls the dynamic selecting of entries
    document.querySelectorAll('.instrument-card').forEach(c => c.classList.remove('selected-card'));
    const card = document.querySelector(`.instrument-card[data-id="${item.Name_ID}"]`);
    if (card) card.classList.add('selected-card');

    // this controls the badge showing the instrument status
    const badge = document.getElementById('detail-status-badge');
    if (badge) {
        badge.textContent = isAvailable ? 'IN' : 'OUT';
        badge.className = `status-indicator-pill ${isAvailable ? 'status-in' : 'status-out'}`;
    } // if

    // this is for image which is pretty bare rn
    const imgDiv = document.getElementById('detail-picture-container');
    const iconElement = document.getElementById('detail-icon');
    if (imgDiv && iconElement) {
        const hasPic = item.Picture && item.Picture !== "N/A" && item.Picture.trim() !== "";
        imgDiv.style.backgroundImage = hasPic ? `url('${item.Picture}')` : 'none';
        imgDiv.style.display = hasPic ? 'block' : 'none';
        iconElement.style.display = hasPic ? 'none' : 'block';
    } // if

    // get all the public fields
    document.getElementById('detail-name').textContent = item.Name_ID || '---';
    document.getElementById('detail-type').textContent = item.Type || '---';
    document.getElementById('detail-make').textContent = item.Make || '---';
    document.getElementById('detail-grade').textContent = item.Grade || '---';
    document.getElementById('detail-model').textContent = item.Model || '---';
    document.getElementById('detail-serial').textContent = item.Serial_Number || '---';
    document.getElementById('detail-price').textContent = item.Price ? `$${item.Price}` : '---';

    // get staff fields if present, then show them if so
    const staffContainer = document.getElementById('staff-only-info');
    const manageTabBtn = document.getElementById('tab-manage');
    const manageContent = document.getElementById('manage-content');

    if (isStaff) {
        // show staff UI
        if (staffContainer) staffContainer.style.display = 'block';
        if (manageTabBtn) manageTabBtn.style.display = 'inline-block';

        // set restricted fields
        document.getElementById('detail-stored').textContent = item.Stored_In || '---';
        document.getElementById('detail-dept').textContent = item.Dept || '---';
        document.getElementById('detail-oldid').textContent = item.Old_ID || '---';
        document.getElementById('detail-notes').textContent = item.Notes || 'N/A';

        // manage tab toggling appropriately
        const checkoutForm = document.getElementById('checkout-form');
        const checkinForm = document.getElementById('checkin-form');
        const loanInfo = document.getElementById('loan-info');

        if (isAvailable) {
            checkoutForm.style.display = 'block';
            checkinForm.style.display = 'none';
        } else {
            checkoutForm.style.display = 'none';
            checkinForm.style.display = 'block';
            document.getElementById('loan-info').innerText = `Instrument ${item.Name_ID} is currently out.`;
        } // elif
    } else {
        // if student, strip restricted data display
        if (staffContainer) staffContainer.style.display = 'none';
        if (manageTabBtn) manageTabBtn.style.display = 'none';
        if (manageContent) manageContent.style.display = 'none';
    } // elif

    // finally, display the correct view
    sidebar.classList.add('open');
} // showDetails

/**
 * ...
 */
function closeDetails() {
    const sidebar = document.getElementById('details-sidebar'); 
    if (sidebar) {
        sidebar.classList.remove('open');
    } // if
    document.querySelectorAll('.instrument-card').forEach(c => c.classList.remove('selected-card'));
} // closeDetails