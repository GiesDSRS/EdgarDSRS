"""
Goal: Read in raw Edgar files, downloadable from the
...

module.py is an auxiliary file that defines the following classes
(1) EdgarAnalyzer

See Example.py for implementation of the EdgarAnalyzer functions
"""
import os
import re
import unicodedata
from bs4 import BeautifulSoup
import glob
import pandas as pd

class EdgarAnalyzer(object):
    """
    Object class to read in Edgar 10k Data
    """
    def clean_html_content(html_content):
       # Parse the HTML content
        try:
            soup = BeautifulSoup(html_content, "html.parser")
        except Exception as e:
            print(f"html.parser failed: {e}")
            try:
                soup = BeautifulSoup(html_content, "lxml")
            except Exception as e:
                print(f"lxml failed: {e}")
                try:
                    soup = BeautifulSoup(html_content, "html5lib")
                except Exception as e:
                    print(f"html5lib failed: {e}")
                    raise
        # soup = BeautifulSoup(html_content, "html.parser")

        # Removes all tags
        for tag in soup.find_all(True):
            tag.unwrap()

        # Extract text and normalize Unicode characters
        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)

        # Remove any remaining HTML entities
        text = re.sub(r'<.*?>', '', text)  # Remove any remaining HTML tags
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)

        # Define a function to remove gibberish based on specific patterns
        def remove_gibberish(text):
            # Removes long sequences of characters without spaces
            # this will remove long normal words, e.g. characteristics
            # text = re.sub(r'\b\w{15,}\b', '', text)

            # Removes sequences with high special character density
            text = re.sub(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}', '', text)

            # Removes lines that are mostly numbers or symbols
            text = re.sub(r'^[^a-zA-Z\s]*$', '', text, flags=re.MULTILINE)

            # Additional patterns for gibberish removal
            # Removes base64 encoded text patterns
            text = re.sub(r'(begin [0-9]{3} [^\n]+\n(.*\n)+end)', '', text, flags=re.MULTILINE)

            # Removes lines that contain too many non-alphanumeric characters
            text = re.sub(r'^[^\w\s]{10,}$', '', text, flags=re.MULTILINE)

            return text


        def clean_noisy_text(text):
            # Split the text into individual words
            words = text.split()

            # Define a function to identify "noisy strings"
            def is_noisy(word):
                # If the word is longer than 15 characters and contains:
                # - Mixed uppercase and lowercase letters
                # - Numbers
                if len(word) > 15 and (
                    re.search(r'[A-Z]', word) and re.search(r'[a-z]', word) and re.search(r'\d', word)
                ):
                    return True
                # If the word is longer than 15 characters and contains symbols
                if len(word) > 15 and re.search(r'[^A-Za-z0-9]', word):
                    return True
                return False

            # Keep only meaningful words, removing the noisy ones
            cleaned_words = [word for word in words if not is_noisy(word)]

            # Return the cleaned text
            return ' '.join(cleaned_words)

        text = remove_gibberish(text)
        text = clean_noisy_text(text)
        text = ' '.join(text.split())

        return text