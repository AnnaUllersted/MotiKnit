const translations = {
    'en': {
        'title': 'Pattern Generator',
        'uploadLabel': 'Upload your desired pattern image:',
        'fileHelp': 'Use a .jpg or .jpeg image. Or choose one of these patterns.',
        'heightLabel': 'Desired height (cm):',
        'heightHelp': 'Specify the height of the pattern on your knitting',
        'stitchLabel': 'Knitting gauge, stitches:',
        'stitchHelp': 'Enter number of stitches per 10 cm',
        'rowLabel': 'Knitting gauge, rows:',
        'rowHelp': 'Enter number of rows per 10 cm',
        'methodLabel': 'Knitting method:',
        'circularNeedles': 'Knitting in the round',
        'backAndForth': 'Knitting back and forth',
        'startLabel': 'Work beginning:',
        'topDown': 'Knitting top down',
        'bottomUp': 'Knitting bottom up',
        'intensityLabel': 'Pattern color intensity:',
        'intensity': 'Intensity',
        'generateButton': 'Generate free pattern and instructions',
        'loading': 'Generating your knitting pattern... Please wait...',
        'imageLabel': 'Image:',
        'patternLabel': 'Knitted pattern:',
        'patternTitle': 'Knitting Pattern',
        'detailsTitle': 'Details:',
        'finalSize': 'Final size',
        'gauge': 'Gauge',
        'rows': 'rows',
        'stitches': 'stitches per 10cm',
        'finalPattern': 'Final pattern size',
        'instructions': 'Instructions:',
        'downloadPDF': 'Download PDF',
        'generatingPDF': 'Generating PDF...'
    },
    'da': {
        'title': 'Strikke mønster generator',
        'uploadLabel': 'Upload billede af dit ønskede motiv:',
        'fileHelp': 'Brug et .jpg eller .jpeg billede. Eller vælg et af disse motiver.',
        'heightLabel': 'Ønsket højde (cm):',
        'heightHelp': 'Fortæl hvilken højde motivet skal have på dit strikketøj',
        'stitchLabel': 'Strikkefasthed, masker:',
        'stitchHelp': 'Angiv antal masker på 10 cm',
        'rowLabel': 'Strikkefasthed, pinde:',
        'rowHelp': 'Angiv antal pinde på 10 cm',
        'methodLabel': 'Strikkemetode:',
        'circularNeedles': 'Der strikkes på rundpind',
        'backAndForth': 'Der strikkes frem og tilbage',
        'startLabel': 'Arbejdets begyndelse:',
        'topDown': 'Der strikkes oppefra og ned',
        'bottomUp': 'Der strikkes nedefra og op',
        'intensityLabel': 'Intensitet af motivets farve:',
        'intensity': 'Intensitet',
        'generateButton': 'Generer gratis mønster og opskrift',
        'loading': 'Genererer din strikkeopskrift... Vent...',
        'imageLabel': 'Billede:',
        'patternLabel': 'Strikket motiv:',
        'patternTitle': 'Strikkeopskrift',
        'detailsTitle': 'Detaljer:',
        'finalSize': 'Endelig størrelse',
        'gauge': 'Strikkefasthed',
        'rows': 'pinde',
        'stitches': 'masker per 10cm',
        'finalPattern': 'Endeligt størrelse af mønster',
        'instructions': 'Instruktioner:',
        'downloadPDF': 'Download PDF',
        'generatingPDF': 'Genererer PDF...'
    }
};

// Function to update page content based on language
function updatePageContent(lang) {
    // Get all elements with data-translate attribute
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang][key]) {
            if (element.tagName === 'INPUT' && element.type === 'submit') {
                element.value = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
}

// Export for use in other files
window.translations = translations;
window.updatePageContent = updatePageContent;