# codigo indentado com o black

from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    OPERADOR_ATRIBUICAO,
    SIMBOLOS_ACEITOS,
    PALAVRAS_RESERVADAS,
    CARACTERES_INVALIDOS,
)  # chama a biblioteca que criamos


# funcao que vai determinar o tipo do token
def token_type(word):
    # verificar se e float
    if "." in word and all(char.isdigit() for char in word.replace(".", "", 1)):
        return "47"

    if word in OPERADOR_ARITMETICO:
        return OPERADOR_ARITMETICO[word]  # retorna o tipo do operador aritmetico

    elif word in OPERADOR_LOGICO:
        return OPERADOR_LOGICO[word]  # retorna o tipo do operador logico

    elif word in OPERADOR_RELACIONAL:
        return OPERADOR_RELACIONAL[word]  # retorna o tipo do operador relacional

    elif word in OPERADOR_ATRIBUICAO:
        return OPERADOR_ATRIBUICAO[word]  # retorna o tipo do operador de atribuicao

    elif word in SIMBOLOS_ACEITOS:
        return SIMBOLOS_ACEITOS[word]  # retorna o tipo do simbolo aceito

    elif word in PALAVRAS_RESERVADAS:
        return PALAVRAS_RESERVADAS[word]  # retorna o tipo da palavra reservada

    # se um numero comecar com 0 e tiver pelo menos um digito de 0 a 7 ele e octal
    elif (
        word.startswith("0")
        and len(word) > 1
        and all(char in "01234567" for char in word[1:])
    ):
        return "45"

    # verificar se é um numero, mas se comecar com 0 e depois do 0 for um numero de 0 a 7 e octa
    elif word.isdigit():
        return "46"

    # verificar se e um numero hexadecimal
    elif word.startswith("0x") and all(char.isdigit() or char.lower() in "abcdef" for char in word[2:]):
        return "48"

    # verificar se e uma variavel
    elif word[0].isdigit():
        raise ValueError("ERRO: A variável está declarada errada", {word})

    elif any(char in CARACTERES_INVALIDOS for char in word):
        raise ValueError("ERRO", {word})
                
    else:
        return "49"  # se nao e operador e nem palavra reservada, entao e uma variavel
