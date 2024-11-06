# codigo indentado com o black

import os
import sys
import string
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
                            print(f"[a {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                            
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
                    
                
                #---------------------------------Tratamento de comentários / e /*  ---------------------------------
                
                
                if caractere == "/": # se o caractere for uma barra
                    prox_caractere = f.read(1)
                    col_atual += 1 
                    
                    if prox_caractere == "/":  # se o proximo for uma barra
                        comentario = "//"
                        caractere = f.read(1) 
                        col_atual += 1
                        
                        while (caractere != "\n" and caractere):  # enquanto o caractere for diferente de \n e tiver caractere
                            comentario += (caractere)
                            caractere = f.read(1)  
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
                                caractere = f.read(1)
                                col_atual += 1
                                
                        else:
                            print(f"Erro encontrado: Erro de comentário de bloco não fechado: Linha: {linha_atual}, Coluna: {col_atual}")
                            return None  # Indica erro
                            
                        print(f"[ 50, '{comentario}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        
                    #---------------------------------Tratamento de operadores de atribuição---------------------------------
                    
                    elif prox_caractere == "=":  # se o próximo for um igual
                        tipo_token = OPERADOR_ATRIBUICAO["/="]
                        print(f"[ {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 1
                        
                    else:
                        tipo_token = OPERADOR_ARITMETICO["/"]
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        f.seek(f.tell() - 1)
                        continue
                        
                        
                #---------------------------------Tratamento de strings---------------------------------
                
                
                if caractere == '"':
                    string_token = verificar_string(f, caractere, linha_atual, col_atual)
                    
                    if not string_token:  # Se retornou None, houve um erro
                        return
                        
                    col_atual += len(string_token)  # Atualiza a coluna com o comprimento da string
                    continue
                    
                #---------------------------------Tratamento de operadores relacionais e aritméticos---------------------------------
                
                if caractere in ("<", ">"):
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de ser >= ou <=
                        tipo_token = OPERADOR_RELACIONAL[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        print(f"[ {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 2  # >= e <= pula duas colunas
                        
                    else:
                        # Entra se for so > ou <
                        tipo_token = OPERADOR_RELACIONAL[caractere]
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        caractere = prox_caractere
                        col_atual += 1
                        
                    continue 
                    
                if caractere in OPERADOR_ARITMETICO:
                    prox_caractere = f.read(1)
                    
                    if prox_caractere == "=": # Entra no caso de operador de atribuição
                        tipo_token = OPERADOR_ATRIBUICAO[caractere + prox_caractere]  # aqui ele pega os dois e tenta encontrar no operador relacional
                        print(f"[ {tipo_token}, '{caractere + prox_caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                        col_atual += 2  # += e -= pula duas colunas
                        
                    elif caractere == "/":
                        continue
                        
                    else:
                        # Entra se for so operador aritmético
                        tipo_token = OPERADOR_ARITMETICO[caractere] 
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
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
                            print(f"[ {tipo_token}, '{token_atual}0', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                            
                        else:
                            print(f"[ {tipo_token}, '{token_atual}', Linha: {linha_atual}, Coluna: {col_atual - len(token_atual)} ]")
                        
                        token_atual = ""  # Reseta para o próximo token
                        
                    if caractere in SIMBOLOS_ACEITOS:  # Verifica se é um símbolo
                        tipo_token = SIMBOLOS_ACEITOS[caractere]
                        print(f"[ {tipo_token}, '{caractere}', Linha: {linha_atual}, Coluna: {col_atual} ]")
                    
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
                
        print("Final da análise léxica")
        
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
