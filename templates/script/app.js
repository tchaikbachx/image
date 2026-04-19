document.addEventListener('alpine:init', () => {
    Alpine.data('inventory', () => ({
        instruments: [],
        searchQuery: '',
        isStaff: localStorage.getItem('isStaff') === 'true',
        
        advType: '',
        advMake: '',
        advGrade: '',
        advLocation: '',
        advPrice: 9999,
        showAdvancedModal: false,

        isDeleteMode: false,
        isEditMode: false,

        async init() {
            await this.fetchInstruments();
        },

        async fetchInstruments() {
            try {
                const res = await fetch('http://127.0.0.1:5000/api/instrument');
                this.instruments = await res.json();
            } catch (err) {
                console.error("Failed to load inventory:", err);
            }
        },

        get filteredInstruments() {
            return this.instruments.filter(i => {
                const matchesSearch = !this.searchQuery || 
                    i.Name_ID.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    i.Type.toLowerCase().includes(this.searchQuery.toLowerCase());

                const matchesAdvType = !this.advType || i.Type.toLowerCase().includes(this.advType.toLowerCase());
                const matchesMake = !this.advMake || i.Make.toLowerCase().includes(this.advMake.toLowerCase());
                const matchesGrade = !this.advGrade || i.Grade.toLowerCase().includes(this.advGrade.toLowerCase());
                const matchesLoc = !this.advLocation || i.Location.toLowerCase().includes(this.advLocation.toLowerCase());
                const matchesPrice = (i.Price || 0) <= this.advPrice;

                return matchesSearch && matchesAdvType && matchesMake && matchesGrade && matchesLoc && matchesPrice;
            });
        },

        async deleteInstrument(id) {
            if (!confirm("Are you sure? This cannot be undone.")) return;
            try {
                const res = await fetch(`http://127.0.0.1:5000/api/instrument/${id}`, { method: 'DELETE' });
                if (res.ok) {
                    this.instruments = this.instruments.filter(i => i.ID !== id);
                }
            } catch (err) {
                alert("Delete failed.");
            }
        },

        resetFilters() {
            this.searchQuery = '';
            this.advType = '';
            this.advMake = '';
            this.advGrade = '';
            this.advLocation = '';
            this.advPrice = 9999;
        }
    }));
});