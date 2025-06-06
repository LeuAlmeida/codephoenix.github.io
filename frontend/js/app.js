// CodePhoenix Frontend - JavaScript Logic

let isScanning = false;

// DOM Elements
const scanForm = document.getElementById('scanForm');
const resultsSection = document.getElementById('resultsSection');
const statusPanel = document.getElementById('statusPanel');
const resultsDisplay = document.getElementById('resultsDisplay');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const currentStatus = document.getElementById('currentStatus');
const scanButton = document.getElementById('scanButton');
const stopButton = document.getElementById('stopButton');

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadSavedConfig();
    setupFormValidation();
});

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const eyeIcon = document.getElementById(inputId + '-eye');
    
    if (input.type === 'password') {
        input.type = 'text';
        eyeIcon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        eyeIcon.className = 'fas fa-eye';
    }
}

// Toggle advanced options
function toggleAdvanced() {
    const advancedOptions = document.getElementById('advancedOptions');
    const chevron = document.getElementById('advanced-chevron');
    const text = document.getElementById('advanced-text');
    
    if (advancedOptions.classList.contains('hidden')) {
        advancedOptions.classList.remove('hidden');
        chevron.className = 'fas fa-chevron-up';
        text.textContent = 'Ocultar';
    } else {
        advancedOptions.classList.add('hidden');
        chevron.className = 'fas fa-chevron-down';
        text.textContent = 'Mostrar';
    }
}

// Load saved configuration from localStorage
function loadSavedConfig() {
    const saved = localStorage.getItem('CodePhoenix-config');
    if (saved) {
        try {
            const config = JSON.parse(saved);
            
            // Don't restore the token for security
            if (config.searchTerms) document.getElementById('searchTerms').value = config.searchTerms;
            if (config.resultsPerPage) document.getElementById('resultsPerPage').value = config.resultsPerPage;
            if (config.pages) document.getElementById('pages').value = config.pages;
            if (config.sleepTime) document.getElementById('sleepTime').value = config.sleepTime;
            if (config.startDate) document.getElementById('startDate').value = config.startDate;
            if (config.endDate) document.getElementById('endDate').value = config.endDate;
        } catch (e) {
            console.log('Error loading saved config:', e);
        }
    }
}

// Save configuration to localStorage
function saveConfig() {
    const config = {
        searchTerms: document.getElementById('searchTerms').value,
        resultsPerPage: document.getElementById('resultsPerPage').value,
        pages: document.getElementById('pages').value,
        sleepTime: document.getElementById('sleepTime').value,
        startDate: document.getElementById('startDate').value,
        endDate: document.getElementById('endDate').value
    };
    
    localStorage.setItem('CodePhoenix-config', JSON.stringify(config));
}

// Form validation setup
function setupFormValidation() {
    const githubToken = document.getElementById('githubToken');
    const searchTerms = document.getElementById('searchTerms');
    
    // GitHub token validation
    githubToken.addEventListener('input', function() {
        const value = this.value.trim();
        const isValid = value.length === 0 || (
            value.startsWith('ghp_') && value.length >= 40
        ) || (
            value.startsWith('github_pat_') && value.length >= 50
        );
        
        if (value.length > 0 && !isValid) {
            this.classList.add('ring-red-500', 'border-red-500');
            this.classList.remove('ring-git-accent');
        } else {
            this.classList.remove('ring-red-500', 'border-red-500');
        }
    });
    
    // Search terms validation
    searchTerms.addEventListener('input', function() {
        const value = this.value.trim();
        if (value.length > 0) {
            const terms = value.split(',').map(t => t.trim()).filter(t => t.length > 0);
            showDetectedTypes(terms);
        }
    });
}

// Show detected data types for search terms
function showDetectedTypes(terms) {
    terms.forEach(term => {
        const type = getDataType(term);
        // Could show a preview of detected types here
    });
}

// Handle form submission
scanForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (isScanning) {
        return;
    }
    
    // Validate form
    const githubToken = document.getElementById('githubToken').value.trim();
    const searchTerms = document.getElementById('searchTerms').value.trim();
    
    if (!githubToken || !searchTerms) {
        showNotification('Please fill in all required fields.', 'error');
        return;
    }
    
    // Save configuration
    saveConfig();
    
    // Start scanning
    await startScan();
});

// Start scanning process
async function startScan() {
    isScanning = true;
    
    // Update UI
    scanButton.disabled = true;
    scanButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Preparing...';
    stopButton.classList.remove('hidden');
    resultsSection.classList.remove('hidden');
    resultsDisplay.innerHTML = '';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    try {
        // Prepare scan configuration
        const config = {
            githubToken: document.getElementById('githubToken').value.trim(),
            searchTerms: document.getElementById('searchTerms').value.trim(),
            resultsPerPage: parseInt(document.getElementById('resultsPerPage').value),
            pages: parseInt(document.getElementById('pages').value),
            sleepTime: parseInt(document.getElementById('sleepTime').value),
            startDate: document.getElementById('startDate').value || null,
            endDate: document.getElementById('endDate').value || null
        };
        
        // Run the Python scanner
        await runRealPythonScanner(config);
        
    } catch (error) {
        console.error('Scan error:', error);
        showNotification('Error during scan: ' + error.message, 'error');
    } finally {
        stopScan();
    }
}

// Stop scanning process
function stopScan() {
    isScanning = false;
    
    // Update UI
    scanButton.disabled = false;
    scanButton.innerHTML = '<i class="fas fa-search"></i><span>Start Scan</span>';
    stopButton.classList.add('hidden');
}

// Update scanning status
function updateStatus(message, progress) {
    currentStatus.textContent = message;
    progressText.textContent = Math.round(progress) + '%';
    progressFill.style.width = progress + '%';
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const bgClass = type === 'success' ? 'bg-git-success' : 
                   type === 'error' ? 'bg-git-accent' : 'bg-blue-500';
    
    notification.className = `fixed top-4 right-4 ${bgClass} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation' : 'info'}-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Slide in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Slide out and remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Get data type for a term
function getDataType(term) {
    if (term.includes('@') && term.includes('.')) return 'EMAIL';
    if (term.startsWith('ghp_') || term.startsWith('gho_')) return 'GITHUB_TOKEN';
    if (term.startsWith('sk-') || term.startsWith('pk_')) return 'API_KEY';
    if (term.startsWith('AKIA')) return 'AWS_KEY';
    if (term.startsWith('http')) return 'URL';
    if (term.includes('://')) return 'DATABASE_URL';
    return 'GENERIC';
}

