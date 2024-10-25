import os
from TipoToken import token_type
from Biblioteca import OPERADOR_ARITMETICO, OPERADOR_LOGICO, OPERADOR_RELACIONAL, OPERADOR_ATRIBUICAO, PALAVRAS_RESERVADAS, SIMBOLOS_ACEITOS

def analisar_arquivo(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado!")
        return
    
    try:
        with open(file_path, 'r') as f:
            linha_atual = 1
            col_atual = 1
            token_atual = ""

            print(f"Arquivo: {file_path}")
            
            while True:
                caractere = f.read(1)
                if not caractere:
                    if token_atual:
                        # Verifica o tipo do token final
                        tipo_token = token_type(token_atual)
                        print(f"[ {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                    break

                # Verifica se o caractere é um espaço, quebra de linha ou símbolo especial
                if caractere.isspace() or caractere in SIMBOLOS_ACEITOS or caractere in OPERADOR_ARITMETICO or caractere in OPERADOR_RELACIONAL:
                    if token_atual:  # Se há um token acumulado, processa-o
                        tipo_token = token_type(token_atual)
                        print(f"[ {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                        token_atual = ""  # Reseta para o próximo token

                    if caractere in SIMBOLOS_ACEITOS:  # Verifica se é um símbolo
                        tipo_token = SIMBOLOS_ACEITOS[caractere]
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                    elif caractere in OPERADOR_ARITMETICO:
                        tipo_token = OPERADOR_ARITMETICO[caractere]
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                    elif caractere.isspace():  # Se for espaço ou nova linha
                        if caractere == '\n':
                            linha_atual += 1
                            col_atual = 0  # Reinicia coluna ao mudar de linha
                        col_atual += 1
                        continue
                else:
                    token_atual += caractere  # Acumula o caractere no token atual

                col_atual += 1  # Atualiza coluna para cada caractere

    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")