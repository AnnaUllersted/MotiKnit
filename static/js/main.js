// Global variables
let currentProcessedImage = null;
let currentParameters = null;
let currentInstructions = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const originalImage = document.getElementById('originalImage');
const processedImage = document.getElementById('processedImage');
const resultDiv = document.getElementById('result');
const instructionsElement = document.getElementById('instructions');
const errorElement = document.getElementById('error');
const loadingElement = document.getElementById('loading');
const imageGrid = document.getElementById('imageGrid');
const uploadForm = document.getElementById('uploadForm');
const downloadButton = document.getElementById('downloadPdfButton');

// Slider functionality
const slider = document.getElementById("myRange");
const output = document.getElementById("demo");

// Initialize the slider output display
output.innerHTML = slider.value;

// Preset image settings
const presetSettings = {
    'preset1.jpg': 50,  
    'preset2.jpg': 80,
    'preset3.jpg': 90,
    'preset4.jpg': 75,
    'preset5.jpg': 40,
    'preset6.jpg': 85
};

// Update slider output when value changes
slider.oninput = function() {
    output.innerHTML = this.value;
};

// Add mouseup event to trigger form submission when slider is released
slider.addEventListener('mouseup', function() {
    if (fileInput.files.length > 0) {
        uploadForm.requestSubmit();
    }
});

// Touch support for mobile devices
slider.addEventListener('touchend', function() {
    if (fileInput.files.length > 0) {
        uploadForm.requestSubmit();
    }
});

// Function to select a preset image
async function selectPresetImage(imgElement) {
    try {
        const response = await fetch(imgElement.src);
        const blob = await response.blob();
        const file = new File([blob], 'preset.jpg', { type: 'image/jpeg' });
        
        // Create a new FileList-like object
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        
        // Update the file input
        fileInput.files = dataTransfer.files;
        
        // Show the selected image in the preview
        originalImage.src = imgElement.src;
        originalImage.style.display = 'block';
        imageGrid.style.display = 'flex';

        // Set slider value based on preset image
        const imageName = imgElement.src.split('/').pop();
        if (presetSettings[imageName]) {
            slider.value = presetSettings[imageName];
            output.innerHTML = slider.value;
        }
    } catch (error) {
        showError('Error loading preset image');
    }
}

// Show the original image after it's uploaded
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            originalImage.src = e.target.result;
            originalImage.style.display = 'block'; // Show image
            imageGrid.style.display = 'flex'; // Show image grid with flex layout
        }
        reader.readAsDataURL(file);
    }
});

// Handle form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!fileInput.files[0]) {
        showError('Please select a file');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('size', document.getElementById('size').value);
    formData.append('pinde', document.getElementById('pinde').value);
    formData.append('masker', document.getElementById('masker').value);
    formData.append('alternating_iteration', document.getElementById('alternating_iteration').value);
    formData.append('bottom_to_top', document.getElementById('bottom_to_top').value);
    formData.append('intensity', slider.value);
    
    try {
        clearError();
        resultDiv.style.display = 'none';
        showLoading();

        // Make request to backend
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Error processing image');
        }
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

// Handle PDF download
downloadButton.addEventListener('click', async () => {
    try {
        // Show loading state
        const originalText = downloadButton.textContent;
        downloadButton.textContent = 'Genererer PDF...';
        downloadButton.disabled = true;

        const response = await fetch('/download-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                processed_image: currentProcessedImage,
                parameters: currentParameters,
                instructions: currentInstructions
            })
        });

        if (!response.ok) {
            throw new Error('Failed to generate PDF');
        }

        const blob = await response.blob();

        // Use FileSaver.js for other devices
        saveAs(blob, 'knitting_pattern.pdf');
        
    } catch (error) {
        showError('Error generating PDF: ' + error.message);
    } finally {
        // Reset button state
        downloadButton.textContent = originalText;
        downloadButton.disabled = false;
    }
});

// Helper functions
function displayResults(data) {
    processedImage.src = `data:image/png;base64,${data.processed_image}`;
    processedImage.style.display = 'block';
    currentProcessedImage = data.processed_image;
    currentParameters = data.parameters;
    currentInstructions = data.instructions;

    processedImage.onload = () => {
        document.getElementById('result').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    };

    // Display parameters
    document.getElementById('finalSizeValue').textContent = data.parameters.final_size;
    document.getElementById('finalGaugeValue').textContent = data.parameters.final_gauge;
    document.getElementById('finalPatternSizeValue').textContent = data.parameters.final_pattern_size;
    
    // Display instructions
    instructionsElement.textContent = data.instructions.join('\n');
    
    resultDiv.style.display = 'block';
    document.getElementById('downloadContainer').style.display = 'block';
}

function showError(message) {
    errorElement.textContent = message;
}

function clearError() {
    errorElement.textContent = '';
}

function showLoading() {
    loadingElement.style.display = 'block';
}

function hideLoading() {
    loadingElement.style.display = 'none';
}

// Initialize language based on user's browser or domain
function initializeLanguage() {
    let currentLang = Intl.DateTimeFormat().resolvedOptions().locale.split('-')[0];
    if (!['da','en'].includes(currentLang)){
        currentLang = window.location.hostname.includes('motiknit.dk') ? 'da' : 'en';
    }
    updatePageContent(currentLang);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguage();
});
