from typing import List
from util import FileHandler
from pathlib import Path
from LexicalAnalyzer import LexicalAnalyzer

def main():
    current_directory: Path = Path(__file__).parent.resolve()
    path: str = f"{current_directory}/files/"

    file_handler: FileHandler = FileHandler(path)
    lexical_analyzer: LexicalAnalyzer = LexicalAnalyzer()

    for file_name in file_handler.get_file_names():
        tokens, errors_tokens = lexical_analyzer.generate_tokens(path, file_name)
        file_handler.write_file(file_name, tokens,)
        if (len(errors_tokens) > 1):
            file_handler.write_file(file_name, errors_tokens, write_mode="a+")

if __name__ == "__main__":
    main()