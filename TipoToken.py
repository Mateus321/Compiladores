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
