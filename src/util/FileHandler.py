from os import listdir
from re import search
from typing import List
from re import search

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
            with open(f"{self.path}/{self.file_queue[0]}.txt", "r") as file:
                eof: bool = False
                flag: bool = True
                state: int = 0
                lexeme: str = ""
                type: str = ""
                tokens: List[str] = []
                character: str = ""
                line_index: str = 1

                while not eof:
                    match state:
                        case 0: # Estado inicial
                            if (flag): character = file.read(1)

                            if (character == "\n"):
                                line_index += 1

                            if (search(r'[^\w\d]', character)): # Símbolo
                                state = 1
                            elif (search(r'\d', character)):  # Dígito
                                state = 2
                            elif (search(r'[a-zA-Z]', character)): # Letra
                                state = 3
                            elif (character == ""):
                                pass # TODO: Ver se não tem um jeito melhor
                            else:
                                print("Error! It's not a symbol.")

                            flag = True
                            
                        case 1: # Símbolo
                            lexeme += character
                            
                            if (character == '+'):
                                type = "ART"
                                state = 4
                            elif (character == '-'):
                                type = "ART"
                                state = 5
                            elif (character == '*'):
                                type = "ART"
                                state = 6
                            elif (character == '/'):
                                type = "ART"
                                state = 7
                            elif (character == '!'):
                                type = "LOG"
                                state = 8
                            elif (character == '='):
                                type = "REL"
                                state = 9
                            elif (character == '<'):
                                type = "REL"
                                state = 10
                            elif (character == '>'):
                                type = "REL"
                                state = 11
                            elif (character == '&'):
                                type = "LOG"
                                state = 12
                            elif (character == '|'):
                                type = "LOG"
                                state = 13
                            elif (character == ';'):
                                type = "DEL"
                                state = 14
                            elif (character == ','):
                                type = "DEL"
                                state = 15
                            elif (character == '.'):
                                type = "DEL"
                                state = 16
                            elif (character == '('):
                                type = "DEL"
                                state = 17
                            elif (character == ')'):
                                type = "DEL"
                                state = 18
                            elif (character == '['):
                                type = "DEL"
                                state = 19
                            elif (character == ']'):
                                type = "DEL"
                                state = 20
                            elif (character == '{'):
                                type = "DEL"
                                state = 21
                            elif (character == '}'):
                                type = "DEL"
                                state = 22
                            elif (character == '"'):
                                type = "CAC"
                                state = 23
                            else:
                                if (character == "\n"):
                                    state = 0
                                    lexeme = ""
                                elif (character == " "):
                                    state = 0
                                    
                                    if (lexeme != " "):
                                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                                    
                                    lexeme = ""
                                    flag = True
                                else:
                                    print("Error")
                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            if (flag): character = file.read(1)

                            if (character == '+'):
                                type = "ART"
                                lexeme += character
                                state = 24
                            else:
                                state = 0
                                tokens.append(f"{line_index} <{type}, {lexeme}>")
                                lexeme = ""
                                flag = False
                        case 5:
                            if (flag): character = file.read(1)

                            if(character == "-"):
                                type = "ART"
                                lexeme += character
                                state = 25
                            elif(character == ">"):
                                type = "DEL"
                                lexeme += character
                                state = 26
                            else:
                                state = 0
                                tokens.append(f"{line_index} <{type}, {lexeme}>")
                                lexeme = ""
                                flag = False
                        case 24:
                            # TODO  função generate_token
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            lexeme = ""
                            state = 0

                        case 25:
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            lexeme = ""
                            state = 0

                        case 26:
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            lexeme = ""
                            state = 0
                        case _:
                            print("Error cases")
                    
                    if (character == ""):
                        eof = True

            return tokens

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