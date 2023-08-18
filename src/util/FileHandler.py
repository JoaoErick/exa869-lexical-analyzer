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
    
    def get_filenames(self) -> List[str]:
        """ Faz a leitura dos nomes de todos os arquivos de entrada.

        Returns
        -------
        List[str]
        """

        file_queue: List[str] = []
        
        for filename in listdir(self.path):
            if search(r'^(?!.*-saida).*\.txt', filename):
                file_queue.append(filename.split(".")[0])

        return file_queue

    def write_file(self, file_name: str, content: List[str]) -> None:
        """ Realiza a escrita de uma lista de caracteres em um arquivo .txt.

        O arquivo de saída possuirá o mesmo nome do arquivo de entrada com o 
        sufixo "-saida".

        Parameters
        ----------
        content: :class:`List[str]`
            Lista de caracteres
        """
        with open(f"{self.path}/{file_name}-saida.txt", "w") as file:
            for index, character in enumerate(content):
                file.write(character)
                if index < len(content) - 1:
                    file.write("\n")