from module import EdgarAnalyzer

def main():
    input_file = "C:\\Users\\xinya\\PhD\\DSRS\\library_10k\\1000180-SANDISK CORP-10-K-2007-02-28.txt"
    analyzer = EdgarAnalyzer()
    output_file = analyzer.process_html_file(input_file)
    if output_file:
        print("\nFirst 500 characters of cleaned text and tables:")
        with open(output_file, 'r', encoding='utf-8') as file:
            print(file.read()[:500])


if __name__ == "__main__":
    main()