from util import FileHandler
from pathlib import Path

def main():
    current_directory = Path(__file__).parent.resolve()
    file_handler = FileHandler(path=f"{current_directory}/files/")
    file_handler.get_filenames()

    content = []

    while len(file_handler.file_queue) > 0:
        content = file_handler.read_file()
        if content:
            file_handler.write_file(content=content)
            file_handler.file_queue.pop(0)

if __name__ == "__main__":
    main()