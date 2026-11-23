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
        'tooltip-description-intensityLabel': 'Higher intensity gives more detail.',
        'intensityLowAlt': 'Knitting chart of a bee at 20% intensity',
        'intensityHighAlt': 'Knitting chart of a bee at 80% intensity',
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
        'insta-tagline':"Follow us on instagram",
        'menuMotifs': 'Free knitting motifs',
        'seeAll': 'See all motifs →',
        'howTitle': 'How it works',
        'howStep1Title': 'Upload a picture',
        'howStep1Text': 'Choose a .jpg picture with a clear shape, or use one of the free motifs.',
        'howStep2Title': 'Choose size and gauge',
        'howStep2Text': 'Enter how tall the motif should be and how many stitches and rows you knit per 10 cm.',
        'howStep3Title': 'Get your chart and pattern',
        'howStep3Text': 'You get a knitting chart and a row-by-row pattern that you can download as a PDF.',
        'howBefore': 'Before: your picture',
        'howAfter': 'After: your knitting chart',
        'howBeforeAlt': 'Picture of Santa Claus with his sack of presents',
        'howAfterAlt': 'Knitting chart of Santa Claus',
        'howAfterSrc': '/static/motifs/santa-claus-chart-en.png',
        'tagline': 'Upload a picture and get a finished knitting chart and pattern in your own size – all for free.',
        'cookieMessage': 'We use cookies (Google Analytics and Pinterest) to measure traffic and improve the site. You can accept or decline them.',
        'cookieAccept': 'Accept',
        'cookieDecline': 'Decline'
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
        'tooltip-description-intensityLabel': 'Højere intensitet giver flere detaljer.',
        'intensityLowAlt': 'Strikkediagram af en bi med 20 % intensitet',
        'intensityHighAlt': 'Strikkediagram af en bi med 80 % intensitet',
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
        'insta-tagline':'Følg os på instagram',
        'menuMotifs': 'Gratis strikkemotiver',
        'seeAll': 'Se alle motiver →',
        'howTitle': 'Sådan virker det',
        'howStep1Title': 'Upload et billede',
        'howStep1Text': 'Vælg et .jpg-billede med en tydelig figur, eller brug et af de gratis motiver.',
        'howStep2Title': 'Vælg størrelse og strikkefasthed',
        'howStep2Text': 'Skriv hvor højt motivet skal være, og hvor mange masker og pinde du strikker på 10 cm.',
        'howStep3Title': 'Få diagram og opskrift',
        'howStep3Text': 'Du får et strikkediagram og en opskrift pind for pind, som du kan hente som PDF.',
        'howBefore': 'Før: dit billede',
        'howAfter': 'Efter: dit strikkediagram',
        'howBeforeAlt': 'Billede af julemanden med gavesæk',
        'howAfterAlt': 'Strikkediagram af julemanden',
        'howAfterSrc': '/static/motifs/santa-claus-chart-da.png',
        'tagline': 'Upload et billede, og få et færdigt strikkediagram og en opskrift i din egen størrelse – helt gratis.',
        'cookieMessage': 'Vi bruger cookies (Google Analytics og Pinterest) til at måle trafik og forbedre siden. Du kan acceptere eller afvise dem.',
        'cookieAccept': 'Accepter',
        'cookieDecline': 'Afvis'
    }
};

// Function to update page content based on language
function updatePageContent(lang) {
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

    // Image alt texts and language-specific images
    document.querySelectorAll('[data-translate-alt]').forEach(element => {
        const key = element.getAttribute('data-translate-alt');
        if (translations[lang][key]) {
            element.alt = translations[lang][key];
        }
    });
    document.querySelectorAll('[data-translate-src]').forEach(element => {
        const key = element.getAttribute('data-translate-src');
        if (translations[lang][key]) {
            element.src = translations[lang][key];
        }
    });
}


// Export for use in other files
window.translations = translations;
window.updatePageContent = updatePageContent;