import sys

# -----------------------------------------------------------------------------
# TUPLAS DE INSTRUÇÕES (código intermediário)
# -----------------------------------------------------------------------------

lista_tuplas = [
    ('=', 'numBloco_0', 0, None),         # numBloco_0 = 0
    ('=', 'divBloco_0', 0, None),        # divBloco_0 = 0
    ('=', 'restoBloco_0', 0, None),      # restoBloco_0 = 0

    ('CALL', 'PRINT', 'Entre com o inteiro: ', None),  # imprime mensagem
    ('CALL', 'SCAN', None, 'numBloco_0'),              # lê valor p/ numBloco_0
    ('CALL', 'PRINT', None, 'numBloco_0'),             # imprime numBloco_0
    ('CALL', 'PRINT', ' = ', None),                    # imprime " = "

    # Label inicial do loop
    ('LABEL', '__label0', None, None), 
    ('>', '__temp0', 'numBloco_0', '1'),     # __temp0 = (numBloco_0 > 1) ?
    ('IF', '_temp0', 'label1', '__label2'), # Se __temp0 verdadeiro -> __label1, senão -> __label2

    # Label se numBloco_0 > 1
    ('LABEL', '__label1', None, None),
    ('=', 'divBloco_0', '2', None),        # divBloco_0 = 2

    ('LABEL', '__label3', None, None),
    ('%', '__temp1', 'numBloco_0', 'divBloco_0'),  # __temp1 = numBloco_0 % divBloco_0
    ('IF', '_temp1', 'label4', '_label5'),     # Se __temp1 != 0 -> __label4, senão -> __label5

    # label4 -> significa "não foi divisível", então soma 1 em divBloco_0 e continua
    ('LABEL', '__label4', None, None),
    ('LABEL', '__label6', None, None),
    ('+', '__temp2', 'divBloco_0', '1'), 
    ('=', 'divBloco_0', '__temp2', None),
    ('JUMP', '__label3', None, None),

    # label5 -> significa "dividiu", então imprime divBloco_0, faz numBloco_0 /= divBloco_0
    ('LABEL', '__label5', None, None),
    ('CALL', 'PRINT', None, 'divBloco_0'),        # imprime um fator
    ('/', '__temp3', 'numBloco_0', 'divBloco_0'), # __temp3 = numBloco_0 / divBloco_0
    ('=', 'numBloco_0', '__temp3', None),         # numBloco_0 = __temp3

    # Se ainda > 1, imprime " * ", senão para
    ('>', '__temp4', 'numBloco_0', '1'),    
    ('IF', '_temp4', 'label8', '_label9'),  

    ('LABEL', '__label8', None, None),
    ('CALL', 'PRINT', ' * ', None),   # imprime " * "
    ('JUMP', '__label7', None, None),

    ('LABEL', '__label9', None, None),
    ('LABEL', '__label7', None, None),
    ('JUMP', '__label0', None, None),

    # label2 -> se numBloco_0 <= 1, finaliza
    ('LABEL', '__label2', None, None),
    ('CALL', 'PRINT', '\n', None),   # imprime quebra de linha
    ('CALL', 'STOP', None, None)     # encerra execução
]

# -----------------------------------------------------------------------------
# DICIONÁRIO DE LABELS, MEMÓRIA E LISTA DE OPERAÇÕES
# -----------------------------------------------------------------------------

dicionario_labels = {}
memoria_ram = {}

lista_operacoes = ['+', '-', '*', '/', '>', '<', '>=', '<=', '=', '!',
                   '<>', '==', '//', '%', '&&', '||']

# Preencher dicionario_labels com o índice de cada LABEL
for idx, tupla in enumerate(lista_tuplas):
    if tupla[0] == 'LABEL':
        dicionario_labels[tupla[1]] = idx

# -----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES: eh_numero, get_valor, realizaOp
# -----------------------------------------------------------------------------

def eh_numero(val):
    """Retorna True se val pode ser convertido para float/int, senão False."""
    try:
        float(val)
        return True
    except ValueError:
        return False

def get_valor(operando):
    """
    - None -> 0
    - int/float -> retorna direto
    - str -> se nome de variável que está em memoria_ram, retorna esse valor
             se for string numérica, converte p/ int
             se começar com temp/__temp, inicializa 0
             senão -> erro
    """
    if operando is None:
        return 0

    if isinstance(operando, (int, float)):
        return operando

    if isinstance(operando, str):
        # Se já estiver na memória
        if operando in memoria_ram:
            return memoria_ram[operando]
        # Se for numérico
        elif eh_numero(operando):
            return int(float(operando))
        # Se for variável temporária, crie se não existir
        elif operando.startswith("__temp") or operando.startswith("_temp0"):
            memoria_ram[operando] = 0
            return 0
        else:
            print("ERRO: Operando inválido ->", operando)
            sys.exit()

    print("ERRO: Operando inválido (não é int/float/str/None) ->", operando)
    sys.exit()

