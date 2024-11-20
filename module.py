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
import xml.etree.ElementTree as ET

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
        text = re.sub(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}', ' ', text)
        text = re.sub(r'^[^a-zA-Z\s]*$', ' ', text, flags=re.MULTILINE)
        text = re.sub(r'(begin [0-9]{3} [^\n]+\n(.*\n)+end)', ' ', text, flags=re.MULTILINE)
        text = re.sub(r'^[^\w\s]{10,}$', ' ', text, flags=re.MULTILINE)
        return text

    @staticmethod
    def extract_and_format_tables(soup):
        # Find all table elements
        tables = soup.find_all("table")
        formatted_tables = []

        for table in tables:
            rows = table.find_all("tr")  # Find all rows in the table
            table_text = []
            
            for row in rows:
                # Find all cells (both <td> and <th>)
                cells = row.find_all(["td", "th"])
                # Extract text and clean it
                row_text = [
                    " ".join(cell.get_text(" ", strip=True).split())  # Use " " for space between <p> or other tags
                    for cell in cells
                ]
                # Only add non-empty rows
                if row_text:
                    table_text.append("\t".join(row_text))
            
            # Only add non-empty tables
            if table_text:
                formatted_tables.append("\n".join(table_text))
        
        # Join all tables with double newlines
        return "\n\n".join(formatted_tables)
    
    @staticmethod
    def detect_file_format(content):
        """
        Detect whether the file is HTML or XBRL (XML).
        """
        if content.strip().startswith("<?xml"):
            return "XBRL"
        elif "<html" in content.lower():
            return "HTML"
        else:
            return "UNKNOWN"
        
    @staticmethod
    def process_xbrl(root):
        """
        Processes XBRL content to extract meaningful data and tables.
        :param root: XML root element of the XBRL document.
        :return: Extracted text and structured tables.
        """
        xbrl_data = []  # To store structured XBRL data
        xbrl_text = []  # To store plain text representation

        # Extract contexts and units
        contexts = EdgarAnalyzer.extract_contexts(root)
        units = EdgarAnalyzer.extract_units(root)

        # Extract facts and group into rows
        for fact in root.iter():
            if fact.tag.startswith("{http://www.xbrl.org/2003/instance}"):
                tag = fact.tag.split("}")[-1]
                context_ref = fact.get("contextRef")
                unit_ref = fact.get("unitRef")
                value = fact.text

                if context_ref in contexts:
                    xbrl_data.append({
                        "tag": tag,
                        "value": value.strip() if value else None,
                        "context": contexts[context_ref],
                        "unit": units.get(unit_ref, None)
                    })
                    xbrl_text.append(f"{tag}: {value.strip() if value else ''}")

        # Combine XBRL text into a single string
        xbrl_text_combined = ' '.join(xbrl_text)
        return xbrl_text_combined, xbrl_data

    @staticmethod
    def extract_contexts(root):
        """
        Extracts context information from an XBRL document.
        :param root: XML root element of the XBRL document.
        :return: Dictionary of context references.
        """
        contexts = {}
        for context in root.findall(".//{http://www.xbrl.org/2003/instance}context"):
            context_id = context.get("id")
            period = context.find(".//{http://www.xbrl.org/2003/instance}period")
            start_date = period.find("{http://www.xbrl.org/2003/instance}startDate")
            end_date = period.find("{http://www.xbrl.org/2003/instance}endDate")
            contexts[context_id] = {
                "startDate": start_date.text if start_date is not None else None,
                "endDate": end_date.text if end_date is not None else None
            }
        return contexts

    @staticmethod
    def extract_units(root):
        """
        Extracts unit information from an XBRL document.
        :param root: XML root element of the XBRL document.
        :return: Dictionary of unit references.
        """
        units = {}
        for unit in root.findall(".//{http://www.xbrl.org/2003/instance}unit"):
            unit_id = unit.get("id")
            measure = unit.find("{http://www.xbrl.org/2003/instance}measure")
            units[unit_id] = measure.text if measure is not None else None
        return units
    
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
            # tag.insert_after(' ')
            tag.unwrap()

        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'<.*?>', ' ', text)
        text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)


        text = EdgarAnalyzer.remove_gibberish(text)
        text = EdgarAnalyzer.clean_noisy_text(text)
        text = ' '.join(text.split())
        
        return text, tables
        # return text

    def process_html_file(self, input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Detect file format
            format = self.detect_file_format(content)
            if format == "HTML":
                cleaned_text, tables = self.clean_html_content(content)
            elif format == "XBRL":
                root = ET.fromstring(content)
                cleaned_text, tables = self.process_xbrl(root)
            else:
                raise ValueError("Unsupported file format")
            
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
