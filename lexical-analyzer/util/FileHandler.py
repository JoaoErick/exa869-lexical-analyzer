from os import listdir
from re import search
from typing import List

class FileHandler:
    """ Classe para lidar com as operações de arquivos de texto.
    """

    def __init__(self, path: str):
        """ Método construtor.

        Parameters
        ----------
        path: :class:`str`
            Caminho relativo do(s) arquivo(s) de texto.
        """

        self.path = path
    
    def get_file_names(self) -> List[str]:
        """ Faz a leitura dos nomes de todos os arquivos de entrada.

        Returns
        -------
        List[str]
        """

        file_queue: List[str] = []
        
        for file_name in listdir(self.path):
            if search(r'^(?!.*-saida).*\.txt', file_name):
                file_queue.append(file_name.split(".")[0])

        return file_queue

    def write_file(
        self, 
        file_name: str, 
        content: List[str], 
        write_mode: str = "w"
    ) -> None:
        """ Realiza a escrita de uma lista de caracteres em um arquivo .txt.

        O arquivo de saída possuirá o mesmo nome do arquivo de entrada com o 
        sufixo "-saida".

        Parameters
        ----------
        file_name: :class:`str`
            Nome do arquivo.
        content: :class:`List[str]`
            Lista de caracteres
        write_mode: :class:`str`
            Modo de escrita do arquivo. Por padrão é utilizado o 'w'.
        """
        with open(f"{self.path}/{file_name}-saida.txt", write_mode) as file:
            for index, character in enumerate(content):
                file.write(character)
                if index < len(content) - 1:
                    file.write("\n")