# codigo indentado com o black

import os
import sys
from TipoToken import token_type
from Biblioteca import (
    OPERADOR_ATRIBUICAO,
    OPERADOR_ARITMETICO,
    OPERADOR_RELACIONAL,
    SIMBOLOS_ACEITOS,
    CARACTERES_INVALIDOS,
) 
from tratar_erros import multi_pontos, verificar_string

#---------------------------------Função para analisar o arquivo---------------------------------

lista_de_tokens = []


def analisar_arquivo(file_path):
    
    #se o arquivo não existir, ele retorna um erro
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado!")
        return
    
    #ele tenta abri o arquivo para ler 
    try:
        with open(file_path, "r") as f:
            linha_atual = 1
            col_atual = 1
            token_atual = ""
            
            print(f"Arquivo: {file_path}")
            
            #enquanto tirar os caracteres ele vai lendo e verifica
            while True:
                caractere = f.read(1)
                
                if not caractere:
                    if token_atual:
                        # aqui vai ver se o token e um numero com mais de um ponto 
                        erros = multi_pontos(token_atual)
                        
                        if erros:
                            for erro in erros:
                                print(f"Erro encontrado: {erro}")
                            return  # Interrompe o processamento ao encontrar um erro
                        
                        else:
                            # Se não tem erro imprime
                            tipo_token = token_type(token_atual)
                            tupla_token = (tipo_token, token_atual, linha_atual, col_atual - len(token_atual))
                            lista_de_tokens.append(tupla_token)
                            
                        token_atual = ""  # Reseta o token após a verificação
                    break     
                
                # ---------------------------------Tratamento de números com ponto decimal---------------------------------
                    
                try:
                    if caractere == "." and token_atual.replace(".", "").isdigit(): #ele remove o . e verfica se é numero
                        if "." in token_atual:
                            # Chama a funcao multi_pontos para reportar o erro
                            erros = multi_pontos(token_atual + caractere)
                            
                            if erros:
                                print(erros)
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
                            f.seek(f.tell() - 1)# Reposiciona o ponteiro se não for válido
                            
                except ValueError as e: 
                    print (f"Erro encontrado: {str(e)}") # se for mais de um ponto ele retorna um erro
                    sys.exit(1)
                    
                    
                # --------------------------------- Tratamento de comentários // e /* ---------------------------------

                if caractere == "/":  # se o caractere for uma barra
                    prox_caractere = f.read(1)
                    col_atual += 1 

                    if prox_caractere == "/":  # se o próximo for uma barra (comentário de linha)
                        comentario = "//"
                        caractere = f.read(1)
                        col_atual += 1

                        while caractere and caractere != "\n":  # enquanto o caractere for diferente de \n e não for None
                            comentario += caractere
                            caractere = f.read(1)
                            col_atual += 1

                        # Armazena o token do comentário de linha
                        # tupla_token = ("50", comentario, linha_atual, col_atual)
                        # lista_de_tokens.append(tupla_token)

                    elif prox_caractere == "*":  # se o próximo for um asterisco (início de comentário de bloco)
                        comentario = "/*"
                        caractere = f.read(1)  # lê o próximo caractere após `/*`
                        col_atual += 1

                        while caractere:
                            if caractere == "*":  # verifica se é o fechamento de bloco
                                prox_caractere = f.read(1)
                                col_atual += 1
                                if prox_caractere == "/":  # encontrou o final do comentário de bloco
                                    comentario += "*/"
                                    caractere = f.read(1) #arrumei aqui pq ele le o proximo caractere e depois coloca a coluna
                                    col_atual += 1 # coloca a coluna
                                    break
                                else:
                                    comentario += "*"
                                    caractere = prox_caractere
                            else:
                                if caractere == "\n":  # se for uma nova linha, incrementa a linha e reseta a coluna
                                    linha_atual += 1
                                    col_atual = 0

                                comentario += caractere
                                caractere = f.read(1)
                                col_atual += 1

                        else:  # caso o loop termine sem encontrar "*/"
                            print(f"Erro encontrado: Comentário de bloco não fechado. Linha: {linha_atual}, Coluna: {col_atual}")
                            return None  # Indica erro

                        # # Armazena o token do comentário de bloco
                        # tupla_token = ("51", comentario, linha_atual, col_atual)
                        # lista_de_tokens.append(tupla_token)

                        
                    #---------------------------------Tratamento de operadores de atribuição---------------------------------
                    
                    elif prox_caractere == "=":  # se o próximo for um igual
                        tipo_token = OPERADOR_ATRIBUICAO["/="]
                        tupla_token = (tipo_token, caractere + prox_caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        col_atual += 1
                        
                    else:
                        tipo_token = OPERADOR_ARITMETICO["/"]
                        tupla_token = (tipo_token, caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        
                        f.seek(f.tell() - 1)
                        continue
                        
                        
                #---------------------------------Tratamento de strings---------------------------------
                
                
                if caractere == '"':
                    string_token = verificar_string(f, caractere, linha_atual, col_atual)
                    
                    if string_token[0] == None:  # Se retornou None, houve um erro
                        return
                    
                    
                    lista_de_tokens.append(string_token)  
                    
                    col_atual += len(string_token)  # Atualiza a coluna com o comprimento da string
                    continue
                    
                #---------------------------------Tratamento de operadores relacionais e aritméticos---------------------------------
                
                if caractere in ("<", ">"):
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de ser >= ou <=
                        tipo_token = OPERADOR_RELACIONAL[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        tupla_token = (tipo_token, caractere + prox_caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        col_atual += 2  # >= e <= pula duas colunas
                        
                    else:
                        # Entra se for so > ou <
                        tipo_token = OPERADOR_RELACIONAL[caractere]
                        tupla_token = (tipo_token, caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        caractere = prox_caractere
                        col_atual += 1
                        
                    continue 
                    
                if caractere in OPERADOR_ARITMETICO:
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de operador de atribuição
                        tipo_token = OPERADOR_ATRIBUICAO[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        tupla_token = (tipo_token, caractere + prox_caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        col_atual += 2  # += e -= pula duas colunas
                        
                    elif caractere == "/":
                        continue
                        
                    else:
                        # Entra se for so operador aritmético
                        tipo_token = OPERADOR_ARITMETICO[caractere] 
                        tupla_token = (tipo_token, caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                        caractere = prox_caractere
                        col_atual += 1
                    
                #---------------------------------Tratamento de espaços, novas linhas e símbolos---------------------------------
                
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
                        if tipo_token in ["47"]:
                            tupla_token = (tipo_token, token_atual + "0", linha_atual, col_atual - len(token_atual))
                            lista_de_tokens.append(tupla_token)
                            
                        else:
                            tupla_token = (tipo_token, token_atual, linha_atual, col_atual - len(token_atual))
                            lista_de_tokens.append(tupla_token)
                        
                        token_atual = ""  # Reseta para o próximo token
                        
                    if caractere in SIMBOLOS_ACEITOS:  # Verifica se é um símbolo
                        tipo_token = SIMBOLOS_ACEITOS[caractere]
                        tupla_token = (tipo_token, caractere, linha_atual, col_atual)
                        lista_de_tokens.append(tupla_token)
                    
                    #---------------------------------Tratamento de espaços e novas linhas---------------------------------
                    
                    elif caractere.isspace():  # Se for espaço ou nova linha
                        if caractere == "\n":
                            linha_atual += 1
                            col_atual = 0  # Reinicia coluna ao mudar de linha
                        
                        col_atual += 1
                        continue
                        
                else:
                    token_atual += caractere  # Acumula o caractere no token atual
                    
                col_atual += 1  # Atualiza coluna para cada caractere
        
        return lista_de_tokens        
        
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
