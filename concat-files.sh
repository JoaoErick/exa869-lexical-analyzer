#!/bin/bash
files_folder="./src/files"

# Removendo o arquivo mesclado anterior.
rm "$files_folder/merged.txt"

# Criando um novo arquivo que será mesclado.
touch "$files_folder/merged.txt"

# Removendo os arquivos de saída.
rm "$files_folder/*-saida.txt"

# Iterar pelos arquivos com terminação "-saida" na pasta "backup"
for file in "$files_folder"/*.txt; do
    if [ "$file" != "$files_folder/merged.txt" ]; then
        # Adicionando o conteúdo dos arquivos no mesclado.
        cat "$file" >> "$files_folder/merged.txt"
        
        # Adicionar uma linha em branco
        echo "" >> "$files_folder/merged.txt"
    fi
done