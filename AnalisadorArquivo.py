import os
from TipoToken import token_type

def analisar_arquivo(file_path): # abre o arquivo e le linha por linha
    if not os.path.exists(file_path): # ve se o arquivo existe antes de abrir
        print(f"Erro: O arquivo '{file_path}' não foi encontrado!")
        return
    
    try:
        # Abre o arquivo de teste
        with open(file_path, 'r') as f:
            linha_atual = 1
            print(f"Arquivo: {file_path}")
            for linha in f: # aqui ele vai ler linha por linha
                col_atual = 1
                palavras = linha.split()  # Separar a linha em palavras
                for palavra in palavras:
                    tipo_token = token_type(palavra)
                    print(f"[ {palavra}, {tipo_token}, {linha_atual}, {col_atual} ]") # printa os tokens
                    col_atual += len(palavra) + 1  # Atualizar a coluna
                linha_atual += 1  # Atualizar a linha
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")