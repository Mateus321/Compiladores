import sys  # acessa os argumentos da linha de comando
import os  # verifica se o arquivo existe antes de abrir
from AnalisadorArquivo import analisar_arquivo
from TipoToken import token_type

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py xxxxxx.java") # EXEMPLO: python main.py teste.java
    
    else:
        analisar_arquivo(sys.argv[1])  # pega o arquivo .java
