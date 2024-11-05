from Biblioteca import PALAVRAS_RESERVADAS


def multi_pontos(token):
    
    # Verifica se o token contém múltiplos pontos, o que indica um número mal formatado
    if token.count(".") > 1:
        raise ValueError(f"Erro de número mal formatado: '{token}' - múltiplos pontos.")


def verificar_token(token):
    
    # Verifica se o token é um número misturado com letras, permitindo hexadecimais
    if token.startswith("0x"):
        
        # Verifica se todos os caracteres após '0x' são válidos em um número hexadecimal
        if all(char in "0123456789ABCDEF" for char in token[2:]):
            return [f"Token hexadecimal válido: '{token}'"]
        
        else:
            return [
                f"Erro de número hexadecimal mal formatado: '{token}' - caracteres inválidos."
            ]
            
    else:
        
        # Verifica se o token é um número misturado com letras
        if any(char.isalpha() for char in token) and any(char.isdigit() for char in token):
            return [f"Token misturado válido: '{token}'"]
        
        else:
            return [
                f"Erro de token mal formatado: '{token}' - deve conter letras e números."
            ]


def verificar_string(f, string_token, linha_atual, col_atual):
    
    while True:
        prox_caractere = f.read(1)
        
        if not prox_caractere:  # Verifica final do arquivo sem fechar string
            print(f"Erro encontrado: Erro de string não fechada: {string_token}")
            return None  # Indica erro
        
        string_token += prox_caractere
        
        if prox_caractere == '"':  # Fecha a string
            print(f"[ 51, '{string_token}', Linha: {linha_atual}, Coluna: {col_atual} ]")
            return string_token  # Retorna a string bem formada
