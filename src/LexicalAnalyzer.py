from typing import List
from re import search

class LexicalAnalyzer:

    def generate_tokens(self, path: str, file_name: str) -> List[str] | None:
        """ Realiza a leitura do conteúdo de um arquivo .txt presente na fila 
        e o retorna.

        Parameters
        ----------
        # TODO: colocar parâmetros
        
        Returns
        -------
        content: :class:`List[str] | None`
        """

        with open(f"{path}/{file_name}.txt", "r") as file:
            eof: bool = False
            flag: bool = True
            flag_dot_error: bool = False
            state: int = 0
            lexeme: str = ""
            type: str = ""
            tokens: List[str] = []
            character: str = ""
            line_index: str = 1
            reserved_words: List[str] = [
                "variables", "const", "class", "methods","objects", "main", 
                "return", "if", "else", "then", "for", "read", "print", 
                "void", "int", "real", "boolean", "string", "true", "false"
            ]
            delimiters: List[str] = [
                ";", ",", ".", "(", ")", "[", "]", "{", "}",
                "+", "-", "*", "/",
                "=", "<", ">",
                "!", "&", "|",
                "\t"
            ]

            while not eof:
                match state:
                    case 0: # Estado inicial
                        if (flag): character = file.read(1)

                        if (character == "\n"):
                            line_index += 1

                        if (search(r'[^\w\d]|_', character)): # Símbolo
                            state = 1
                        elif (search(r'\d', character)):  # Dígito
                            lexeme += character
                            state = 2
                        elif (search(r'[a-zA-Z]', character)): # Letra
                            lexeme += character
                            state = 3
                        elif (character == ""):
                            pass # TODO: Ver se não tem um jeito melhor
                        else:
                            print(f"Error! It's not a symbol. In {file_name} file line: {line_index}")

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
                            if (character == "\n" or character == "\t"):
                                state = 0
                                lexeme = ""
                            elif (character == " "):
                                state = 0
                                
                                if (lexeme != " "):
                                    tokens.append(f"{line_index} <{type}, {lexeme}>")
                                
                                lexeme = ""
                                flag = True
                            else:
                                print(f"Error! Not a known symbol. In {file_name} file line: {line_index}")
                    case 2:
                        type = "NRO"

                        if (flag): character = file.read(1)

                        if (search(r'\d', character)):  # Dígito
                            lexeme += character
                            state = 2
                        elif (character == "."):
                            type = "NRO"
                            lexeme += character
                            state = 26
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            if (lexeme != " "):
                                tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                            
                            state = 0
                            lexeme = ""
                            flag = False
                        else:
                            print(f"Error NMF. In {file_name} file line: {line_index}")
                            state = 0
                            lexeme = ""
                            flag = True
                    case 3:
                        if (flag): character = file.read(1)

                        if (
                            search(r'\d', character) or
                            character == "_"
                        ):
                            type = "IDE"
                            lexeme += character
                            state = 3
                        elif (search(r'[a-zA-Z]', character)):
                            type = "PRE"
                            lexeme += character
                            state = 3
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            flag = False

                            if (lexeme in reserved_words):
                                tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                                state = 0
                                lexeme = ""
                            else:
                                type = "IDE"
                                tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                                state = 0
                                lexeme = ""
                        else:
                            if (type == "IDE"):
                                print(f"Error IMF. In {file_name} file line: {line_index}")
                            else:
                                print(f"Error TMF. In {file_name} file line: {line_index}")
                            state = 0
                            flag = True
                            lexeme = ""
                    case 4:
                        if (flag): character = file.read(1)

                        if (character == '+'):
                            type = "ART"
                            lexeme += character
                        else:
                            flag = False
                            
                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 5:
                        if (flag): character = file.read(1)

                        if (character == "-"):
                            type = "ART"
                            lexeme += character
                        elif (character == ">"):
                            type = "DEL"
                            lexeme += character
                        else:
                            flag = False

                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 6:
                        if (flag): character = file.read(1)

                        if (character == "/"):
                            type = "COM"
                            lexeme += character
                        else:
                            flag = False

                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 7:
                        if (flag): character = file.read(1)

                        if (character == "*"):
                            type = "COM"
                            lexeme += character
                            state = 24
                        elif (character == "/"):
                            type = "COM"
                            lexeme += character
                            state = 25
                        else:
                            flag = False
                            state = 0
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            lexeme = ""
                    case 8 | 9 | 10 | 11:
                        if (flag): character = file.read(1)

                        if (character == "="):
                            type = "REL"
                            lexeme += character
                        else:
                            flag = False

                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 12:
                        if (flag): character = file.read(1)

                        if (character == "&"):
                            type = "LOG"
                            lexeme += character
                        else:
                            print(f"Error TMF. In {file_name} file line: {line_index}")

                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 13:
                        if (flag): character = file.read(1)

                        if (character == "|"):
                            type = "LOG"
                            lexeme += character
                        else:
                            print(f"Error TMF. In {file_name} file line: {line_index}")

                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22:
                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 23:
                        if (flag): character = file.read(1)
                        
                        if (character == '"'):
                            state = 0
                            lexeme += character
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            lexeme = ""
                        elif (character == '\n' or character == ""):
                            print(f"Error CMF. In {file_name} file line: {line_index}")
                            state = 0
                            lexeme = ""
                            flag = False
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) # Letra
                        ): 
                            type = "CAC"
                            lexeme += character
                            state = 23
                        else:
                            print(f"Error CMF. In {file_name} file line: {line_index}")
                    case 24:
                        if (flag): character = file.read(1)

                        if (character == "*"):
                            lexeme += character
                            character = file.read(1)
                            lexeme += character
                            
                            if (character == "/"):
                                type = "COM"
                                # tokens.append(f"{line_index} <{type}, {lexeme}>") # TODO: Apagar
                                lexeme = ""
                                state = 0
                            else:
                                type = "COM"
                                state = 24
                        elif (character == "\n"):
                            line_index += 1
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) or # Letra
                            search(r'[À-ÖØ-öø-ÿ]', character) # Letras com acentuação
                        ): 
                            type = "COM"
                            lexeme += character
                            state = 24
                        else:
                            print(f"Error CoMF. In {file_name} file line: {line_index}")
                    case 25:
                        if (flag): character = file.read(1)

                        if (character == '\n' or character == ""):
                            # tokens.append(f"{line_index} <{type}, {lexeme}>") # TODO: Apagar
                            flag = False
                            lexeme = ""
                            state = 0
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) or # Letra
                            search(r'[À-ÖØ-öø-ÿ]', character) # Letras com acentuação
                        ): 
                            type = "COM"
                            lexeme += character
                            state = 25
                        else:
                            print(f"Error CoMF. In {file_name} file line: {line_index}")
                    case 26:
                        type = "NRO"
                        
                        if (flag): character = file.read(1)

                        if (search(r'\d', character)):  # Dígito
                            lexeme += character
                            state = 26
                        elif (character == "."):
                            flag_dot_error = True
                            state = 26
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            if (flag_dot_error):
                                print(f"Error NMF. In {file_name} file line: {line_index}")
                                state = 0
                                lexeme = ""
                                flag_dot_error = False
                            else:
                                if (lexeme != " "):
                                    tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                                
                                state = 0   
                                lexeme = ""
                                flag = False
                    case _:
                        print(f"Error default case. In {file_name} file line: {line_index}")
                
                if (character == ""):
                    eof = True

        return tokens