# Translations
i18n = {
    'en': {
        'no_file': 'No file part',
        'no_selection': 'No selected file',
        'invalid_values': 'Invalid numeric values',
        'file_not_allowed': 'File type not allowed',
        'pattern_generated': 'Pattern generated successfully',
        'row_instructions': 'Row {row}: {details}',
        'ret_pind': 'Row {row} is a knit row',
        'vrang_pind': 'Row {row} is a purl row',
        'masker_details': '{count} {color} stitches',
        'error_message': 'An error occurred: {error}',
        'pinde_index': 'Row {index}',
        'pattern_title': 'Knitting Pattern',
        'details_title': 'Details:',
        'final_size': 'Final size: {size} x {size} cm',
        'knit_gauge': 'Gauge: {pinde} rows x {masker} stitches per 10cm',
        'pattern_size': 'Final size of pattern: {final_width} stiches x {final_height} rows',
        'instructions_title': 'Knitting Recipe:',
        'white': 'white',
        'black': 'black'
    },
    'da': {
        'no_file': 'Ingen fil fundet',
        'no_selection': 'Ingen fil valgt',
        'invalid_values': 'Ugyldige numeriske værdier',
        'file_not_allowed': 'Filtype ikke tilladt',
        'pattern_generated': 'Mønster genereret med succes',
        'row_instructions': 'Pind {row}: {details}',
        'ret_pind': 'Pind {row} er en retpind',
        'vrang_pind': 'Pind {row} er en vrangpind',
        'masker_details': '{count} {color} masker',
        'error_message': 'Der opstod en fejl: {error}',
        'pinde_index': 'Pind {index}',
        'pattern_title': 'Strikke Mønster',
        'details_title': 'Detaljer:',
        'final_size': 'Endelig størrelse: {size} x {size} cm',
        'knit_gauge': 'Strikkefasthed: {pinde} pinde x {masker} masker per 10cm',
        'pattern_size': 'Endeligt størrelse af mønster: {final_width} masker x {final_height} pinde',
        'instructions_title': 'Strikkeopskrift:',
        'white': 'hvide',
        'black': 'sorte'
    }
}

def translate(key, lang, **kwargs):
    language_map = i18n[lang]
    final_str =  language_map[key].format(**kwargs)
    return final_str