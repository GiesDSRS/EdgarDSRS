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
        text = re.sub(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}', '', text)
        text = re.sub(r'^[^a-zA-Z\s]*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'(begin [0-9]{3} [^\n]+\n(.*\n)+end)', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[^\w\s]{10,}$', '', text, flags=re.MULTILINE)
        return text

    @staticmethod
    def extract_and_format_tables(soup):
        tables = soup.find_all("table")
        formatted_tables = []
        for table in tables:
            rows = table.find_all("tr")
            table_text = []
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_text = [cell.get_text(strip=True) for cell in cells]
                table_text.append("\t".join(row_text))
            formatted_tables.append("\n".join(table_text))
        return "\n\n".join(formatted_tables)

    @staticmethod
    def clean_html_content(html_content):
        for parser in ["html.parser", "lxml", "html5lib"]:
            try:
                soup = BeautifulSoup(html_content, parser)
                break
            except Exception as e:
                print(f"{parser} failed: {e}")
                if parser == "html5lib":
                    raise Exception("All HTML parsers failed")
        
        # Extract tables before unwrapping tags
        tables = EdgarAnalyzer.extract_and_format_tables(soup)

        for tag in soup.find_all(True):
            tag.unwrap()

        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)

        text = EdgarAnalyzer.remove_gibberish(text)
        text = EdgarAnalyzer.clean_noisy_text(text)
        text = ' '.join(text.split())

        return text, tables

    def process_html_file(self, input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()

            cleaned_text, tables = self.clean_html_content(content)

            base_name = os.path.basename(input_path)
            dir_name = os.path.dirname(input_path)
            output_file_name = os.path.splitext(base_name)[0] + "_cleaned.txt"
            output_path = os.path.join(dir_name, output_file_name)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)
                if tables:
                    file.write("\n\n--- Extracted Tables ---\n\n")
                    file.write(tables)

            print(f"Cleaned text and tables saved to: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return None


