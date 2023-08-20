from typing import List, Tuple
from re import search

class LexicalAnalyzer:
    """ Classe responsável por prover métodos para realizar a análise léxica.
    """

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
            flag: bool = True
            flag_character_error: bool = False
            flag_nmf_comment: bool = False # TODO: Ver se n tem um nome melhor
            flag_nmf_first_dot: bool = True # TODO: Ver se n tem um nome melhor
            state: int = 0
            lexeme: str = ""
            double_delimiter: str = ""
            type: str = ""
            tokens: List[str] = []
            errors_tokens: List[str] = ["\n"]
            character: str = ""
            line_index: int = 1
            block_comment_start_line: int = 0
            reserved_words: List[str] = [
                "variables", "const", "class", "methods","objects", "main", 
                "return", "if", "else", "then", "for", "read", "print", 
                "void", "int", "real", "boolean", "string", "true", "false"
            ]
            delimiters: List[str] = [
                ";", ",", ".", "(", ")", "[", "]", "{", "}",
                "+", "-", "*", "/",
                "=", "<", ">",
                "!", "\t", '"'
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
                            print(f"Error It's not a symbol. In {file_name} file line: {line_index}")
                            state = 27
                            lexeme += character
                            flag = True

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
                                print(f"Error Not a known symbol. In {file_name} file line: {line_index}")
                                state = 27
                                flag = True
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
                            if (flag_nmf_comment):
                                type = "NMF"
                                errors_tokens.append(f"{line_index} <{type}, {lexeme}>")
                                flag_nmf_comment = False
                            else:
                                if (lexeme != " "):
                                    tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                            
                            state = 0
                            lexeme = ""
                            flag = False
                        else:
                            print(f"Error NMF. In {file_name} file line: {line_index}")
                            flag_nmf_comment = True
                            state = 2
                            lexeme += character
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
                                if (flag_character_error):
                                    type = "TMF"
                                    errors_tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                                    flag_character_error = False
                                else:
                                    tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )

                                state = 0
                                lexeme = ""
                            else:
                                if (flag_character_error):
                                    type = "IMF"
                                    errors_tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                                    flag_character_error = False
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

                            flag_character_error = True
                            state = 3
                            lexeme += character
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
                            block_comment_start_line = line_index
                            lexeme += character
                            
                            if (flag_nmf_comment):
                                # Removendo o '/' do lexema, para gerar o token de erro
                                type = "NMF"
                                errors_tokens.append(f"{line_index} <{type}, {lexeme[:len(lexeme) - 2]}>")
                                lexeme = lexeme.split(".")[1]
                                flag_nmf_comment = False

                            type = "COM"
                            state = 24
                        elif (character == "/"):
                            lexeme += character

                            if (flag_nmf_comment):
                                # Removendo o '/' do lexema, para gerar o token de erro
                                type = "NMF"
                                errors_tokens.append(f"{line_index} <{type}, {lexeme[:len(lexeme) - 2]}>")
                                lexeme = lexeme.split(".")[1]
                                flag_nmf_comment = False

                            type = "COM"
                            state = 25
                        else:
                            if (flag_nmf_comment):
                                state = 26
                                flag_nmf_comment = False
                                flag = False
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
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            state = 0
                            lexeme = ""
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            type = "TMF"
                            errors_tokens.append(f"{line_index} <{type}, {lexeme}>")
                            state = 0
                            lexeme = ""
                            flag = False
                        else:
                            print(f"Error TMF. In {file_name} file line: {line_index}")
                            lexeme += character
                            state = 27
                    case 13:
                        if (flag): character = file.read(1)

                        if (character == "|"):
                            type = "LOG"
                            lexeme += character
                            tokens.append(f"{line_index} <{type}, {lexeme}>")
                            state = 0    
                            lexeme = ""
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            type = "TMF"
                            errors_tokens.append(f"{line_index} <{type}, {lexeme}>")
                            state = 0
                            lexeme = ""
                            flag = False
                        else:
                            print(f"Error TMF. In {file_name} file line: {line_index}")
                            lexeme += character
                            state = 27

                    case 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22:
                        state = 0
                        tokens.append(f"{line_index} <{type}, {lexeme}>")
                        lexeme = ""
                    case 23:
                        if (flag): character = file.read(1)
                        
                        if (character == '"'):
                            lexeme += character

                            if (flag_character_error):
                                type = "TMF"
                                errors_tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                                flag_character_error = False
                            else:
                                tokens.append(f"{line_index} <{type}, {lexeme}>")

                            state = 0
                            lexeme = ""
                        elif (character == '\n' or character == ""):
                            print(f"Error CMF. In {file_name} file line: {line_index}")
                            type = "CMF"
                            errors_tokens.append(
                                f"{line_index} <{type}, {lexeme}>"
                            )
                            state = 0
                            lexeme = ""
                            flag = False
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) # Letra
                        ): 
                            type = "CAC"
                            state = 23
                            lexeme += character
                        else:
                            print(f"Error CMF. In {file_name} file line: {line_index}")
                            flag_character_error = True
                            state = 23
                            lexeme += character
                    case 24:
                        if (flag): character = file.read(1)

                        if (character == "*"):
                            lexeme += character
                            character = file.read(1)
                            lexeme += character
                            
                            if (character == "/"):
                                type = "COM"
                                lexeme = ""
                                state = 0
                            else:
                                type = "COM"
                                state = 24
                        elif (character == "\n"):
                            state = 24
                            line_index += 1
                        elif (
                            search(r'[^\w\d]|_', character) or # Símbolo
                            search(r'\d', character) or # Dígito
                            search(r'[a-zA-Z]', character) or # Letra
                            search(r'[À-ÖØ-öø-ÿ]', character) # Letras com acentuação
                        ): 
                            type = "COM"
                            state = 24
                            lexeme += character
                        else:
                            if (flag_nmf_comment):
                                state = 26
                                flag_nmf_comment = False
                                flag = False
                            else:
                                type = "CoMF"

                                if (block_comment_start_line < line_index):
                                    print(f"Error CoMF. In {file_name} file line: [{block_comment_start_line}-{line_index}]")
                                    errors_tokens.append(
                                        f"[{block_comment_start_line}-{line_index}] <{type}, {lexeme}>"
                                    )
                                else:
                                    print(f"Error CoMF. In {file_name} file line: {line_index}")
                                    errors_tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                                
                                state = 0
                                lexeme = ""
                                flag = True
                    case 25:
                        if (flag): character = file.read(1)

                        if (character == '\n' or character == ""):
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
                            if (flag_nmf_comment):
                                state = 26
                                flag_nmf_comment = False
                                flag = False
                            else:
                                print(f"Error CoMF. In {file_name} file line: {line_index}")
                                type = "CoMF"
                                errors_tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                                state = 0
                                lexeme = ""
                                flag = True
                    case 26:
                        type = "NRO"
                        
                        if (flag): character = file.read(1)

                        if (search(r'\d', character)):  # Dígito
                            lexeme += character
                            state = 26
                        elif (character == "."):
                            lexeme += character
                            state = 26
                            flag_nmf_first_dot = False
                        elif (character == "&" or character == "|"):
                            double_delimiter += character
                            lexeme += character

                            if (len(double_delimiter) == 2):
                                if (double_delimiter == "&&" or 
                                    double_delimiter == "||"
                                ):
                                    # Removendo delimitador duplo do lexema.
                                    lexeme = lexeme[:len(lexeme) - 2]

                                    if (not search(r'^-?\d+(?:\.\d+)$', lexeme)):
                                        type = "NMF"
                                        errors_tokens.append(
                                            f"{line_index} <{type}, {lexeme}>"
                                        )
                                    else:
                                        tokens.append(
                                            f"{line_index} <{type}, {lexeme}>"
                                        )
                                    
                                    # Gera o token do delimitador duplo
                                    tokens.append(
                                        f"{line_index} <LOG, {double_delimiter}>"
                                    )

                                    lexeme = ""
                                    double_delimiter = ""
                                    state = 0
                                    flag = True
                                else:
                                    state = 26
                                    double_delimiter = ""
                            else:
                                state = 26
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            # Se for delimitador após ponto
                            if (flag_nmf_first_dot and character in delimiters):
                                if (lexeme[-1] == "."):
                                    if (character == "/"):
                                        flag_nmf_comment = True
                                        state = 7
                                        lexeme += character
                                    else:
                                        state = 26
                                        lexeme += character
                                    
                                    flag_nmf_first_dot = True
                                    continue
                                
                            if (
                                not search(r'^-?\d+(?:\.\d+)$', lexeme) or 
                                not flag_nmf_first_dot
                            ):
                                print(f"Error NMF. In {file_name} file line: {line_index}")
                                
                                type = "NMF"
                                errors_tokens.append(
                                    f"{line_index} <{type}, {lexeme}>"
                                )
                            else:
                                if (lexeme != " "):
                                    tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                            
                            state = 0   
                            lexeme = ""
                            flag = False
                        else:
                            state = 26
                            lexeme += character
                    case 27:
                        if (flag): character = file.read(1)

                        if (character == "&" or character == "|"):
                            double_delimiter += character
                            lexeme += character

                            if (len(double_delimiter) == 2):
                                if (double_delimiter == "&&" or 
                                    double_delimiter == "||"
                                ):
                                    # Removendo delimitador duplo do lexema.
                                    lexeme = lexeme[:len(lexeme) - 2]

                                    type = "TMF"
                                    errors_tokens.append(
                                        f"{line_index} <{type}, {lexeme}>"
                                    )
                                    
                                    # Gera o token do delimitador duplo
                                    tokens.append(
                                        f"{line_index} <LOG, {double_delimiter}>"
                                    )

                                    lexeme = ""
                                    double_delimiter = ""
                                    state = 0
                                    flag = True
                                else:
                                    state = 27
                                    double_delimiter = ""
                            else:
                                state = 27
                        elif (
                            character == " " or 
                            character == "\n" or
                            character == "" or
                            character in delimiters
                        ):
                            type = "TMF"
                            errors_tokens.append(
                                f"{line_index} <{type}, {lexeme}>"
                            )
                            state = 0
                            lexeme = ""
                            flag = False
                        else:
                            lexeme += character
                    case _:
                        print(f"Error default case. In {file_name} file line: {line_index}")
                
                if (character == ""):
                    eof = True

        return (tokens, errors_tokens)