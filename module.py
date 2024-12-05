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
           if re.match(r'^\d{10}-\d{2}-\d{6}(\.txt|\.hdr\.sgml)?$', word):
               return False
           
           return len(word) > 15 and (
               re.search(r'[A-Z].*[a-z].*\d', word) or 
               re.search(r'[^A-Za-z0-9]', word)
           )
       
       cleaned_words = [word for word in text.split() if not is_noisy(word)]
       return ' '.join(cleaned_words)

   @staticmethod
   def extract_and_format_tables(soup):
       if not soup:
           return ""

       def process_table_cells(cells):
           return [
               " ".join(cell.get_text(" ", strip=True).split())
               for cell in cells
               if cell.get_text(strip=True)
           ]

       tables = []
       
       table_elements = (
           soup.find_all('table') +
           soup.find_all('TABLE') +
           soup.find_all(lambda tag: tag.name == 'table' and 
                        (tag.find('ix:nonnumeric') or 
                         tag.find('ix:nonfraction') or 
                         tag.find('ix:fraction')))
       )

       for table in table_elements:
           table_text = []
           
           thead = table.find(['thead', 'THEAD'])
           if thead:
               header_rows = thead.find_all(['tr', 'TR'])
               for row in header_rows:
                   header_cells = row.find_all(['th', 'TD', 'td', 'TH'])
                   if header_cells:
                       processed_cells = process_table_cells(header_cells)
                       if processed_cells:
                           table_text.append('\t'.join(processed_cells))
           
           tbody = table.find(['tbody', 'TBODY']) or table
           rows = tbody.find_all(['tr', 'TR'])
           
           for row in rows:
               regular_cells = row.find_all(['td', 'TD', 'th', 'TH'])
               xbrl_cells = row.find_all(['ix:nonnumeric', 'ix:nonfraction', 'ix:fraction'])
               
               if regular_cells:
                   processed_cells = process_table_cells(regular_cells)
               elif xbrl_cells:
                   processed_cells = process_table_cells(xbrl_cells)
               else:
                   continue
                   
               if processed_cells:
                   table_text.append('\t'.join(processed_cells))
           
           tfoot = table.find(['tfoot', 'TFOOT'])
           if tfoot:
               footer_rows = tfoot.find_all(['tr', 'TR'])
               for row in footer_rows:
                   footer_cells = row.find_all(['td', 'TD', 'th', 'TH'])
                   if footer_cells:
                       processed_cells = process_table_cells(footer_cells)
                       if processed_cells:
                           table_text.append('\t'.join(processed_cells))
           
           if table_text:
               tables.append('\n'.join(table_text))
       
       return '\n\n'.join(tables)

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

       formatted_tables = self.extract_and_format_tables(soup)

       for element in soup(['script', 'style', 'meta', 'link', 'head']):
           element.decompose()

       text = soup.get_text(separator=' ')
       text = unicodedata.normalize('NFKD', text)
       text = re.sub(r'(<.*?>)'
                   r'|(&[a-zA-Z0-9#]+;)'
                   r'|[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}'
                   r'|^\s*[^a-zA-Z\s]*$'
                   r'|begin [0-9]{3} [^\n]+\n(.*\n)+?end'
                   r'|^[^\w\s]{10,}$'
                   r'|\s+',
                   ' ', 
                   text,
                   flags=re.MULTILINE)

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
