document.addEventListener('alpine:init', () => {
    Alpine.data('inventory', () => ({
        // --- NAVIGATION & STATE ---
        activeTable: 'instrument', 
        entries: [],
        isStaff: document.body.getAttribute('data-logged-in') === 'true',
        currentTab: 'details',
        activeLoans: [],

        // --- UI MODALS ---
        showAddModal: false,
        showEditModal: false,
        showEmailModal: false,
        emailSubject: '',
        emailBody: '',
        showAdvancedModal: false,
        isEditMode: false,
        isDeleteMode: false,
        
        // --- SELECTION & CRUD ---
        selectedEntry: null,
        searchQuery: '',
        editTarget: {},
        newEntry: {}, 
        filters: {
            Type: '',
            Grade: '',
            Make: '',
            Model: '',
            Serial_Number: '',
            Price: 9999,
            Stored_In: '',
            Dept: '',
            Status: ''
        },

        // --- FETCHING & TABS ---
        async init() {
            // ensures data loads immediately for the default table
            this.switchTable('instrument'); 
            
            // check if staff from the data-attribute set in your HTML
            this.isStaff = document.body.getAttribute('data-logged-in') === 'true';
        },

        switchTable(tableName) {
            this.activeTable = tableName;
            this.searchQuery = '';
            this.clearFilters(); 
            this.isEditMode = false;   // reset modes on tab switch
            this.isDeleteMode = false; // reset modes on tab switch
            this.selectedEntry = null;
            this.fetchEntries();
        },

        get filteredEntries() {
            return this.entries.filter(entry => {
                // search bar
                const matchesSearch = !this.searchQuery || 
                Object.values(entry).some(val => 
                    String(val || '').toLowerCase().includes(this.searchQuery.toLowerCase())
                );

                // adv filter
                const matchesAdvanced = Object.keys(this.filters).every(key => {
                const filterValue = String(this.filters[key] || '').toLowerCase();
                const entryValue = String(entry[key] || '').toLowerCase();

                if (!filterValue || filterValue === '') return true;

                // price
                if (key === 'Price') return Number(entry[key] || 0) <= Number(this.filters[key]);

                // status
                if (key === 'Status') return String(entry.Availability || '').toLowerCase() === filterValue;

                // partial matching search
                return entryValue.includes(filterValue);
                });

                return matchesSearch && matchesAdvanced;
            });
            },


        clearFilters() {
            this.filters = {
                // shared/instruments
                Type: '',
                Grade: '',
                Make: '',
                Model: '',
                Serial_Number: '',
                Price: 9999,
                Stored_In: '',
                Dept: '',
                Status: '',
                // Keys
                Description: '',
                Qty: '',
                // Lockers
                Kkey: '',
                Name_ID: ''
            };
        },

        async fetchEntries() {
            try {
                const res = await fetch(`/api/${this.activeTable}`);
                const data = await res.json();
                this.entries = Array.isArray(data) ? data : []; 
            } catch (err) {
                this.entries = [];
            }
        },

        // --- GENERALIZED CRUD (using integer ID) ---
        async addEntry() {
            try {
                const res = await fetch(`/api/${this.activeTable}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.newEntry)
                });
                if (res.ok) {
                    await this.fetchEntries();
                    this.showAddModal = false;
                    this.newEntry = {};
                }
            } catch (err) { console.error("Add failed"); }
        },

        async updateEntry() {
            try {
                // use integer ID for URL
                const res = await fetch(`/api/${this.activeTable}/${this.editTarget.ID}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.editTarget)
                });
                if (res.ok) {
                    await this.fetchEntries();
                    this.showEditModal = false;
                    this.isEditMode = false;
                }
            } catch (err) { console.error("Update failed"); }
        },

        async deleteEntry(id) {
            if (!confirm("Are you sure?")) return;
            try {
                // 'id' here is integer ID
                const res = await fetch(`/api/${this.activeTable}/${id}`, { method: 'DELETE' });
                if (res.ok) await this.fetchEntries();
            } catch (err) { console.error("Delete failed"); }
        },

        toggleEditMode() {
            this.isEditMode = !this.isEditMode;
            if (this.isEditMode) {
                // reset all other modes/modals
                this.isDeleteMode = false;
                this.showAddModal = false;
                this.selectedEntry = null; 
            }
        },

        toggleDeleteMode() {
            this.isDeleteMode = !this.isDeleteMode;
            if (this.isDeleteMode) {
                // reset all other modes/modals
                this.isEditMode = false;
                this.showAddModal = false;
                this.selectedEntry = null;
            }
        },

        // --- UI HANDLER ---
        async handleCardClick(entry) {
            if (this.isDeleteMode) {
                this.deleteEntry(entry.ID);
            } else if (this.isEditMode) {
                this.editTarget = { ...entry };
                this.showEditModal = true;
            } else {
                this.selectedEntry = entry;
                this.activeLoans = []; // reset
                
                // fetch borrowers for this specific Item_ID
                try {
                    const res = await fetch(`/api/checkouts/${entry.ID}`);
                    this.activeLoans = await res.json();
                } catch (err) { console.error("Loan fetch failed"); }

                if (this.activeTable === 'instrument') {
                    this.fetchHistory(entry.Name_ID);
                }
            }
        },

        async fetchHistory(nameID) {
            try {
                // prevents the crash
                const res = await fetch(`/api/history/${nameID}`);
                this.history = res.ok ? await res.json() : [];
            } catch (err) {
                console.error("History fetch failed:", err);
                this.history = [];
            }
        },

        async returnEntry(loanID) {
            if(!confirm("Confirm return for this borrower?")) return;
            try {
                const res = await fetch(`/api/return/${loanID}`, { method: 'POST' });
                if (res.ok) {
                    // remove from sidebar list and refresh grid counts
                    this.activeLoans = this.activeLoans.filter(l => l.ID !== loanID);
                    this.fetchEntries(); 
                }
            } catch (err) { console.error("Return failed"); }
        }
    }));
});