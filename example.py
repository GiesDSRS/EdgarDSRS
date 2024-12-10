from edgaranalyzer import EdgarAnalyzer

analyzer = EdgarAnalyzer()

# Cleaning the file
input_file = "your_10k_file.html"
cleaned_file = analyzer.process_html_file(input_file)
