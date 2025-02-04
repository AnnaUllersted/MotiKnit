const translations = {
    'en': {
        'title': 'Pattern Generator',
        'uploadLabel': 'Upload your desired pattern image:',
        'fileHelp': 'Use a .jpg or .jpeg image',
        'heightLabel': 'Desired height (cm):',
        'tooltip-description-heightLabel': 'Specify the height of the pattern on your knitting',
        'stitchLabel': 'Knitting gauge, stitches:',
        'tooltip-description-stitchLabel': 'Count and enter the number of stiches you have within 10 cm',
        'rowLabel': 'Knitting gauge, rows:',
        'tooltip-description-rowLabel': 'Count and enter the number of rows you have per 10 cm',
        'methodLabel': 'Knitting method:',
        'circularNeedles': 'Knitting in the round',
        'backAndForth': 'Knitting back and forth',
        'startLabel': 'Work beginning:',
        'topDown': 'Knitting top down',
        'bottomUp': 'Knitting bottom up',
        'intensityLabel': 'Pattern color intensity:',
        'intensity': 'Intensity',
        'generateButton': 'Generate pattern',
        'loading': 'Generating your knitting pattern... Please wait...',
        'imageLabel': 'Image:',
        'patternLabel': 'Knitted pattern:',
        'patternTitle': 'Knitting Pattern',
        'detailsTitle': 'Details:',
        'rows': 'rows',
        'stitches': 'stitches per 10cm',
        'instructions': 'Instructions:',
        'downloadPDF': 'Download PDF',
        'generatingPDF': 'Generating PDF...',
        'Examples': 'Examples'
    },
    'da': {
        'title': 'Strikke mønster generator',
        'uploadLabel': 'Upload billede af dit ønskede motiv:',
        'fileHelp': 'Brug et .jpg eller .jpeg billede',
        'heightLabel': 'Ønsket højde (cm):',
        'tooltip-description-heightLabel': 'Fortæl hvilken højde motivet skal have',
        'stitchLabel': 'Strikkefasthed, masker:',
        'tooltip-description-stitchLabel': 'Tæl og angiv hvor mange masker du har på 10 cm',
        'rowLabel': 'Strikkefasthed, pinde:',
        'tooltip-description-rowLabel': 'Tæl og angiv hvor mange pinde du har på 10 cm',
        'methodLabel': 'Strikkemetode:',
        'circularNeedles': 'Der strikkes på rundpind',
        'backAndForth': 'Der strikkes frem og tilbage',
        'startLabel': 'Arbejdets begyndelse:',
        'topDown': 'Der strikkes oppefra og ned',
        'bottomUp': 'Der strikkes nedefra og op',
        'intensityLabel': 'Intensitet af motivets farve:',
        'intensity': 'Intensitet',
        'generateButton': 'Generer mønster',
        'loading': 'Genererer din strikkeopskrift... Vent...',
        'imageLabel': 'Billede:',
        'patternLabel': 'Strikket motiv:',
        'patternTitle': 'Strikkeopskrift',
        'detailsTitle': 'Detaljer:',
        'rows': 'pinde',
        'stitches': 'masker per 10cm',
        'instructions': 'Instruktioner:',
        'downloadPDF': 'Download PDF',
        'generatingPDF': 'Genererer PDF...',
        'Examples': 'Eksempler'
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

function updatePageContent2(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang][key]) {
            if (element.classList.contains('tooltip-container')) {
                element.childNodes[0].textContent = translations[lang][key] + " "; // Opdater label-teksten
                const tooltipText = element.querySelector('.tooltip-description-' + key);
                if (tooltipText) {
                    tooltipText.textContent = translations[lang]['tooltip-description-' + key] || ''; // Sæt tooltip-teksten
                }
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
}


// Export for use in other files
window.translations = translations;
window.updatePageContent = updatePageContent;