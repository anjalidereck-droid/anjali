/*
Clinical Trial Protocol Analyzer - Frontend JavaScript

This script handles all client-side interactions including file upload,
API communication, and dynamic UI updates.
*/

// API Base URL
const API_URL = 'http://localhost:8000';

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadNewBtn = document.getElementById('uploadNewBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
const searchBtn = document.getElementById('searchBtn');
const searchInput = document.getElementById('searchInput');
const summaryGrid = document.getElementById('summaryGrid');
const issuesList = document.getElementById('issuesList');
const searchResults = document.getElementById('searchResults');

let currentAnalysis = null;

/*
Event Listeners
*/

uploadBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', handleFileSelect);

uploadBox.addEventListener('dragover', handleDragOver);
uploadBox.addEventListener('dragleave', handleDragLeave);
uploadBox.addEventListener('drop', handleFileDrop);

tabButtons.forEach(button => {
    button.addEventListener('click', switchTab);
});

searchBtn.addEventListener('click', performSearch);

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

uploadNewBtn.addEventListener('click', resetApplication);

/*
File Upload Handlers
*/

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) uploadFile(file);
}

function handleDragOver(event) {
    event.preventDefault();
    uploadBox.style.borderColor = '#764ba2';
    uploadBox.style.backgroundColor = '#f5f5f5';
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadBox.style.borderColor = '#667eea';
    uploadBox.style.backgroundColor = 'white';
}

function handleFileDrop(event) {
    event.preventDefault();
    uploadBox.style.borderColor = '#667eea';
    uploadBox.style.backgroundColor = 'white';
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

/*
Upload File to Server
*/

async function uploadFile(file) {
    if (!file.name.endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }

    try {
        uploadBox.style.display = 'none';
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload protocol');
        }

        const data = await response.json();
        currentAnalysis = data;

        displayResults(data);
        loadingSpinner.style.display = 'none';
        resultsSection.style.display = 'block';

    } catch (error) {
        loadingSpinner.style.display = 'none';
        uploadBox.style.display = 'block';
        showError('Error uploading file: ' + error.message);
    }
}

/*
Display Results
*/

function displayResults(data) {
    displaySummary(data.summary);
    displayIssues(data.issues);
}

function displaySummary(summary) {
    summaryGrid.innerHTML = '';
    
    const items = [
        { key: 'has_study_design', label: 'Study Design' },
        { key: 'has_inclusion_criteria', label: 'Inclusion Criteria' },
        { key: 'has_exclusion_criteria', label: 'Exclusion Criteria' },
        { key: 'has_primary_endpoint', label: 'Primary Endpoint' },
        { key: 'has_safety_plan', label: 'Safety Plan' }
    ];

    items.forEach(item => {
        const value = summary[item.key];
        const statusClass = value ? 'present' : 'missing';
        const statusText = value ? 'PRESENT' : 'MISSING';

        const element = document.createElement('div');
        element.className = 'summary-item';
        element.innerHTML = `
            <h4>${item.label}</h4>
            <div class="value ${statusClass}">${statusText}</div>
        `;
        summaryGrid.appendChild(element);
    });
}

function displayIssues(issues) {
    issuesList.innerHTML = '';

    if (issues.length === 0) {
        issuesList.innerHTML = '<p>No major issues detected</p>';
        return;
    }

    issues.forEach(issue => {
        const element = document.createElement('div');
        element.className = `issue-item ${issue.severity}`;
        element.innerHTML = `
            <span class="severity-badge ${issue.severity}">${issue.severity.toUpperCase()}</span>
            <h3>${issue.issue}</h3>
            <p class="issue-description">${issue.description}</p>
            <p class="issue-recommendation">Recommendation: ${issue.recommendation}</p>
        `;
        issuesList.appendChild(element);
    });
}

/*
Tab Switching
*/

function switchTab(event) {
    const tabName = event.target.getAttribute('data-tab');

    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

/*
Search Functionality
*/

async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showError('Please enter a search term');
        return;
    }

    if (!currentAnalysis) {
        showError('No protocol loaded');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const data = await response.json();
        displaySearchResults(data.results);

    } catch (error) {
        showError('Error searching protocol: ' + error.message);
    }
}

function displaySearchResults(results) {
    searchResults.innerHTML = '';

    if (!results || results.length === 0) {
        const element = document.createElement('div');
        element.className = 'search-result-item';
        element.textContent = 'No results found';
        searchResults.appendChild(element);
        return;
    }

    results.forEach(result => {
        const element = document.createElement('div');
        element.className = 'search-result-item';
        element.textContent = result;
        searchResults.appendChild(element);
    });
}

/*
Error Handling
*/

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

/*
Reset Application
*/

function resetApplication() {
    uploadBox.style.display = 'block';
    resultsSection.style.display = 'none';
    loadingSpinner.style.display = 'none';
    errorMessage.style.display = 'none';
    fileInput.value = '';
    searchInput.value = '';
    summaryGrid.innerHTML = '';
    issuesList.innerHTML = '';
    searchResults.innerHTML = '';
    currentAnalysis = null;

    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    document.querySelector('[data-tab="summary"]').classList.add('active');
    document.getElementById('summary').classList.add('active');
}

/*
Initialize Application
*/

document.addEventListener('DOMContentLoaded', () => {
    console.log('Clinical Trial Protocol Analyzer initialized');
});
