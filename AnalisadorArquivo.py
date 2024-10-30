import os
from TipoToken import token_type
from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_RELACIONAL,
    SIMBOLOS_ACEITOS,
)
from tratar_erros import tratar_erros, verificar_string

# Faz uma busca pelo arquivo java
def analisar_arquivo(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado!")
        return

    try:
        with open(file_path, "r") as f:
            linha_atual = 1
            col_atual = 1
            token_atual = ""
            # Inicializa a analise do arquivo na posição [1, 1]
             
            print(f"Arquivo: {file_path}")

            while True:
                caractere = f.read(1)
                if not caractere:
                    if token_atual:
                        # Verifica outros tipos de erros no token
                        erros = tratar_erros(token_atual)
                        if erros:
                            for erro in erros:
                                print(f"Erro encontrado: {erro}")
                            return  # Interrompe o processamento ao encontrar um erro
                        else:
                            # Se não houver erro, verifica o tipo e imprime
                            tipo_token = token_type(token_atual)
                            print(
                                f"[ {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]"
                            )
                        token_atual = ""  # Reseta o token após a verificação
                    break

                # Trata strings entre aspas duplas
                if caractere == '"':
                    string_token = verificar_string(
                        f, caractere, linha_atual, col_atual
                    )
                    if not string_token:  # Se retornou None, houve um erro
                        return
                    col_atual += len(
                        string_token
                    )  # Atualiza a coluna com o comprimento da string
                    continue

                # criei uma condicao porque estava dando pau quando era os operadores de > e <
                if caractere in ("<", ">"):
                    prox_caractere = f.read(1)
                    if prox_caractere == "=":
                        tipo_token = OPERADOR_RELACIONAL[ # >= e <= pula duas colunas
                            caractere + prox_caractere
                        ]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        print(
                            f"[ {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]"
                        )
                        col_atual += 2  # >= e <= pula duas colunas 
                    else:
                        # se for so > ou <
                        tipo_token = OPERADOR_RELACIONAL[caractere]
                        print(
                            f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]"
                        )
                        caractere = prox_caractere
                        col_atual += 1
                    continue

                # condicao para ver se o caractere é um espaço, quebra de linha ou símbolo especial
                if (
                    caractere.isspace()
                    or caractere in SIMBOLOS_ACEITOS
                    or caractere in OPERADOR_ARITMETICO
                    or caractere in OPERADOR_RELACIONAL
                ):
                    if token_atual:  # Se tem token acumulado
                        erros = tratar_erros(token_atual)
                        if erros:
                            for erro in erros:
                                print(f"Erro encontrado: {erro}")
                            return  # Interrompe o processamento ao encontrar um erro
                        tipo_token = token_type(token_atual)
                        print(
                            f"[ {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]"
                        )
                        token_atual = ""  # Reseta para o próximo token

                    if caractere in SIMBOLOS_ACEITOS:  # Verifica se é um símbolo
                        tipo_token = SIMBOLOS_ACEITOS[caractere]
                        print(
                            f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]"
                        )
                    elif caractere in OPERADOR_ARITMETICO:
                        tipo_token = OPERADOR_ARITMETICO[caractere]
                        print(
                            f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]"
                        )
                    elif caractere.isspace():  # Se for espaço ou nova linha
                        if caractere == "\n":
                            linha_atual += 1
                            col_atual = 0  # Reinicia coluna ao mudar de linha
                        col_atual += 1
                        continue
                else:
                    token_atual += caractere  # Acumula o caractere no token atual

                col_atual += 1  # Atualiza coluna para cada caractere
        print("Final da análise léxica")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")