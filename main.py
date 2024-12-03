import sys  # acessa os argumentos da linha de comando
import os  # verifica se o arquivo existe antes de abrir
from AnalisadorArquivo import analisar_arquivo
from paser import parse_function_star

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py xxxxxx.java") # EXEMPLO: python main.py teste.java
        
    else:
        lista_de_tokens = []
        lista_de_tokens.append(analisar_arquivo(sys.argv[1]))  # pega o arquivo .java
        
        #imprimir essa lista de tokens com quebra de linha
        print("\n".join(str(token) for token in lista_de_tokens[0]))
        print("\nFinal da análise léxica")

        #chamar o parser
        
        try:
            parse_function_star(lista_de_tokens[0])
            print("\nAnálise sintática concluída com sucesso\n")
        except Exception as e:
            print(f"Erro na análise sintática: {e}")