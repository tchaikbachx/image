document.addEventListener('alpine:init', () => {
    Alpine.data('inventory', () => ({
        // --- NAVIGATION & STATE ---
        activeTable: 'instrument', 
        entries: [],
        checkoutEmail: '',
        isStaff: document.body.getAttribute('data-logged-in') === 'true',
        currentTab: 'details',
        activeLoans: [],
        history: [],

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
            this.selectedEntry = entry;
            this.currentTab = 'details';
            
            // only fetch sensitive tabs if user is staff
            if (this.isStaff) {
                if (this.isDeleteMode) {
                    this.deleteEntry(entry.ID);
                } else if (this.isEditMode) {
                    this.editTarget = { ...entry };
                    this.showEditModal = true;
                } else {
                    this.selectedEntry = entry;
                    this.currentTab = 'details';
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
            } else {
                // clear sensitive data so it doesn't leak from a previous staff session
                this.activeLoans = [];
                this.history = [];
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


        submitCheckout(id, type) {
            if (!this.checkoutEmail) {
                alert("Please enter a borrower email.");
                return;
            }

            const payload = {
                item_id: id,
                item_type: type,
                email: this.checkoutEmail,
                due_date: this.threeMonthsFromToday
            };

            fetch('/api/checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(async (data) => {
                if (data.status === 'success') {
                    // refresh the main grid to update the status (AVAILABLE -> OUT)
                    await this.fetchEntries(); 
                    
                    // refresh the sidebar w/ existing /api/checkouts/ endpoint
                    const res = await fetch(`/api/checkouts/${id}`);
                    this.activeLoans = await res.json();
                    
                    // cleanup
                    this.checkoutEmail = ''; 
                    alert("Checkout recorded successfully!");
                }
            })
            .catch(err => console.error("Checkout failed:", err));
        },


        async returnEntry(loanID) {
            if(!confirm("Confirm return for this borrower?")) return;
            try {
                const res = await fetch(`/api/return/${loanID}`, { method: 'POST' });
                if (res.ok) {
                    // refresh the main grid so BOTH items turn AVAILABLE
                    await this.fetchEntries(); 
                    
                    // re-fetch the whole loan list for the selected item
                    const loanRes = await fetch(`/api/checkouts/${this.selectedEntry.ID}`);
                    this.activeLoans = await loanRes.json();
                    
                    alert("Return processed successfully.");
                }
            } catch (err) { console.error("Return failed:", err); }
        },

        get threeMonthsFromToday() {
            const d = new Date();
            d.setMonth(d.getMonth() + 3);
            return d.toISOString().split('T')[0];
        }
    }));
});