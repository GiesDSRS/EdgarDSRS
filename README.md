# EDGARTOOL: Tool for SEC 10-k files
## Description:

EDGARTOOL is a Python library designed to clean and process SEC EDGAR 10-K filing HTML files. It removes unnecessary HTML elements, tables with high numeric content, and various types of noise/gibberish text to produce clean, readable text output suitable for analysis.

## Features

- HTML cleaning and text extraction
- Removal of financial tables and numeric-heavy content
- Elimination of noisy text and gibberish
- Unicode normalization
- Special character handling
- Multiple HTML parser support (html.parser, lxml, html5lib)

## Installation

```bash
pip install edgaranalyzer
```

Required dependencies:
- beautifulsoup4
- lxml
- html5lib
- unicodedata
- xml.etree.ElementTree

## Usage

Basic usage to clean a 10-K HTML file:

```python
from edgartool import EdgarAnalyzer

analyzer = EdgarAnalyzer()

# Cleaning the file
input_file = "your_10k_file.html"
cleaned_file = analyzer.process_html_file(input_file)
```

## Cleaning Process

The tool performs the following cleaning operations:

1. **HTML Parsing**: Attempts to parse HTML using multiple parsers (html.parser, lxml, html5lib)
2. **Tag Removal**: Strips all HTML tags while preserving text content
3. **Unicode Normalization**: Normalizes Unicode characters
4. **Noise Removal**:
   - Removes sequences with high special character density
   - Eliminates base64 encoded patterns
   - Cleans up lines with excessive non-alphanumeric characters
5. **Text Cleaning**:
   - Removes noisy words (mixed case with numbers, excessive length)
   - Normalizes whitespace

## Functions

### `clean_html_content(html_content)`
Main function to clean HTML content and extract text.

```python
text = EdgarAnalyzer.clean_html_content(html_content)
```

### `clean_noisy_text(text)`
Removes noisy text patterns and standardizes format.

### `remove_gibberish(text)`
Eliminates gibberish and unwanted patterns from text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Pratik Relekar | Xinyao Qian


## Disclaimer
