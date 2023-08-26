# Analisador Léxico

<p align="center">
  <img src="./images/lexical-analyzer-icon.png" alt="Lexical Analyzer Icon" width="250px" height="250px">
</p>

## :books: Descrição ##
Analisador léxico construído como forma de avaliação para a disciplina EXA869 MI - Processadores de Linguagem de Programação.

### :computer: Tecnologias
- [Python 3.10+](https://www.python.org/)

### Tabela da estrutura léxica da linguagem
<table>
    <tbody>
        <tr>
            <td>
                Palavras Reservadas
            </td>
            <td>
                variables, const, class, methods,
                objects, main, return, if, else, then,
                for, read, print, void, int, real,
                boolean, string, true, false
            </td>
        </tr>
        <tr>
            <td>
                Identificadores
            </td>
            <td>
                letra ( letra | dígito | _ )*
            </td>
        </tr>
        <tr>
            <td>
                Números
            </td>
            <td>
                dígito<sup>+</sup>(. dígito ( dígito )*)?
            </td>
        </tr>
        <tr>
            <td>
                Dígito
            </td>
            <td>
                [0-9]
            </td>
        </tr>
        <tr>
            <td>
                Letra
            </td>
            <td>
                [a-z] | [A-Z]
            </td>
        </tr>
        <tr>
            <td>
                Operadores Aritméticos
            </td>
            <td>
                + - * / ++ --
            </td>
        </tr>
        <tr>
            <td>
                Operadores Relacionais
            </td>
            <td>
                != == < <= > >= =
            </td>
        </tr>
        <tr>
            <td>
                Operadores Lógicos
            </td>
            <td>
                ! && ||
            </td>
        </tr>
        <tr>
            <td>
                Comentários
            </td>
            <td>
                // isto é um comentário de linha
                <br>
                /* isto
                <br> 
                é um comentário de
                <br>
                bloco */
            </td>
        </tr>
        <tr>
            <td>
                Delimitadores
            </td>
            <td>
                ; , . ( ) [ ] { } ->
            </td>
        </tr>
        <tr>
            <td>
                Cadeia de Caracteres
            </td>
            <td>
                " ( letra | dígito | símbolo )* "
            </td>
        </tr>
        <tr>
            <td>
                Símbolo
            </td>
            <td>
                ASCII de 32 a 126 (exceto ASCII 34)
            </td>
        </tr>
    </tbody>
</table>

## Como usar
1. Clonar este repositório;
2. Garanta que existe a versão 3.10+ do python instalada na sua máquina;
3. Coloque um ou mais arquivos de entrada `.txt` no diretório `src/files`;
4. Execute o projeto utilizando o comando:
    ```python
    python src/main.py
    ```
5. Os arquivos de saída estarão armazenados no diretório `src/files`.

## :pushpin: Autores ##
- Allan Capistrano: [Github](https://github.com/AllanCapistrano) - [Linkedin](https://www.linkedin.com/in/allancapistrano/) - [E-mail](https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1&source=mailto&to=asantos@ecomp.uefs.br)
- João Erick Barbosa: [Github](https://github.com/JoaoErick) - [Linkedin](https://www.linkedin.com/in/joão-erick-barbosa-9050801b0/) - [E-mail](https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1&source=mailto&to=jsilva@ecomp.uefs.br)

------------

## :balance_scale: Licença ##
[MIT License](./LICENSE)