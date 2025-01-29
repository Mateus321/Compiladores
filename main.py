import sys
import traceback
from AnalisadorArquivo import analisar_arquivo
from paser import parse_function_star
from interpretador import Interp


def tokens_para_instrucoes(tokens):
    """Converte tokens da análise léxica em código intermediário"""
    instrucoes = []
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i][:2]

        # DECLARE
        if token_type in {'21', '22', '23'}:  # int, float, string
            if i+1 < len(tokens) and tokens[i+1][0] == '49':  # Identificador após o tipo
                instrucoes.append(("DECLARE", tokens[i+1][1], token_value, None))
                i += 1  # Pula identificador

        # ASSIGN e operações matemáticas
        elif token_type == '15':  # '='
            var = tokens[i-1][1]
            expr = tokens[i+1:]
            if len(expr) >= 3 and expr[1][1] in {"+", "-", "*", "/", "%", "//"}:
                instrucoes.append((expr[1][1], var, expr[0][1], expr[2][1]))
                i += 2  # Pula dois operandos e operador
            else:
                instrucoes.append(("ASSIGN", var, expr[0][1], None))
                i += 1

        # IF (gera comparação e JUMP)
        elif token_type == '28':  # 'if'
            cond_var = f"_temp{len(instrucoes)}"  # Cria variável temporária
            var = tokens[i+2][1]  # Nome da variável comparada
            op = tokens[i+3][1]  # Operador (>, <, ==, etc.)
            valor = tokens[i+4][1]  # Valor a comparar

            instrucoes.append((op, cond_var, var, valor))  # Ex: ('>', '_temp1', 'a', '3')
            instrucoes.append(("IF", cond_var, "LABEL_TRUE", "LABEL_FALSE"))  # Ex: ('IF', '_temp1', 'LABEL_TRUE', 'LABEL_FALSE')
            instrucoes.append(("LABEL", "LABEL_TRUE", None, None))

        # ELSE (gera rótulo)
        elif token_type == '29':  # 'else'
              instrucoes.insert(-1, ("JUMP", "LABEL_END", None, None)) 
              instrucoes.append(("LABEL", "LABEL_FALSE", None, None))


        # Fecha bloco do IF/ELSE
        elif token_type == '39':  # '}'
            instrucoes.append(("LABEL", "LABEL_END", None, None))

        i += 1
    return instrucoes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.java>")
        sys.exit(1)

    arquivo_java = sys.argv[1]

    try:
        # **Análise Léxica**
        lista_de_tokens = analisar_arquivo(arquivo_java)
        print("\nTokens gerados:")
        print("\n".join(str(token) for token in lista_de_tokens))
        print("\nFinal da análise léxica.")

        # **Análise Sintática**
        try:
            parse_function_star(lista_de_tokens)
            print("\nAnálise sintática concluída com sucesso!\n")
        except Exception as e:
            print(f"\nErro na análise sintática: {e}")
            print(traceback.format_exc())
            sys.exit(1)

        # **Conversão de Tokens para Instruções**
        try:
            tuplas_convertidas = tokens_para_instrucoes(lista_de_tokens)
            print("\nInstruções convertidas com sucesso:")
            for instrucao in tuplas_convertidas:
                print(instrucao)
        except Exception as e:
            print(f"\nErro na conversão de tokens para instruções: {e}")
            print(traceback.format_exc())
            sys.exit(1)

        # **Execução do Interpretador**
        try:
            interpretador = Interp(tuplas_convertidas)
            print("\nIniciando execução do interpretador...")
            interpretador.iniciar()  
        except Exception as e:
            print(f"\nErro no interpretador: {e}")
            print(traceback.format_exc())
            sys.exit(1)

    except FileNotFoundError:
        print(f"\nErro: Arquivo '{arquivo_java}' não encontrado. Verifique o caminho e tente novamente.")
        sys.exit(1)

    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print(traceback.format_exc())
        sys.exit(1)
