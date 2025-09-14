// Internship Locator - Frontend JavaScript

class InternshipLocator {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5001/api';
        this.currentResults = [];
        this.currentFilters = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkApiHealth();
    }

    bindEvents() {
        // Search form submission
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.performSearch();
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                console.log('✅ API is healthy');
                this.showNotification('API connected successfully', 'success');
            } else {
                console.warn('⚠️ API health check failed');
                this.showNotification('API connection issue', 'warning');
            }
        } catch (error) {
            console.error('❌ API health check error:', error);
            this.showNotification('Cannot connect to API. Please ensure the backend is running.', 'error');
        }
    }

    async performSearch() {
        const formData = this.getFormData();
        
        if (!formData.keyword || !formData.location) {
            this.showNotification('Please fill in both job type and location fields.', 'error');
            return;
        }

        this.showLoading();
        this.hideResults();

        try {
            const response = await fetch(`${this.apiBaseUrl}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                this.currentResults = data.jobs;
                this.currentFilters = formData;
                this.displayResults(data);
            } else {
                throw new Error(data.error || 'Search failed');
            }

        } catch (error) {
            console.error('Search error:', error);
            this.showNotification('Search failed. Please try again.', 'error');
            this.hideLoading();
        }
    }

    getFormData() {
        return {
            keyword: document.getElementById('keyword').value.trim(),
            location: document.getElementById('location').value.trim(),
            remote_only: document.getElementById('remoteOnly').value === 'true',
            paid_only: document.getElementById('paidOnly').value === 'true',
            platforms: this.getSelectedPlatforms()
        };
    }

    getSelectedPlatforms() {
        const platformValue = document.getElementById('platforms').value;
        if (platformValue === 'all') {
            return ['linkedin', 'indeed', 'glassdoor', 'handshake'];
        }
        return [platformValue];
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('search').scrollIntoView({ behavior: 'smooth' });
        
        // Simulate progress
        this.simulateSearchProgress();
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    simulateSearchProgress() {
        const progressBar = document.querySelector('.progress-bar');
        const statusElement = document.getElementById('searchStatus');
        const platforms = ['LinkedIn', 'Indeed', 'Glassdoor', 'Handshake'];
        let currentPlatform = 0;

        const interval = setInterval(() => {
            const progress = ((currentPlatform + 1) / platforms.length) * 100;
            progressBar.style.width = `${progress}%`;
            
            if (currentPlatform < platforms.length) {
                statusElement.textContent = `Searching ${platforms[currentPlatform]}...`;
                currentPlatform++;
            } else {
                clearInterval(interval);
                statusElement.textContent = 'Processing results...';
            }
        }, 1000);
    }

    displayResults(data) {
        this.hideLoading();
        
        const resultsSection = document.getElementById('results');
        const resultsTitle = document.getElementById('resultsTitle');
        const resultsSubtitle = document.getElementById('resultsSubtitle');
        const resultCount = document.getElementById('resultCount');
        const resultsGrid = document.getElementById('resultsGrid');
        const noResults = document.getElementById('noResults');

        // Update header
        resultsTitle.innerHTML = `<i class="fas fa-list"></i> Search Results`;
        resultsSubtitle.textContent = `Found ${data.total_count} internships for "${data.search_params.keyword}" in "${data.search_params.location}"`;
        resultCount.textContent = `${data.total_count} results found`;

        if (data.total_count === 0) {
            resultsGrid.innerHTML = '';
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
            resultsGrid.innerHTML = this.generateResultsHTML(data.jobs);
        }

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    generateResultsHTML(jobs) {
        return jobs.map(job => `
            <div class="col-lg-6 col-xl-4">
                <div class="job-card fade-in">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="card-title">${this.escapeHtml(job.title)}</h5>
                        <span class="platform-badge ${job.platform.toLowerCase()}">${job.platform}</span>
                    </div>
                    
                    <div class="company mb-2">
                        <i class="fas fa-building"></i> ${this.escapeHtml(job.company)}
                    </div>
                    
                    <div class="location mb-2">
                        <i class="fas fa-map-marker-alt"></i> ${this.escapeHtml(job.location)}
                    </div>
                    
                    <div class="salary mb-3">
                        <i class="fas fa-dollar-sign"></i> ${this.escapeHtml(job.salary)}
                    </div>
                    
                    <div class="description mb-3">
                        ${this.escapeHtml(job.description)}
                    </div>
                    
                    <div class="d-flex gap-2">
                        <a href="${job.apply_url}" target="_blank" class="btn btn-primary apply-btn">
                            <i class="fas fa-external-link-alt"></i> Apply Now
                        </a>
                        <button class="btn btn-outline-secondary" onclick="window.open('${job.apply_url}', '_blank')">
                            <i class="fas fa-external-link-alt"></i>
                        </button>
                    </div>
                    
                    <div class="mt-2">
                        <small class="text-muted">
                            <i class="fas fa-clock"></i> Scraped ${this.formatTime(job.scraped_at)}
                        </small>
                    </div>
                </div>
            </div>
        `).join('');
    }

    filterResults(filterType) {
        let filteredResults = [...this.currentResults];

        switch (filterType) {
            case 'remote':
                filteredResults = filteredResults.filter(job => job.remote);
                break;
            case 'paid':
                filteredResults = filteredResults.filter(job => job.paid);
                break;
            case 'all':
            default:
                // Show all results
                break;
        }

        this.displayFilteredResults(filteredResults, filterType);
    }

    displayFilteredResults(results, filterType) {
        const resultsGrid = document.getElementById('resultsGrid');
        const resultCount = document.getElementById('resultCount');
        const noResults = document.getElementById('noResults');

        resultCount.textContent = `${results.length} results found`;

        if (results.length === 0) {
            resultsGrid.innerHTML = '';
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
            resultsGrid.innerHTML = this.generateResultsHTML(results);
        }
    }

    hideResults() {
        document.getElementById('results').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatTime(timestamp) {
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMs / 3600000);

            if (diffMins < 1) return 'just now';
            if (diffMins < 60) return `${diffMins} minutes ago`;
            if (diffHours < 24) return `${diffHours} hours ago`;
            return date.toLocaleDateString();
        } catch (error) {
            return 'recently';
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.internshipLocator = new InternshipLocator();
});

// Global function for filtering (accessible from HTML)
function filterResults(filterType) {
    if (window.internshipLocator) {
        window.internshipLocator.filterResults(filterType);
    }
} 