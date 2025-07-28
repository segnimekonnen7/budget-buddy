// ML Internship Finder - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data if on jobs page
    if (window.location.pathname === '/jobs') {
        loadJobs();
    }
}

function setupEventListeners() {
    // Search form submission
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }
    
    // Application tracking
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('apply-btn')) {
            handleApply(e);
        }
        
        if (e.target.classList.contains('view-details-btn')) {
            handleViewDetails(e);
        }
    });
}

async function handleSearch(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const keywords = document.getElementById('keywords').value;
    const location = document.getElementById('location').value;
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords: keywords,
                location: location,
                limit: 50
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.jobs);
        } else {
            showError('Search failed: ' + data.error);
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayResults(jobs) {
    const resultsSection = document.getElementById('results-section');
    const container = document.getElementById('results-container');
    
    if (!resultsSection || !container) return;
    
    // Show results section
    resultsSection.style.display = 'block';
    
    if (jobs.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h4>No jobs found</h4>
                <p class="text-muted">Try adjusting your search criteria</p>
            </div>
        `;
        return;
    }
    
    // Generate job cards
    const jobCards = jobs.map((job, index) => createJobCard(job, index)).join('');
    
    container.innerHTML = `
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h4>Found ${jobs.length} matching internships</h4>
                    <button class="btn btn-outline-primary" onclick="exportJobs()">
                        <i class="fas fa-download"></i> Export to CSV
                    </button>
                </div>
                ${jobCards}
            </div>
        </div>
    `;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function createJobCard(job, index) {
    const skills = job.skills_required || [];
    const skillTags = skills.map(skill => 
        `<span class="skill-tag">${skill}</span>`
    ).join('');
    
    const matchScore = job.match_score || 0;
    const matchColor = matchScore > 70 ? '#28a745' : matchScore > 50 ? '#ffc107' : '#dc3545';
    
    return `
        <div class="job-card hover-lift">
            <div class="job-header">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h5 class="job-title">${job.title}</h5>
                        <p class="job-company mb-1">${job.company}</p>
                        <p class="job-location mb-2">
                            <i class="fas fa-map-marker-alt"></i> ${job.location}
                        </p>
                        <span class="job-salary">${job.salary}</span>
                    </div>
                    <div class="text-end">
                        <div class="match-score" style="background-color: ${matchColor}">
                            ${matchScore.toFixed(0)}% Match
                        </div>
                    </div>
                </div>
            </div>
            <div class="job-body">
                <p class="text-muted mb-3">${job.description}</p>
                <div class="job-skills">
                    <strong>Required Skills:</strong><br>
                    ${skillTags}
                </div>
                <div class="d-flex justify-content-between align-items-center mt-3">
                    <small class="text-muted">
                        <i class="fas fa-calendar"></i> Posted: ${job.posted_date}
                    </small>
                    <div>
                        <button class="btn btn-outline-primary btn-sm me-2 view-details-btn" 
                                data-job-id="${index}">
                            <i class="fas fa-eye"></i> View Details
                        </button>
                        <button class="btn btn-primary btn-sm apply-btn" 
                                data-job-id="${index}">
                            <i class="fas fa-paper-plane"></i> Apply
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function handleApply(e) {
    const jobId = e.target.dataset.jobId;
    const jobs = await getJobs();
    
    if (jobs && jobs[jobId]) {
        const job = jobs[jobId];
        
        // Show application modal
        showApplicationModal(job, jobId);
    }
}

function showApplicationModal(job, jobId) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'applicationModal';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Apply to ${job.title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="applicationForm">
                        <div class="mb-3">
                            <label class="form-label">Application Status</label>
                            <select class="form-select" name="status" required>
                                <option value="applied">Applied</option>
                                <option value="interview">Interview Scheduled</option>
                                <option value="offer">Offer Received</option>
                                <option value="rejected">Rejected</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Notes</label>
                            <textarea class="form-control" name="notes" rows="3" 
                                      placeholder="Add any notes about this application..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="submitApplication(${jobId})">
                        Track Application
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    // Clean up modal when hidden
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

async function submitApplication(jobId) {
    const form = document.getElementById('applicationForm');
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`/apply/${jobId}`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            bootstrap.Modal.getInstance(document.getElementById('applicationModal')).hide();
        } else {
            showError('Failed to track application: ' + data.error);
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function handleViewDetails(e) {
    const jobId = e.target.dataset.jobId;
    window.location.href = `/job/${jobId}`;
}

async function loadJobs() {
    try {
        const response = await fetch('/api/jobs');
        const jobs = await response.json();
        
        if (jobs.length > 0) {
            displayResults(jobs);
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

async function getJobs() {
    try {
        const response = await fetch('/api/jobs');
        return await response.json();
    } catch (error) {
        console.error('Error fetching jobs:', error);
        return null;
    }
}

async function exportJobs() {
    try {
        const response = await fetch('/export');
        const data = await response.json();
        
        if (data.success) {
            showSuccess('Jobs exported successfully!');
        } else {
            showError('Export failed: ' + data.error);
        }
    } catch (error) {
        showError('Export error: ' + error.message);
    }
}

function showLoading() {
    const button = document.querySelector('#searchForm button[type="submit"]');
    if (button) {
        button.innerHTML = '<span class="loading"></span> Searching...';
        button.disabled = true;
    }
}

function hideLoading() {
    const button = document.querySelector('#searchForm button[type="submit"]');
    if (button) {
        button.innerHTML = '<i class="fas fa-search"></i> Search Internships';
        button.disabled = false;
    }
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'danger');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatSalary(salary) {
    if (!salary) return 'Not specified';
    return salary;
}

// Profile management
function updateProfile(profileData) {
    fetch('/profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Profile updated successfully!');
        } else {
            showError('Profile update failed: ' + data.error);
        }
    })
    .catch(error => {
        showError('Network error: ' + error.message);
    });
}

// Skills management
function addSkill(skill) {
    const skillsContainer = document.getElementById('skills-container');
    if (skillsContainer) {
        const skillElement = document.createElement('span');
        skillElement.className = 'skill-input';
        skillElement.innerHTML = `
            ${skill}
            <button type="button" class="btn-close btn-close-white ms-2" 
                    onclick="removeSkill(this)"></button>
        `;
        skillsContainer.appendChild(skillElement);
    }
}

function removeSkill(button) {
    button.parentElement.remove();
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}); 