def realizaOp(operacao, operando1, operando2=None):
    """Executa a operação (binária ou unária) e retorna resultado."""
    if operacao == '+' and operando2 is not None:
        return operando1 + operando2
    elif operacao == '-' and operando2 is not None:
        return operando1 - operando2
    elif operacao == '*':
        return operando1 * operando2
    elif operacao == '/':
        return operando1 / operando2
    elif operacao == '%':
        return operando1 % operando2
    elif operacao == '//':
        return operando1 // operando2
    elif operacao == '+':  # unário
        return +operando1
    elif operacao == '-':  # unário
        return -operando1
    elif operacao == '||':
        return operando1 or operando2
    elif operacao == '&&':
        return operando1 and operando2
    elif operacao == '==':
        return operando1 == operando2
    elif operacao == '<>':  # !=
        return operando1 != operando2
    elif operacao == '>':
        return operando1 > operando2
    elif operacao == '>=':
        return operando1 >= operando2
    elif operacao == '<':
        return operando1 < operando2
    elif operacao == '<=':
        return operando1 <= operando2
    elif operacao == '=':  # Atribuição
        return operando1
    elif operacao == '!':
        return not operando1

    print("ERRO: Operação não reconhecida ->", operacao)
    sys.exit()

# -----------------------------------------------------------------------------
# INTERPRETADOR (loop de execução das tuplas)
# -----------------------------------------------------------------------------

i = 0
while i < len(lista_tuplas):
    comando = lista_tuplas[i][0]

    # 1) Se for uma das operações aritméticas/lógicas (+, -, *, /, etc.)
    if comando in lista_operacoes:
        # Lê operandos
        op1 = get_valor(lista_tuplas[i][2])
        op2 = get_valor(lista_tuplas[i][3])
        # Executa e salva na memória
        memoria_ram[lista_tuplas[i][1]] = realizaOp(comando, op1, op2)

    # 2) JUMP
    elif comando == 'JUMP':
        label_destino = lista_tuplas[i][1]
        if label_destino in dicionario_labels:
            i = dicionario_labels[label_destino]
            continue
        else:
            print("ERRO 3: Label não encontrada ->", label_destino)
            sys.exit()

    # 3) IF
    elif comando == 'IF':
        condicao = get_valor(lista_tuplas[i][1])
        label_true = lista_tuplas[i][2]
        label_false = lista_tuplas[i][3]

        if condicao:
            i = dicionario_labels[label_true]
        else:
            i = dicionario_labels[label_false]
        continue

    # 4) CALL
    elif comando == 'CALL':
        func = lista_tuplas[i][1]

        if func == 'PRINT':
            # A tupla pode ser ('CALL', 'PRINT', 'alguma_string', None)
            # ou ('CALL', 'PRINT', None, 'variavel')
            valor_print = lista_tuplas[i][2]
            if valor_print is None:
                valor_print = lista_tuplas[i][3]
            if valor_print is None:
                print("ERRO: PRINT sem argumentos")
                sys.exit()

            # Se esse valor é nome de variável guardada, pega da memória
            if isinstance(valor_print, str) and valor_print in memoria_ram:
                valor_print = memoria_ram[valor_print]
            elif valor_print in memoria_ram:
                valor_print = memoria_ram[valor_print]

            # Aqui imprimimos sem pular linha (end='')
            print(valor_print, end='')

        elif func == 'SCAN':
            # Exemplo de tupla: ('CALL', 'SCAN', None, 'nome_variavel')
            var_name = lista_tuplas[i][2]
            if var_name is None:
                var_name = lista_tuplas[i][3]

            if var_name is None:
                print("ERRO: SCAN sem variável destino")
                sys.exit()

            entrada = input()
            memoria_ram[var_name] = int(entrada)

        elif func == 'STOP':
            # Encerrar execução
            break
        else:
            print("6º ERRO: Função de CALL não reconhecida ->", func)
            sys.exit()

    # 5) LABEL
    elif comando == 'LABEL':
        # Só um marcador, não faz nada específico aqui
        pass

    else:
        print(f"ERRO: Comando não reconhecido -> {comando}")
        sys.exit()

    i += 1