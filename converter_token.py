from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    OPERADOR_ATRIBUICAO,
    PALAVRAS_RESERVADAS,
    SIMBOLOS_ACEITOS,
)

# Mapeamento para traduzir tokens em operadores/comandos
MAPA_TOKENS = {
    **OPERADOR_ARITMETICO,
    **OPERADOR_LOGICO,
    **OPERADOR_RELACIONAL,
    **OPERADOR_ATRIBUICAO,
    "36": ";",
    "39": "}",
    "40": "(",
    "41": ")",
    "33": "PRINT",
    "35": "SCAN",
}

def converter_tokens_para_instrucoes(tokens_lexicos):
    """Converte os tokens léxicos em instruções para o interpretador."""
    instrucoes = []
    for token in tokens_lexicos:
        tipo, lexema, linha, coluna = token  # Desempacota o token

        if tipo in MAPA_TOKENS:
            operador = MAPA_TOKENS[tipo]

            # Exemplo: Operadores aritméticos
            if operador in OPERADOR_ARITMETICO:
                instrucoes.append((operador, "var_temp", "op1", "op2"))

            # Comando PRINT
            elif operador == "PRINT":
                instrucoes.append(("CALL", "PRINT", lexema, None))

            # Comando SCAN
            elif operador == "SCAN":
                instrucoes.append(("CALL", "SCAN", lexema, None))

        # Identificadores (variáveis ou labels)
        elif lexema.isidentifier():
            instrucoes.append(("LABEL", lexema, None, None))

        # Literais numéricos
        elif lexema.isnumeric():
            instrucoes.append(("=", "var_temp", int(lexema), None))

    
    print("teste? \n", instrucoes)
    
    return instrucoes
