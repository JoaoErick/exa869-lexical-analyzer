#!/bin/bash

# Caminhos das pastas
backup_folder="./src/files/backup"
files_folder="./src/files"

# Iterar pelos arquivos com terminação "-saida" na pasta "backup"
for backup_file in "$backup_folder"/*-saida.txt; do
    # Extrair o nome do arquivo
    filename=$(basename "$backup_file")

    # Caminho para o arquivo correspondente na pasta "files"
    files_file="$files_folder/$filename"

    # Verificar se o arquivo correspondente existe na pasta "files"
    if [ -e "$files_file" ]; then
        # Executar o comando diff entre os arquivos
        diff_result=$(diff "$backup_file" "$files_file")

        # Exibir o resultado do diff apenas se houver diferenças
        if [ -n "$diff_result" ]; then
            echo "Differences found in the file: $filename"
            echo "$diff_result"
        fi
    else
        echo "Corresponding file not found in files folder for: $filename"
    fi
done