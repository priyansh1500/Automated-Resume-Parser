// main.js — Automated Resume Parser
//
// Stage 2: Shows the selected filename when the user picks a file.
// Stage 3: Adds a loading state on the Upload button while the form submits.

// --- Feature 1: Show filename when user selects a file ---
const fileInput = document.getElementById('resume');
const fileNameDisplay = document.getElementById('file-name-display');

if (fileInput && fileNameDisplay) {
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = 'No file selected';
        }
    });
}

// --- Feature 2: Show loading state when the form is submitted ---
// This prevents the user from clicking Upload multiple times
// and gives them visual feedback that the upload is in progress.
const uploadForm = document.getElementById('upload-form');
const uploadBtn = document.getElementById('upload-btn');

if (uploadForm && uploadBtn) {
    uploadForm.addEventListener('submit', function () {
        // Change the button text to indicate loading
        uploadBtn.textContent = 'Uploading... ⏳';
        // Disable the button to prevent double submissions
        uploadBtn.disabled = true;
    });
}
