from typing import List, Tuple
from re import search

class LexicalAnalyzer:
    """ Classe responsável por prover métodos para realizar a análise léxica.
    """

    def __init__(self) -> None:
        """ Método construtor.
        """
        
        self.reserved_words: List[str] = [
            "variables", "const", "class", "methods","objects", "main", 
            "return", "if", "else", "then", "for", "read", "print", 
            "void", "int", "real", "boolean", "string", "true", "false"
        ]
        self.delimiters: List[str] = [
            ";", ",", ".", "(", ")", "[", "]", "{", "}",
            "+", "-", "*", "/",
            "=", "<", ">",
            "!", "\t", '"'
        ]
        self.tokens: List[str] = []
        self.errors_tokens: List[str] = []
        self.state: int = 0
        self.lexeme: str = ""
        self.line_index: int = 1
        self.flag_read_character: bool = True

    def generate_tokens(self, path: str, file_name: str) -> Tuple[List[str], List[str]] | None:
        """ Realiza a análise léxica de um determinado arquivo, e gera uma lista
        com os tokens correspondentes.

        Parameters
        ----------
        path: :class:`str`
            Caminho relativo do arquivo.
        file_name: :class:`str`
            Nome do arquivo.
        
        Returns
        -------
        content: :class:`List[str] | None`
        """

        with open(f"{path}/{file_name}.txt", "r") as file:
            eof: bool = False
            flag_character_error: bool = False
            flag_nmf_comment: bool = False
            flag_nmf_first_dot: bool = True
            double_delimiter: str = ""
            type: str = ""
            character: str = ""
            block_comment_start_line: int = 0

            self.__clean_lists__()
            self.__change_state__(clean_lexeme=True, flag=True, state=0)
            self.line_index = 1
            self.flag_read_character: bool = True

            while not eof:
                match self.state:
                    case 0: # Estado inicial
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "\n"):
                            self.line_index += 1

                        if (search(r'[^\w\d]|_', character)): # Símbolo
                            self.state = 1
                        elif (search(r'\d', character)):  # Dígito
                            self.lexeme += character
                            self.state = 2
                        elif (search(r'[a-zA-Z]', character)): # Letra
                            self.lexeme += character
                            self.state = 3
                        elif (character == ""):
                            pass # Sair do switch-case quando encontra o final do arquivo
                        else:
                            print(f"Error It's not a symbol. In {file_name} file line: {self.line_index}")
                            self.lexeme += character
                            self.__change_state__(clean_lexeme=False, flag=True, state=27)

                        self.flag_read_character = True
                    case 1: # Símbolo
                        self.lexeme += character
                        
                        if (character == '+'):
                            type = "ART"
                            self.state = 4
                        elif (character == '-'):
                            type = "ART"
                            self.state = 5
                        elif (character == '*'):
                            type = "ART"
                            self.state = 6
                        elif (character == '/'):
                            type = "ART"
                            self.state = 7
                        elif (character == '!'):
                            type = "LOG"
                            self.state = 8
                        elif (character == '='):
                            type = "REL"
                            self.state = 9
                        elif (character == '<'):
                            type = "REL"
                            self.state = 10
                        elif (character == '>'):
                            type = "REL"
                            self.state = 11
                        elif (character == '&'):
                            type = "LOG"
                            self.state = 12
                        elif (character == '|'):
                            type = "LOG"
                            self.state = 13
                        elif (character == ';'):
                            type = "DEL"
                            self.state = 14
                        elif (character == ','):
                            type = "DEL"
                            self.state = 15
                        elif (character == '.'):
                            type = "DEL"
                            self.state = 16
                        elif (character == '('):
                            type = "DEL"
                            self.state = 17
                        elif (character == ')'):
                            type = "DEL"
                            self.state = 18
                        elif (character == '['):
                            type = "DEL"
                            self.state = 19
                        elif (character == ']'):
                            type = "DEL"
                            self.state = 20
                        elif (character == '{'):
                            type = "DEL"
                            self.state = 21
                        elif (character == '}'):
                            type = "DEL"
                            self.state = 22
                        elif (character == '"'):
                            type = "CAC"
                            self.state = 23
                        else:
                            if (character == "\n" or character == "\t"):
                                self.__change_state__(clean_lexeme=True, flag=True, state=0)
                            elif (character == " "):
                                if (self.lexeme != " "):
                                    self.__add_token__(type)
                                
                                self.__change_state__(
                                    clean_lexeme = True, 
                                    flag = True, 
                                    state = 0
                                )
                            else:
                                print(f"Error Not a known symbol. In {file_name} file line: {self.line_index}")
                                self.__change_state__(
                                    clean_lexeme = False, 
                                    flag = True, 
                                    state = 27
                                )
                    case 2: # Número inteiro
                        if (self.flag_read_character): character = file.read(1)

                        if (search(r'\d', character)):  # Dígito
                            type = "NRO"
                            self.lexeme += character
                            self.state = 2
                        elif (character == "."):
                            if (type == "NMF"):
                                self.state = 2
                                flag_nmf_comment = True
                            else:
                                type = "NRO"
                                self.state = 26

                            self.lexeme += character
                        elif (character == "&" or character == "|"):
                            type = "NMF"
                            double_delimiter += character
                            self.lexeme += character

                            if (len(double_delimiter) == 2):
                                if (double_delimiter == "&&" or 
                                    double_delimiter == "||"
                                ):
                                    type = "NRO"

                                    # Removendo delimitador duplo do lexema.
                                    self.lexeme = self.lexeme[:len(self.lexeme) - 2]

                                    if (not search(r'\d', self.lexeme)):
                                        self.__add_error_token__("NMF")
                                    else:
                                        self.__add_token__(type)
                                    
                                    # Gera o token do delimitador duplo
                                    self.tokens.append(
                                        f"{self.line_index} <LOG, {double_delimiter}>"
                                    )

                                    double_delimiter = ""
                                    self.__change_state__(
                                        clean_lexeme = True, 
                                        flag = True, 
                                        state = 0
                                    )
                                else:
                                    type = "NMF"
                                    double_delimiter = ""
                                    self.state = 26
                            else:
                                self.state = 2
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            if (flag_nmf_comment):
                                self.__add_error_token__("NMF")
                                flag_nmf_comment = False
                            else:
                                if (self.lexeme != " "):
                                    self.__add_token__("NRO")
                            
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            print(f"Error NMF. In {file_name} file line: {self.line_index}")
                            type = "NMF"
                            flag_nmf_comment = True
                            self.lexeme += character
                            self.__change_state__(
                                clean_lexeme = False, 
                                flag = True, 
                                state = 2
                            )
                    case 3: # Letra
                        if (self.flag_read_character): character = file.read(1)

                        if (
                            search(r'\d', character) or
                            character == "_"
                        ):
                            type = "IDE"
                            self.lexeme += character
                            self.state = 3
                        elif (search(r'[a-zA-Z]', character)):
                            type = "PRE"
                            self.lexeme += character
                            self.state = 3
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            if (self.lexeme in self.reserved_words):
                                if (flag_character_error):
                                    self.__add_error_token__("TMF")
                                    flag_character_error = False
                                else:
                                    self.__add_token__(type)

                            else:
                                if (flag_character_error):
                                    self.__add_error_token__("IMF")
                                    flag_character_error = False
                                else:
                                    self.__add_token__("IDE")

                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            if (type == "IDE"):
                                print(f"Error IMF. In {file_name} file line: {self.line_index}")
                            else:
                                print(f"Error TMF. In {file_name} file line: {self.line_index}")

                            flag_character_error = True
                            self.lexeme += character
                            self.__change_state__(
                                clean_lexeme = False, 
                                flag = True, 
                                state = 3
                            )
                    case 4:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == '+'):
                            type = "ART"
                            self.lexeme += character
                            self.__add_token__(type)
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        else:
                            self.__add_token__(type)
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                    case 5:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "-"):
                            self.lexeme += character
                            self.__add_token__("ART")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        elif (character == ">"):
                            self.lexeme += character
                            self.__add_token__("DEL")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        else:
                            self.__add_token__(type)
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                    case 6:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "/"):
                            self.lexeme += character
                            self.__add_token__("COM")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        else:
                            self.__add_token__(type)
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                    case 7:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "*"):
                            block_comment_start_line = self.line_index
                            self.lexeme += character
                            
                            if (flag_nmf_comment):
                                self.__add_error_token__(
                                    type = "NMF", 
                                    lexeme = self.lexeme[:len(self.lexeme) - 2] # Removendo o '/' do lexema, para gerar o token de erro
                                )
                                self.lexeme = self.lexeme.split(".")[1]
                                flag_nmf_comment = False

                            type = "COM"
                            self.state = 24
                        elif (character == "/"):
                            self.lexeme += character

                            if (flag_nmf_comment):
                                self.__add_error_token__(
                                    type = "NMF", 
                                    lexeme = self.lexeme[:len(self.lexeme) - 2] # Removendo o '/' do lexema, para gerar o token de erro
                                )
                                self.lexeme = self.lexeme.split(".")[1]
                                flag_nmf_comment = False

                            type = "COM"
                            self.state = 25
                        else:
                            if (flag_nmf_comment):
                                flag_nmf_comment = False
                                self.__change_state__(
                                    clean_lexeme = False, 
                                    flag = False, 
                                    state = 26
                                )
                            else:
                                self.__add_token__(type)
                                self.__change_state__(
                                    clean_lexeme = True, 
                                    flag = False, 
                                    state = 0
                                )
                    case 8 | 9 | 10 | 11:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "="):
                            self.lexeme += character
                            self.__add_token__("REL")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        else:
                            self.__add_token__(type)
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                    case 12:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "&"):
                            self.lexeme += character
                            self.__add_token__("LOG")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            self.__add_error_token__("TMF")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            print(f"Error TMF. In {file_name} file line: {self.line_index}")
                            self.lexeme += character
                            self.state = 27
                    case 13:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "|"):
                            self.lexeme += character
                            self.__add_token__("LOG")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            self.__add_error_token__("TMF")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            print(f"Error TMF. In {file_name} file line: {self.line_index}")
                            self.lexeme += character
                            self.state = 27
                    case 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22:
                        self.__add_token__(type)
                        self.__change_state__(
                            clean_lexeme = True, 
                            flag = True, 
                            state = 0
                        )
                    case 23:
                        if (self.flag_read_character): character = file.read(1)
                        
                        if (character == '"'):
                            self.lexeme += character

                            if (flag_character_error):
                                self.__add_error_token__("CMF")
                                flag_character_error = False
                            else:
                                self.__add_token__(type)

                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = True, 
                                state = 0
                            )
                        elif (character == '\n' or character == ""):
                            print(f"Error CMF. In {file_name} file line: {self.line_index}")
                            self.__add_error_token__("CMF")
                            flag_character_error = False
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) # Letra
                        ): 
                            type = "CAC"
                            self.state = 23
                            self.lexeme += character
                        else:
                            print(f"Error CMF. In {file_name} file line: {self.line_index}")
                            flag_character_error = True
                            self.state = 23
                            self.lexeme += character
                    case 24:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "*"):
                            self.lexeme += character
                            character = file.read(1)
                            
                            if (character != "\n" and character != "\t"):
                                self.lexeme += character
                            
                            if (character == "\n"):
                                self.line_index += 1
                            
                            if (character == "/"):
                                type = "COM"
                                self.__change_state__(
                                    clean_lexeme = True, 
                                    flag = True, 
                                    state = 0
                                )
                            else:
                                type = "COM"
                                self.state = 24
                        elif (character == "\n"):
                            self.state = 24
                            self.line_index += 1
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) or # Letra
                            search(r'[À-ÖØ-öø-ÿ]', character) # Letra com acentuação
                        ): 
                            type = "COM"
                            self.state = 24
                            self.lexeme += character
                        else:
                            if (flag_nmf_comment):
                                flag_nmf_comment = False
                                self.__change_state__(
                                    clean_lexeme = False, 
                                    flag = False, 
                                    state = 26
                                )
                            else:
                                if (block_comment_start_line < self.line_index):
                                    print(f"Error CoMF. In {file_name} file line: [{block_comment_start_line}-{self.line_index}]")
                                    self.__add_error_token__("CoMF", block_comment_start_line)
                                else:
                                    print(f"Error CoMF. In {file_name} file line: {self.line_index}")
                                    self.__add_error_token__("CoMF")
                                
                                self.__change_state__(
                                    clean_lexeme = True, 
                                    flag = True, 
                                    state = 0
                                )
                    case 25:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == '\n' or character == ""):
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) or # Letra
                            search(r'[À-ÖØ-öø-ÿ]', character) # Letra com acentuação
                        ): 
                            type = "COM"
                            self.lexeme += character
                            self.state = 25
                        else:
                            if (flag_nmf_comment):
                                flag_nmf_comment = False
                                self.__change_state__(
                                    clean_lexeme = False, 
                                    flag = False, 
                                    state = 26
                                )
                            else:
                                print(f"Error CoMF. In {file_name} file line: {self.line_index}")
                                self.__add_error_token__("CoMF")
                                self.__change_state__(
                                    clean_lexeme = True, 
                                    flag = True, 
                                    state = 0
                                )
                    case 26:
                        type = "NRO"
                        
                        if (self.flag_read_character): character = file.read(1)

                        if (search(r'\d', character)): # Dígito
                            self.lexeme += character
                            self.state = 26
                        elif (character == "."):
                            self.lexeme += character
                            self.state = 26
                            flag_nmf_first_dot = False
                        elif (character == "&" or character == "|"):
                            double_delimiter += character
                            self.lexeme += character

                            if (len(double_delimiter) == 2):
                                if (double_delimiter == "&&" or 
                                    double_delimiter == "||"
                                ):
                                    # Removendo delimitador duplo do lexema.
                                    self.lexeme = self.lexeme[:len(self.lexeme) - 2]

                                    if (not search(r'^-?\d+(?:\.\d+)$', self.lexeme)):
                                        self.__add_error_token__("NMF")
                                    else:
                                        self.__add_token__(type)
                                    
                                    # Gera o token do delimitador duplo
                                    self.tokens.append(
                                        f"{self.line_index} <LOG, {double_delimiter}>"
                                    )

                                    double_delimiter = ""
                                    self.__change_state__(
                                        clean_lexeme = True, 
                                        flag = True, 
                                        state = 0
                                    )
                                else:
                                    double_delimiter = ""
                                    self.state = 26
                            else:
                                self.state = 26
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            # Se for delimitador após ponto
                            if (flag_nmf_first_dot and character in self.delimiters):
                                if (self.lexeme[-1] == "."):
                                    if (character == "/"):
                                        flag_nmf_comment = True
                                        self.state = 7
                                        self.lexeme += character
                                    else:
                                        self.state = 26
                                        self.lexeme += character
                                    
                                    flag_nmf_first_dot = True
                                    continue
                                
                            if (
                                not search(r'^-?\d+(?:\.\d+)$', self.lexeme) or 
                                not flag_nmf_first_dot
                            ):
                                print(f"Error NMF. In {file_name} file line: {self.line_index}")
                                self.__add_error_token__("NMF")
                            else:
                                if (self.lexeme != " "):
                                    self.__add_token__(type)
                            
                            double_delimiter = ""
                            flag_nmf_first_dot = True
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            self.state = 26
                            self.lexeme += character
                    case 27:
                        if (self.flag_read_character): character = file.read(1)

                        if (character == "&" or character == "|"):
                            double_delimiter += character
                            self.lexeme += character

                            if (len(double_delimiter) == 2):
                                if (double_delimiter == "&&" or 
                                    double_delimiter == "||"
                                ):
                                    # Removendo delimitador duplo do lexema.
                                    self.lexeme = self.lexeme[:len(self.lexeme) - 2]
                                    self.__add_error_token__("TMF")
                                    
                                    # Gera o token do delimitador duplo
                                    self.tokens.append(
                                        f"{self.line_index} <LOG, {double_delimiter}>"
                                    )

                                    double_delimiter = ""
                                    self.__change_state__(
                                        clean_lexeme = True, 
                                        flag = True, 
                                        state = 0
                                    )
                                else:
                                    self.state = 27
                                    double_delimiter = ""
                            else:
                                self.state = 27
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in self.delimiters
                        ):
                            self.__add_error_token__("TMF")
                            self.__change_state__(
                                clean_lexeme = True, 
                                flag = False, 
                                state = 0
                            )
                        else:
                            self.lexeme += character
                    case _:
                        print(f"Error default case. In {file_name} file line: {self.line_index}")
                
                if (character == ""):
                    eof = True

        return (self.tokens, self.errors_tokens)
    
    def __add_token__(self, type: str) -> None:
        """ Adicionar um token na lista de tokens.

        Parameters
        ----------
        type: :class:`str`
            Tipo do token. [PRE, IDE, CAC, NRO, DEL, REL, LOG, ART]
        """

        self.tokens.append(f"{self.line_index} <{type}, {self.lexeme}>")

    def __add_error_token__(
        self, 
        type: str, 
        block_comment_start_line: int = -1, 
        lexeme: str | None = None
    ) -> None:
        """ Adicionar um token de erro na lista de tokens de erro.

        Parameters
        ----------
        type: :class:`str`
            Tipo do token. [CMF, CoMF, NMF, IMF, TMF]
        block_comment_start_line :class:`int`
            Linha em que começa o comentário de bloco, caso possua mais de uma
            linha. Por padrão inicia como `-1`, ou seja, somente uma linha.
        lexeme :class:`str | None`
            Lexema que será adicionado na lista, caso seja diferente do 
            atributo. Por padrão é `None`, ou seja, utiliza o valor do atributo.
        """

        if (not lexeme):
            lexeme = self.lexeme

        if (block_comment_start_line > 0):
            self.errors_tokens.append(
                f"[{block_comment_start_line}-{self.line_index}] <{type}, {lexeme}>"
            )
        else:
            self.errors_tokens.append(f"{self.line_index} <{type}, {lexeme}>")

    def __change_state__(
        self, 
        clean_lexeme: bool, 
        flag: bool, 
        state: int = -1
    ) -> None:
        """ Altera o estado do autômato finito, podendo modificar ou não o 
        lexema analisado.

        Parameters
        ----------
        clean_lexeme: :class:`bool`
            Limpar ou não o lexema.
        flag: :class:`bool`
            Ler ou não o próximo caractere.
        state: :class:`int `
            Estado para o qual será mudado. Por padrão é `-1`, indicando que não
            ocorrerá a mudança de estado.
        """

        if (clean_lexeme):
            self.lexeme = ""

        if (state >= 0):
            self.state = state

        self.flag_read_character = flag
    
    def __clean_lists__(self) -> None:
        """ Limpa todas as listas de tokens.
        """
        
        self.tokens = []
        self.errors_tokens = ["\nERROS:"]