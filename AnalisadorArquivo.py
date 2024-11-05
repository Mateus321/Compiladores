# codigo indentado com o black

import os
import sys
from TipoToken import token_type
from Biblioteca import (
    OPERADOR_ATRIBUICAO,
    OPERADOR_ARITMETICO,
    OPERADOR_RELACIONAL,
    SIMBOLOS_ACEITOS,
)
from tratar_erros import multi_pontos, verificar_string

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
                        erros = multi_pontos(token_atual)
                        
                        if erros:
                            for erro in erros:
                                print(f"Erro encontrado: {erro}")
                            return  # Interrompe o processamento ao encontrar um erro
                        
                        else:
                            # Se não houver erro, verifica o tipo e imprime
                            tipo_token = token_type(token_atual)
                            print(f"[a {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                            
                        token_atual = ""  # Reseta o token após a verificação
                    break
                    
                try:
                    if caractere == "." and token_atual.replace(".", "").isdigit():    
                        if "." in token_atual:
                            # Chama o multi_pontos para reportar o erro
                            erros = multi_pontos(token_atual + caractere)
                            
                            if erros:
                                print(erros)  # Ou você pode lidar com o erro de outra forma
                            continue  # Sai do loop atual para evitar continuar com o token inválido
                            
                        prox_caractere = f.read(1)
                        
                        if (
                            prox_caractere.isdigit() 
                            or prox_caractere.isspace() 
                            or prox_caractere in SIMBOLOS_ACEITOS
                            ):
                            
                            token_atual += caractere
                            
                            if prox_caractere.isdigit():
                                token_atual += prox_caractere
                                col_atual += 2
                                
                            else:
                                f.seek(
                                    f.tell() - 1
                                )  # Reposiciona o ponteiro se for espaço ou símbolo
                            continue
                            
                        else:
                            f.seek(f.tell() - 1)  # Reposiciona o ponteiro se não for válido
                            
                except ValueError as e: 
                    sys.exit(1)
                
                if caractere == "/":  # se o caracter for um barra
                    prox_caractere = f.read(1)  # le o proximo
                    col_atual += 1  # coloca uma coluna
                    
                    if prox_caractere == "/":  # se o proximo for uma barra
                        comentario = "//"
                        caractere = f.read(1)  # lê o próximo caractere para iniciar o comentário
                        col_atual += 1
                        
                        while (caractere != "\n" and caractere):  # enquanto o caractere for diferente de \n e tiver caractere
                            comentario += (caractere) # adiciona o caractere ao comentário
                            caractere = f.read(1)  # lê o próximo caractere
                            col_atual += 1
                            
                        print(f"[ 50, '{comentario}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        
                    elif (prox_caractere == "*"):  # se o próximo for um asterisco (início de um comentário de bloco)
                        comentario = "/*"
                        caractere = f.read(1)  # lê o próximo caractere após `/*`
                        col_atual += 1
                        
                        while caractere:
                            if caractere == "*":
                                prox_caractere = f.read(1)  # olha o próximo caractere para verificar se é `/`
                                col_atual += 1
                                
                                if (prox_caractere == "/"):  # encontrou o final do comentário de bloco
                                    comentario += "*/"
                                    break
                                
                                else:
                                    comentario += ("*")# adiciona `*` ao comentário e continua
                                    caractere = prox_caractere
                                    
                            else:
                                if (caractere == "\n"):  # se for uma nova linha, incrementa a linha e reseta a coluna
                                    linha_atual += 1
                                    col_atual = 0
                                    
                                comentario += (caractere) # adiciona o caractere ao comentário
                                caractere = f.read(1)  # lê o próximo caractere
                                col_atual += 1
                                
                        else:
                            print(f"Erro encontrado: Erro de comentário de bloco não fechado: {comentario}")
                            return None  # Indica erro
                            
                        print(f"[ 50, '{comentario}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                    
                    elif prox_caractere == "=":  # se o próximo for um igual
                        tipo_token = OPERADOR_ATRIBUICAO["/="]
                        print(f"[l {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 1
                        
                    else:
                        tipo_token = OPERADOR_ARITMETICO["/"]
                        print(f"[b {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        f.seek(f.tell() - 1)
                        continue
                        
                # Trata strings entre aspas duplas
                if caractere == '"':
                    string_token = verificar_string(f, caractere, linha_atual, col_atual)
                    
                    if not string_token:  # Se retornou None, houve um erro
                        return
                        
                    col_atual += len(string_token)  # Atualiza a coluna com o comprimento da string
                    continue
                    
                # Foi criada uma condicao porque estava com problema nos operadores de > e <
                if caractere in ("<", ">"):
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de ser >= ou <=
                        tipo_token = OPERADOR_RELACIONAL[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        print(f"[c {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 2  # >= e <= pula duas colunas
                        
                    else:
                        # Entra se for so > ou <
                        tipo_token = OPERADOR_RELACIONAL[caractere]
                        print(f"[d {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        caractere = prox_caractere
                        col_atual += 1
                        
                    continue
                    
                # Verificar operadores de atribuição
                if caractere in OPERADOR_ARITMETICO:
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de operador de atribuição
                        tipo_token = OPERADOR_ATRIBUICAO[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        print(f"[e {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 2  # += e -= pula duas colunas
                        
                    elif caractere == "/":
                        continue
                        
                    else:
                        # Entra se for so operador aritmético
                        tipo_token = OPERADOR_ARITMETICO[caractere] 
                        print(f"[f {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        caractere = prox_caractere
                        col_atual += 1
                        
                    continue
                    
                    
                # Condição para ver se o caractere é um espaço, quebra de linha ou símbolo especial
                if (
                    caractere.isspace()
                    or caractere in SIMBOLOS_ACEITOS
                    or caractere in OPERADOR_RELACIONAL
                ):
                    if token_atual:  # Se tem token acumulado
                        erros = multi_pontos(token_atual)
                        if erros:
                            for erro in erros:
                                print(f"Erro encontrado: {erro}")
                            return  # Interrompe o processamento ao encontrar um erro
                        
                        tipo_token = token_type(token_atual)
                        
                        # adicona um 0 no final do token se for um float
                        if tipo_token in ["44", "47"]:
                            print(f"[g {tipo_token}, '{token_atual}0', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                            
                        else:
                            print(f"[h {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                        
                        token_atual = ""  # Reseta para o próximo token
                        
                    if caractere in SIMBOLOS_ACEITOS:  # Verifica se é um símbolo
                        tipo_token = SIMBOLOS_ACEITOS[caractere]
                        print(f"[i {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        
                    # Verifica se o caractere é um operador aritmético ou um número negativo
                    elif caractere == "-" and not token_atual:
                        prox_caractere = f.read(1)
                        
                        while prox_caractere.isspace():
                            prox_caractere = f.read(1)
                            col_atual += 1
                        
                        if prox_caractere.isdigit():
                            # Trata o número negativo como um único token
                            token_atual = caractere + prox_caractere
                            col_atual += 1
                            decimal_found = False  # isso aqui e para poder colocar somente um . depois do n
                            # Continua lendo dígitos enquanto forem parte do número negativo
                            
                            while True:
                                prox_caractere = f.read(1)
                                
                                if prox_caractere.isdigit():
                                    token_atual += prox_caractere
                                    col_atual += 1
                                
                                elif prox_caractere == "." and not decimal_found:
                                    # Permite um ponto decimal para floats
                                    token_atual += prox_caractere
                                    col_atual += 1
                                    decimal_found = True  # Marca que já encontramos um ponto decimal
                                
                                else:
                                    # Retorna o caractere não numérico para o fluxo e encerra o loop
                                    f.seek(f.tell() - 1)
                                    break
                            # Verifica o tipo do token acumulado como número negativo
                            tipo_token = token_type(token_atual)
                            print(f"[j {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)+1} ]")
                            token_atual = ""  # Reseta o token atual
                            continue
                            
                        else:
                            # Trata o '-' como operador aritmético
                            tipo_token = OPERADOR_ARITMETICO[caractere]
                            print(f"[k {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                            caractere = (prox_caractere)# Continua com o próximo caractere
                            col_atual += 1
                            continue
                            
                    
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
