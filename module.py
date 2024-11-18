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

class EdgarAnalyzer:
    @staticmethod
    def clean_noisy_text(text):
        words = text.split()
        
        def is_noisy(word):
            if len(word) > 15 and (
                re.search(r'[A-Z]', word) and 
                re.search(r'[a-z]', word) and 
                re.search(r'\d', word)
            ):
                return True
            if len(word) > 15 and re.search(r'[^A-Za-z0-9]', word):
                return True
            return False
            
        cleaned_words = [word for word in words if not is_noisy(word)]
        return ' '.join(cleaned_words)

    @staticmethod
    def remove_gibberish(text):
        # Remove sequences with high special character density
        text = re.sub(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}', '', text)
        
        # Remove lines that are mostly numbers or symbols
        text = re.sub(r'^[^a-zA-Z\s]*$', '', text, flags=re.MULTILINE)
        
        # Remove base64 encoded text patterns
        text = re.sub(r'(begin [0-9]{3} [^\n]+\n(.*\n)+end)', '', text, flags=re.MULTILINE)
        
        # Remove lines with too many non-alphanumeric characters
        text = re.sub(r'^[^\w\s]{10,}$', '', text, flags=re.MULTILINE)
        
        return text

    @staticmethod
    def clean_html_content(html_content):
        # Try different parsers
        for parser in ["html.parser", "lxml", "html5lib"]:
            try:
                soup = BeautifulSoup(html_content, parser)
                break
            except Exception as e:
                print(f"{parser} failed: {e}")
                if parser == "html5lib":
                    raise Exception("All HTML parsers failed")

        # Remove all tags while keeping their content
        for tag in soup.find_all(True):
            tag.unwrap()

        # Get text and normalize
        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)

        # Remove HTML remnants
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)

        # Clean the text
        text = EdgarAnalyzer.remove_gibberish(text)
        text = EdgarAnalyzer.clean_noisy_text(text)
        text = ' '.join(text.split())

        return text

def process_file(input_path, output_path=None):
    """
    Process a single HTML file and optionally save the cleaned output
    
    Args:
        input_path: Path to input HTML file
        output_path: Optional path to save cleaned text
    
    Returns:
        Cleaned text content
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        cleaned_text = EdgarAnalyzer.clean_html_content(content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)
            print(f"Cleaned text saved to: {output_path}")
            
        return cleaned_text
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your input file path
    input_file = "/home/jovyan/datahub/1003078-MSC INDUSTRIAL DIRECT CO INC-10-K-2021-10-20.txt"
    output_file = "cleaned_output.txt"
    
    cleaned_text = process_file(input_file, output_file)
    
    if cleaned_text:
        print("\nFirst 500 characters of cleaned text:")
        print(cleaned_text[:500])
