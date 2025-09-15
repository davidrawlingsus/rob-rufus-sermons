// Rob Rufus Sermon Directory - Frontend JavaScript

class SermonDirectory {
    constructor() {
        this.allSermons = [];
        this.filteredSermons = [];
        this.activeFilters = new Set();
        this.currentSort = 'newest';
        this.isLoading = false;
        
        this.init();
    }

    async init() {
        try {
            await this.loadStats();
            await this.loadSermons();
            this.initializeFilters();
            this.setupEventListeners();
        } catch (error) {
            console.error('Error initializing app:', error);
            this.showError('Failed to load sermon directory. Please refresh the page.');
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            if (stats.error) {
                throw new Error(stats.error);
            }
            
            this.updateHeaderStats(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async loadSermons() {
        this.setLoading(true);
        
        try {
            const params = new URLSearchParams({
                search: document.getElementById('searchInput').value,
                sort: this.currentSort,
                ...Object.fromEntries(this.activeFilters.entries())
            });
            
            const response = await fetch(`/api/sermons?${params}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            this.filteredSermons = data.sermons;
            this.renderSermons();
            this.updateStats(data.total);
            
        } catch (error) {
            console.error('Error loading sermons:', error);
            this.showError('Failed to load sermons. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    async loadThemes() {
        try {
            const response = await fetch('/api/themes');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            return data.themes;
        } catch (error) {
            console.error('Error loading themes:', error);
            return [];
        }
    }

    async initializeFilters() {
        const themes = await this.loadThemes();
        
        const filterChips = document.getElementById('filterChips');
        filterChips.innerHTML = '';

        // Add "All" filter
        const allChip = this.createFilterChip('All', this.filteredSermons.length, true);
        filterChips.appendChild(allChip);

        // Define mobile-first optimized theme order
        const mobileThemes = [
            'Grace & Gospel',
            'Anointing & Power', 
            'Holy Spirit',
            'Faith & Trust',
            'Worship & Praise',
            'Healing & Miracles',
            'Kingdom & Authority',
            'Freedom & Liberation'
        ];

        // Add mobile-optimized theme filters
        mobileThemes.forEach(themeName => {
            const theme = themes.find(t => t.name === themeName);
            if (theme) {
                const chip = this.createFilterChip(theme.name, theme.count);
                filterChips.appendChild(chip);
            }
        });

        // Add "More" button for additional themes
        const moreChip = document.createElement('div');
        moreChip.className = 'filter-chip more-themes-btn';
        moreChip.textContent = 'More...';
        moreChip.addEventListener('click', () => this.showMoreThemes(themes));
        filterChips.appendChild(moreChip);
    }

    showMoreThemes(themes) {
        const filterChips = document.getElementById('filterChips');
        const moreBtn = filterChips.querySelector('.more-themes-btn');
        
        if (moreBtn.textContent === 'More...') {
            // Show additional themes
            const additionalThemes = [
                'Spiritual Warfare', 'Fear & Courage', 'Word & Truth', 'Peace & Rest',
                'Prayer & Intercession', 'Identity & Sonship', 'Joy & Happiness',
                'Church & Ministry', 'Christmas & Easter', 'End Times & Prophecy',
                'Discipleship & Growth', 'Testimonies & Reports'
            ];

            additionalThemes.forEach(themeName => {
                const theme = themes.find(t => t.name === themeName);
                if (theme) {
                    const chip = this.createFilterChip(theme.name, theme.count);
                    filterChips.insertBefore(chip, moreBtn);
                }
            });
            moreBtn.textContent = 'Less...';
        } else {
            // Hide additional themes
            const additionalChips = filterChips.querySelectorAll('.filter-chip:not([data-theme="All"]):not(.more-themes-btn)');
            const mobileThemes = [
                'Grace & Gospel', 'Anointing & Power', 'Holy Spirit', 'Faith & Trust',
                'Worship & Praise', 'Healing & Miracles', 'Kingdom & Authority', 'Freedom & Liberation'
            ];
            
            additionalChips.forEach(chip => {
                if (!mobileThemes.includes(chip.dataset.theme)) {
                    chip.remove();
                }
            });
            moreBtn.textContent = 'More...';
        }
    }

    createFilterChip(theme, count, isActive = false) {
        const chip = document.createElement('div');
        chip.className = `filter-chip ${isActive ? 'active' : ''}`;
        chip.textContent = `${theme} (${count})`;
        chip.dataset.theme = theme;
        
        chip.addEventListener('click', () => this.toggleFilter(theme));
        
        return chip;
    }

    toggleFilter(theme) {
        if (theme === 'All') {
            this.activeFilters.clear();
            document.querySelectorAll('.filter-chip').forEach(chip => {
                chip.classList.remove('active');
            });
            document.querySelector('[data-theme="All"]').classList.add('active');
        } else {
            if (this.activeFilters.has(theme)) {
                this.activeFilters.delete(theme);
            } else {
                this.activeFilters.add(theme);
            }
            
            // Update chip states
            document.querySelectorAll('.filter-chip').forEach(chip => {
                chip.classList.remove('active');
            });
            
            if (this.activeFilters.size === 0) {
                document.querySelector('[data-theme="All"]').classList.add('active');
            } else {
                this.activeFilters.forEach(filter => {
                    const chip = document.querySelector(`[data-theme="${filter}"]`);
                    if (chip) chip.classList.add('active');
                });
            }
        }
        
        this.loadSermons();
    }

    renderSermons() {
        const sermonList = document.getElementById('sermonList');
        
        if (this.filteredSermons.length === 0) {
            sermonList.innerHTML = `
                <div class="empty-state">
                    <h3>No sermons found</h3>
                    <p>Try adjusting your search or filters</p>
                </div>
            `;
            return;
        }
        
        sermonList.innerHTML = this.filteredSermons.map(sermon => `
            <div class="sermon-item">
                <h3 class="sermon-title">${this.escapeHtml(sermon.title)}</h3>
                <div class="sermon-meta">
                    <span class="sermon-date">${this.formatDate(sermon.date)}</span>
                    <span class="sermon-year">${sermon.year}</span>
                </div>
                <div class="sermon-themes">
                    ${sermon.themes.map(theme => `<span class="theme-tag">${this.escapeHtml(theme)}</span>`).join('')}
                </div>
                <div class="sermon-actions">
                    <a href="${this.escapeHtml(sermon.url)}" class="btn btn-primary" download>
                        <span>📥</span> Download
                    </a>
                    <button class="btn btn-secondary" onclick="sermonDirectory.playSermon('${this.escapeHtml(sermon.url)}')">
                        <span>▶️</span> Play
                    </button>
                </div>
            </div>
        `).join('');
    }

    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    updateHeaderStats(stats) {
        const headerStats = document.getElementById('headerStats');
        headerStats.textContent = `${stats.total_sermons} sermons from ${stats.date_range.earliest} to ${stats.date_range.latest} • Optimized thematic filters`;
    }

    updateStats(total) {
        const statsDisplay = document.getElementById('statsDisplay');
        const showing = this.filteredSermons.length;
        
        if (showing === total) {
            statsDisplay.textContent = `${total} sermons`;
        } else {
            statsDisplay.textContent = `Showing ${showing} of ${total} sermons`;
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        const sermonList = document.getElementById('sermonList');
        
        if (loading) {
            sermonList.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading sermons...</p>
                </div>
            `;
        }
    }

    showError(message) {
        const sermonList = document.getElementById('sermonList');
        sermonList.innerHTML = `
            <div class="error">
                <h3>Error</h3>
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
    }

    playSermon(url) {
        // This would integrate with an audio player
        alert(`Playing: ${url}`);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        let searchTimeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.loadSermons();
            }, 300);
        });

        // Sort select
        document.getElementById('sortSelect').addEventListener('change', (e) => {
            this.currentSort = e.target.value;
            this.loadSermons();
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.sermonDirectory = new SermonDirectory();
});
