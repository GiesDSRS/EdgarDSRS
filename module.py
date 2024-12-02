import os
import re
import unicodedata
from bs4 import BeautifulSoup
import logging

class EdgarAnalyzer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def clean_noisy_text(self, text):
        if not text:
            return ""
        
        def is_noisy(word):
            # Allow specific patterns like "0000907471-18-000139", "0000907471-18-000139.txt", and "0001000015-98-000009.hdr.sgml"
            if re.match(r'^\d{10}-\d{2}-\d{6}(\.txt|\.hdr\.sgml)?$', word):
                return False
            
            # Check for noisy conditions
            return len(word) > 15 and (
                re.search(r'[A-Z].*[a-z].*\d', word) or 
                re.search(r'[^A-Za-z0-9]', word)
            )
        
        # Filter out noisy words
        cleaned_words = [word for word in text.split() if not is_noisy(word)]
        
        return ' '.join(cleaned_words)

    def clean_html_content(self, html_content):
        if not html_content:
            self.logger.warning("Empty HTML content provided")
            return "", ""

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            self.logger.info("Successfully parsed HTML")
        except Exception as e:
            self.logger.error(f"HTML parsing failed: {e}")
            return "", ""

        # Extract tables first
        tables = []
        for table in soup.find_all('table'):
            table_text = []
            for row in table.find_all('tr'):
                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if any(cells):
                    table_text.append('\t'.join(cells))
            if table_text:
                tables.append('\n'.join(table_text))
        formatted_tables = '\n\n'.join(tables)

        # Remove unwanted elements
        for element in soup(['script', 'style', 'meta', 'link', 'head']):
            element.decompose()

        # Get text content
        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'(<.*?>)'                             # Matches HTML tags
                    r'|(&[a-zA-Z0-9#]+;)'                  # Matches HTML entities
                    r'|[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}'  # Matches sequences of 5+ special characters
                    r'|^\s*[^a-zA-Z\s]*$'                  # Matches lines with only non-alphabetic content
                    r'|begin [0-9]{3} [^\n]+\n(.*\n)+?end' # Matches "begin 644 ... end" blocks
                    r'|^[^\w\s]{10,}$'                     # Matches lines with 10+ consecutive special characters
                    r'|\s+',                               # Matches multiple spaces
                    ' ', 
                    text, 
                    flags=re.MULTILINE)

    #     text = re.sub(
    # r'(<.*?>)|(&[a-zA-Z0-9#]+;)|[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}|\s+', 
    # ' ', 
    # text, 
    # flags=re.MULTILINE)
        text = self.clean_noisy_text(text)
        
        return text, formatted_tables

    def process_html_file(self, input_path, output_dir=None):
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")

            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(input_path, 'r', encoding=encoding) as file:
                        content = file.read()
                        self.logger.info(f"Read file with {encoding} encoding")
                        break
                except UnicodeDecodeError:
                    continue
            else:
                raise UnicodeDecodeError("Failed to read file with any encoding")

            cleaned_text, tables = self.clean_html_content(content)

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                base_name = os.path.basename(input_path)
                output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_cleaned.txt")
            else:
                output_path = f"{os.path.splitext(input_path)[0]}_cleaned.txt"

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)
                if tables:
                    file.write("\n\n--- Extracted Tables ---\n\n")
                    file.write(tables)

            self.logger.info(f"Cleaned text saved to: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            return None