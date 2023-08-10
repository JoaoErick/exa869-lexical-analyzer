from os import listdir
from re import search
from typing import List

class FileHandler:
    """ Classe para lidar com as operações de arquivos de texto.

    Parameters
    ----------
    path: :class:`str`
        Caminho relativo dos arquivos de texto.
    """

    def __init__(self, path: str):
        """ Método construtor.
        """

        self.path = path
        self.file_queue = []
    
    def get_filenames(self) -> None:
        """ Faz a leitura dos nomes de todos os arquivos de entrada.
        """
        
        for filename in listdir(self.path):
            if search(r'^(?!.*-saida).*\.txt', filename):
                self.file_queue.append(filename.split(".")[0])

    def read_file(self) -> List[str] | None:
        """ Realiza a leitura do conteúdo de um arquivo .txt presente na fila 
        e o retorna.
        
        Returns
        -------
        content: :class:`List[str] | None`
        """

        if len(self.file_queue) > 0:
            content = []
            with open(f"{self.path}/{self.file_queue[0]}.txt", "r") as file:
                while True:
                    character = file.read(1)
                    if not character:
                        break
                    content.append(character)
            return content
        return None

    def write_file(self, content: List[str]) -> None:
        """ Realiza a escrita de uma lista de caracteres em um arquivo .txt.

        O arquivo de saída possuirá o mesmo nome do arquivo de entrada com o 
        sufixo "-saida".

        Parameters
        ----------
        content: :class:`List[str]`
            Lista de caracteres
        """
        with open(f"{self.path}/{self.file_queue[0]}-saida.txt", "w") as file:
            for index, character in enumerate(content):
                file.write(character)
                if index < len(content) - 1:
                    file.write("\n")