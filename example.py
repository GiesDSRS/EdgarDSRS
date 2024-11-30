from edgartool import EdgarAnalyzer

def main():
    analyzer = EdgarAnalyzer()
    input_file = "path/to/your/10k_file.html"
    output_dir = "./cleaned_output"
    cleaned_file = analyzer.process_html_file(input_file, output_dir)
    if cleaned_file:
        print(f"Successfully cleaned file. Output saved to: {cleaned_file}")

if __name__ == "__main__":
    main()
