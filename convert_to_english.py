#!/usr/bin/env python3

import sys
import argparse
import unicodedata
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Extended Arabic to English character mapping
ar_chars_dict = {
    u'ذ': '`', u'ض': 'q', u'ص': 'w', u'ث': 'e', u'ق': 'r', u'ف': 't', u'غ': 'y', u'ع': 'u', u'ه': 'i', u'خ': 'o',
    u'ح': 'p', u'ج': '[', u'د': ']',
    u'ش': 'a', u'س': 's', u'ي': 'd', u'ب': 'f', u'ل': 'g', u'ا': 'h', u'ت': 'j', u'ن': 'k', u'م': 'l', u'ك': ';',
    u'ط': "'",
    u'ئ': 'z', u'ء': 'x', u'ؤ': 'c', u'ر': 'v', u'ﻻ': 'b', u'ى': 'n', u'ة': 'm', u'و': ',', u'ز': '.', u'ظ': '/',
    ' ': ' ', '\n': '', u'؟': '?',
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
    u'أ': 'H', u'إ': 'Y', u'آ': 'N',
}

def normalize_and_replace_chars(text: str):
    """ Normalize Unicode characters and replace Arabic characters with corresponding English ones. """
    normalized_text = unicodedata.normalize('NFKD', text)
    line = ""
    abnormal_chars = []
    for cch in normalized_text:
        try:
            line += ar_chars_dict.get(cch, cch)  # Use the character itself if not found in the mapping
        except KeyError as e:
            logging.error(f"Error processing character: {e}")
            line += cch
        if cch not in ar_chars_dict and cch not in abnormal_chars:
            abnormal_chars.append(cch)
    if abnormal_chars:
        logging.warning(f"Abnormal chars: {', '.join(x.encode('unicode_escape').decode('utf8') for x in abnormal_chars)}")
    return line

def main(arguments):
    """ Main function to handle command-line arguments and text processing. """
    parser = argparse.ArgumentParser(
        description="Convert Arabic characters in text to corresponding English characters based on QWERTY keyboard layout.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("text", help="Input Arabic text to be converted", nargs="+")
    
    args = parser.parse_args(arguments)

    # Join the list of arguments into a single string, assuming that the input might contain spaces
    input_text = ' '.join(args.text)
    print(normalize_and_replace_chars(input_text))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
