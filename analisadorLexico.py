import sys  # acessa os argumentos da linha de comando
import os  # verifica se o arquivo existe antes de abrir
from AnalisadorArquivo import analisar_arquivo
from TipoToken import token_type

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analisadorLexico.py <arquivo>")
    else:
        analisar_arquivo(sys.argv[1])  # pega o arquivo .java