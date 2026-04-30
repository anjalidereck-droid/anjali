const API_URL = 'http://localhost:8001';

const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const submitBtn = document.getElementById('submitBtn');
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
const fileLabel = document.getElementById('fileLabel');

let currentAnalysis = null;
let selectedFile = null;

uploadBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) handleFile(file);
});

uploadBox.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadBox.classList.remove('dragover');
    const files = event.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

submitBtn.addEventListener('click', async () => {
    if (selectedFile) {
        await uploadFile(selectedFile);
    } else {
        showError('Please choose a PDF first.');
    }
});

tabButtons.forEach(button => {
    button.addEventListener('click', switchTab);
});

searchBtn.addEventListener('click', performSearch);

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

uploadNewBtn?.addEventListener('click', resetApplication);

function handleFile(file) {
    const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');

    if (!isPdf) {
        showError('Please select a PDF file.');
        return;
    }

    selectedFile = file;
    fileLabel.textContent = `Selected file: ${file.name}`;
    submitBtn.disabled = false;
    hideError();
}

async function uploadFile(file) {
    try {
        uploadBox.style.display = 'none';
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file, file.name);

        const response = await fetch(`${API_URL}/api/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || `Upload failed with status ${response.status}`);
        }

        currentAnalysis = data;
        renderResults(data);

        loadingSpinner.style.display = 'none';
        resultsSection.style.display = 'block';
    } catch (error) {
        loadingSpinner.style.display = 'none';
        uploadBox.style.display = 'block';
        showError('Error uploading file: ' + error.message);
    }
}

function renderResults(data) {
    renderStatus(data);
    renderSummary(data.summary);
    renderIssues(data.issues);
}

function renderStatus(data) {
    let statusBanner = document.getElementById('statusBanner');

    if (!statusBanner) {
        statusBanner = document.createElement('div');
        statusBanner.id = 'statusBanner';
        statusBanner.className = 'status-banner';
        resultsSection.prepend(statusBanner);
    }

    const issuesCount = Array.isArray(data.issues) ? data.issues.length : 0;

    statusBanner.innerHTML = `
        <div class="status-card ${data.status === 'success' ? 'success' : 'error'}">
            <h3>${data.status === 'success' ? 'Upload Successful' : 'Upload Failed'}</h3>
            <p>${data.message || ''}</p>
        </div>
        <div class="meta-card">
            <h4>Page Count</h4>
            <div class="value present">${data.page_count ?? 'N/A'}</div>
        </div>
        <div class="meta-card">
            <h4>Issues</h4>
            <div class="value ${issuesCount === 0 ? 'present' : 'missing'}">
                ${issuesCount === 0 ? 'None found' : issuesCount}
            </div>
        </div>
    `;
}

function renderSummary(summary) {
    summaryGrid.innerHTML = '';

    const items = [
        { key: 'has_study_design', label: 'Study Design' },
        { key: 'has_inclusion_criteria', label: 'Inclusion Criteria' },
        { key: 'has_exclusion_criteria', label: 'Exclusion Criteria' },
        { key: 'has_primary_endpoint', label: 'Primary Endpoint' },
        { key: 'has_safety_plan', label: 'Safety Plan' }
    ];

    items.forEach(item => {
        const value = summary?.[item.key];
        const card = document.createElement('div');
        card.className = 'summary-item';
        card.innerHTML = `
            <h4>${item.label}</h4>
            <div class="value ${value ? 'present' : 'missing'}">${value ? 'PRESENT' : 'MISSING'}</div>
        `;
        summaryGrid.appendChild(card);
    });
}

function renderIssues(issues) {
    issuesList.innerHTML = '';

    if (!issues || issues.length === 0) {
        issuesList.innerHTML = '<p class="ready-message">No major issues detected</p>';
        return;
    }

    issues.forEach(issue => {
        const card = document.createElement('div');
        card.className = `issue-item ${issue.severity || 'low'}`;
        card.innerHTML = `
            <span class="severity-badge ${issue.severity || 'low'}">${(issue.severity || 'low').toUpperCase()}</span>
            <h3>${issue.issue || 'Issue'}</h3>
            <p class="issue-description">${issue.description || ''}</p>
            <p class="issue-recommendation">Recommendation: ${issue.recommendation || ''}</p>
        `;
        issuesList.appendChild(card);
    });
}

function switchTab(event) {
    const tabName = event.target.getAttribute('data-tab');

    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showError('Please enter a search term.');
        return;
    }

    if (!currentAnalysis) {
        showError('No protocol loaded.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || 'Search failed');
        }

        renderSearchResults(data.results);
    } catch (error) {
        showError('Error searching protocol: ' + error.message);
    }
}

function renderSearchResults(results) {
    searchResults.innerHTML = '';

    if (!results || results.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">No results found</div>';
        return;
    }

    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.textContent = result;
        searchResults.appendChild(item);
    });
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';

    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

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
    selectedFile = null;
    currentAnalysis = null;
    submitBtn.disabled = true;
    fileLabel.textContent = 'Click to select or drag and drop your PDF file';

    const statusBanner = document.getElementById('statusBanner');
    if (statusBanner) statusBanner.remove();

    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    document.querySelector('[data-tab="summary"]').classList.add('active');
    document.getElementById('summary').classList.add('active');
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Clinical Trial Protocol Analyzer initialized');
});