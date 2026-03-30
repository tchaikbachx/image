/*  +-------------+ 
    |  FETCHING   |
    +----- -------+*/

let isDeleteMode = false;
let isEditMode = false;
let currentEditId = null;


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
 * @returns 
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
            card.className = 'instrument-card card';
            
            // gatekeeper
            card.onclick = (e) => onCardClick(item.ID, e, item);

            card.innerHTML = `
                <h3>${item.Name_ID}</h3>
                <p>${item.Type} - ${item.Make}</p>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        console.error(err);
    } // try/catch
} // loadInstruments


/**
 * close modal if user clicks outside (e.g., background)
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
 * controls the edit flag behavior.
 */
function toggleEditMode() {
    isEditMode = !isEditMode;
    isDeleteMode = false; // only one mode can exist at a time
    
    const grid = document.getElementById('instrument-grid');
    grid.classList.remove('delete-mode');
    grid.classList.toggle('edit-mode', isEditMode);
    
    document.getElementById('edit-mode-btn').classList.toggle('active-mode', isEditMode);
    document.getElementById('delete-mode-btn').classList.remove('active-mode');
} // toggleEditMode

/**
 * controls the action of opening the modal & filling out any fields the
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
 * 
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
 */
function toggleDeleteMode() {
    isDeleteMode = !isDeleteMode;
    const grid = document.getElementById('instrument-grid');
    const btn = document.getElementById('delete-mode-btn');
    
    grid.classList.toggle('delete-mode', isDeleteMode);
    btn.classList.toggle('active-mode', isDeleteMode);
} // toggleDeleteMode

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
        showDetails(item.Name_ID, item.Model, 'In Stock', item.Notes || 'No notes');
    } // elif
} // onCardClick

/**
 * ...
 * @param {*} id 
 * @param {*} event 
 * @returns 
 */
async function deleteInstrument(id, event) {
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
 * general modal UI controls
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
    saveBtn.textContent = "Save to Database";
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
    // match the 12 fields in database
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
