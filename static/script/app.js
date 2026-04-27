document.addEventListener('alpine:init', () => {
    Alpine.data('inventory', () => ({
        instruments: [],
        searchQuery: '',
        isStaff: document.body.getAttribute('data-logged-in') === 'true',        

        isEditMode: false,
        isDeleteMode: false,
        showAddModal: false,
        showEditModal: false,
        
        selectedInstrument: null,
        editTarget: {},
        newInstrument: { 
            Name_ID: '', 
            Old_ID: '', 
            Type: '', 
            Grade: '', 
            Make: '', 
            Model: '', 
            Picture: '', 
            Serial_Number: '', 
            Price: 0.0, 
            Stored_In: 1, 
            Dept: 1 
        },

        currentTab: 'details',

        showAdvancedModal: false,

        filters: {
            Name_ID: '',
            Old_ID: '',
            Type: '',
            Grade: '',
            Make: '',
            Model: '',
            Serial_Number: '',
            Price: 9999, // max
            Stored_In: '',
            Dept: ''
        },

        checkoutEmail: '',
        instrumentHistory: [],

        // calculate the return date (arbitrarily set to 3 months for now)
        get threeMonthsFromToday() {
            const d = new Date();
            d.setMonth(d.getMonth() + 3);
            return d.toLocaleDateString();
        },

        async fetchHistory(instrumentId) {
            try {
                const res = await fetch(`/api/history/${instrumentId}`);
                this.instrumentHistory = await res.json();
            } catch (err) {
                console.error("Failed to load history:", err);
            }
        },

        async submitCheckout() {
            if (!this.checkoutEmail.endsWith('@grinnell.edu')) {
                alert("Please use a valid @grinnell.edu email.");
                return;
            }

            const dueDate = new Date();
            dueDate.setMonth(dueDate.getMonth() + 3);

            try {
                const res = await fetch('/api/checkout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: this.checkoutEmail,
                        Item_ID: this.selectedInstrument.Name_ID,
                        Due_Date: dueDate.toISOString().split('T')[0]
                    })
                });

                if (res.ok) {
                    alert("Checked out successfully!");
                    this.checkoutEmail = '';
                    await this.fetchInstruments(); // refresh status
                    this.selectedInstrument = this.instruments.find(i => i.ID === this.selectedInstrument.ID);
                    await this.fetchHistory(this.selectedInstrument.Name_ID);
                }
            } catch (err) {
                alert("Checkout failed.");
            }
        },

        async returnInstrument(instrumentId) {
            if (!confirm(`Are you sure you want to return ${instrumentId}?`)) return;

            try {
                const response = await fetch(`/api/return/${instrumentId}`, {
                    method: 'POST'
                });

                if (response.ok) {
                    await this.fetchInstruments();
                    this.selectedInstrument = null;
                    alert("Instrument returned successfully.");
                } else {
                    const error = await response.json();
                    alert("Error returning instrument: " + error.message);
                }
            } catch (err) {
                console.error("Return failed:", err);
            }
        },

        get filteredInstruments() {
            const q = this.searchQuery.toLowerCase().trim();
            
            return this.instruments.filter(i => {
                const matchesSearch = !q || (
                    i.Name_ID?.toString().toLowerCase().includes(q) ||
                    i.Type?.toLowerCase().includes(q) ||
                    i.Make?.toLowerCase().includes(q) ||
                    i.Model?.toLowerCase().includes(q)
                );

                const matchesType = !this.filters.Type || 
                    i.Type?.toLowerCase().includes(this.filters.Type.toLowerCase().trim());

                const matchesGrade = !this.filters.Grade || i.Grade === this.filters.Grade;
                const matchesMake = !this.filters.Make || i.Make?.toLowerCase().includes(this.filters.Make.toLowerCase());
                const matchesModel = !this.filters.Model || i.Model?.toLowerCase().includes(this.filters.Model.toLowerCase());
                const matchesSerial = !this.filters.Serial_Number || i.Serial_Number?.toString().includes(this.filters.Serial_Number);
                
                const maxPrice = parseFloat(this.filters.Price) || 9999;
                const matchesPrice = (parseFloat(i.Price) || 0) <= maxPrice;

                const matchesStored = !this.filters.Stored_In || i.Stored_In?.toString() === this.filters.Stored_In.toString();
                const matchesDept = !this.filters.Dept || i.Dept?.toString() === this.filters.Dept.toString();

                return matchesSearch && matchesType && matchesGrade && matchesMake && 
                    matchesModel && matchesSerial && matchesPrice && matchesStored && matchesDept;
            });
        },

        clearFilters() {
            this.filters = {
                Name_ID: '', Old_ID: '', Type: '', Grade: '', Make: '', 
                Model: '', Serial_Number: '', Price: 9999, Stored_In: '', Dept: ''
            };
            this.searchQuery = '';
        },

        async init() {
            await this.fetchInstruments();
        },

        // GET the data
        async fetchInstruments() {
            try {
                const res = await fetch('/api/instrument');
                this.instruments = await res.json();
            } catch (err) {
                console.error("Failed to load instruments:", err);
            }
        },

        // POST the data
        async addInstrument() {
            try {
                const res = await fetch('/api/instrument', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.newInstrument)
                });
                if (res.ok) {
                    await this.fetchInstruments();
                    this.showAddModal = false;
                    this.resetNewInstrumentForm();
                }
            } catch (err) {
                alert("Error adding instrument to database.");
            }
        },

        async updateInstrument() {
            try {
                const res = await fetch(`/api/instrument/${this.editTarget.ID}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.editTarget)
                });
                
                if (res.ok) {
                    await this.fetchInstruments(); // refresh
                    this.showEditModal = false;
                    this.isEditMode = false;
                } else {
                    const errorData = await res.json();
                    console.error("Server Error:", errorData.message);
                }
            } catch (err) {
                console.error("Network or Update failed:", err);
            }
        },

        async deleteInstrument(id) {
            if (!confirm("Are you sure you want to delete this?")) return;
            try {
                const res = await fetch(`/api/instrument/${id}`, { method: 'DELETE' });
                if (res.ok) {
                    await this.fetchInstruments(); // refresh
                }
            } catch (err) {
                alert("Delete failed.");
            }
        },

        // UI handling -------------------------------------------------------------------------------------
        handleCardClick(entry) {
            if (this.isDeleteMode) {
                this.deleteInstrument(entry.ID);
            } else if (this.isEditMode) {
                this.editTarget = { ...entry };
                this.showEditModal = true;
            } else {
                this.selectedInstrument = entry;
                this.currentTab = 'details';
            }
        },

        toggleEditMode() {
            this.isEditMode = !this.isEditMode;
            this.isDeleteMode = false;
            this.selectedInstrument = null;
        },

        toggleDeleteMode() {
            this.isDeleteMode = !this.isDeleteMode;
            this.isEditMode = false;
            this.selectedInstrument = null;
        },

        openAddModal() {
            this.showAddModal = true;
        },

        resetNewInstrumentForm() {
            this.newInstrument = { 
                Name_ID: '', 
                Old_ID: '', 
                Type: '', 
                Grade: '', 
                Make: '', 
                Model: '', 
                Picture: '', 
                Serial_Number: '', 
                Price: 0.0, 
                Stored_In: 1, 
                Dept: 1 
            };
        }
    }));
});