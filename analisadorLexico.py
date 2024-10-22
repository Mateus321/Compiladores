import sys # acessa os argumentos da linha de comando
import os # verifica se o arquivo existe antes de abrir
from Biblioteca import OPERADOR_ARITMETICO, OPERADOR_LOGICO, OPERADOR_RELACIONAL, OPERADOR_ATRIBUICAO, SIMBOLOS_ACEITOS, PALAVRAS_RESERVADAS #chama a biblioteca que criamos


# funcao que vai determinar o tipo do token
def token_type(word):
    if word in OPERADOR_ARITMETICO:
        return OPERADOR_ARITMETICO[word] #retorna o tipo do operador aritmetico
    
    elif word in OPERADOR_LOGICO:
        return OPERADOR_LOGICO[word] #retorna o tipo do operador logico
    
    elif word in OPERADOR_RELACIONAL:
        return OPERADOR_RELACIONAL[word] #retorna o tipo do operador relacional
    
    elif word in OPERADOR_ATRIBUICAO:
        return OPERADOR_ATRIBUICAO[word] #retorna o tipo do operador de atribuicao
    
    elif word in SIMBOLOS_ACEITOS:
        return SIMBOLOS_ACEITOS[word] #retorna o tipo do simbolo aceito
    
    elif word in PALAVRAS_RESERVADAS:
        return PALAVRAS_RESERVADAS[word] #retorna o tipo da palavra reservada
    
    elif word.isdigit():  # vai verificar se é um número
        return 'NUMERO'
    
    else:
        return 'IDENTIFICADOR'  # se nao e operador e nem palavra reservada, entao e uma variavel

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analisadorLexico.py <arquivo>")
    else:
        analisar_arquivo(sys.argv[1]) # aqui ele vai pegar o arquivo .java que sera analisado
