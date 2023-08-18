from typing import List
from util import FileHandler
from pathlib import Path
from LexicalAnalyzer import LexicalAnalyzer

def main():
    current_directory: Path = Path(__file__).parent.resolve()
    path: str = f"{current_directory}/files/"
    file_handler: FileHandler = FileHandler(path)
    lexical_analyzer: LexicalAnalyzer = LexicalAnalyzer()
    file_names: List[str] = file_handler.get_filenames()

    for file_name in file_names:
        tokens = lexical_analyzer.generate_tokens(path, file_name)
        file_handler.write_file(file_name, tokens)

if __name__ == "__main__":
    main()