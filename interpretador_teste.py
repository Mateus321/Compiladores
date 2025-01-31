import sys

# -----------------------------------------------------------------------------
# TUPLAS DE INSTRUÇÕES (código intermediário)
# -----------------------------------------------------------------------------

lista_tuplas = [
    ('=', 'numBloco_0', 0, None),
    ('=', 'divBloco_0', 0, None),
    ('=', 'restoBloco_0', 0, None),

    ('CALL', 'PRINT', 'Entre com o inteiro: ', None),
    ('CALL', 'SCAN', None, 'numBloco_0'),
    ('CALL', 'PRINT', None, 'numBloco_0'),
    ('CALL', 'PRINT', ' = ', None),

    ('LABEL', '__label0', None, None),
    ('>', '__temp0', 'numBloco_0', '1'),
    ('IF', '__temp0', '__label1', '__label2'),

    ('LABEL', '__label1', None, None),
    ('=', 'divBloco_0', '2', None),

    ('LABEL', '__label3', None, None),
    ('%', '__temp1', 'numBloco_0', 'divBloco_0'),
    ('IF', '__temp1', '__label4', '__label5'),

    ('LABEL', '__label4', None, None),
    ('LABEL', '__label6', None, None),
    ('+', '__temp2', 'divBloco_0', '1'),
    ('=', 'divBloco_0', '__temp2', None),
    ('JUMP', '__label3', None, None),

    ('LABEL', '__label5', None, None),
    ('CALL', 'PRINT', None, 'divBloco_0'),
    ('/', '__temp3', 'numBloco_0', 'divBloco_0'),
    ('=', 'numBloco_0', '__temp3', None),

    ('>', '__temp4', 'numBloco_0', '1'),
    ('IF', '__temp4', '__label8', '__label9'),

    ('LABEL', '__label8', None, None),
    ('CALL', 'PRINT', ' * ', None),
    ('JUMP', '__label7', None, None),

    ('LABEL', '__label9', None, None),
    ('LABEL', '__label7', None, None),
    ('JUMP', '__label0', None, None),

    ('LABEL', '__label2', None, None),
    ('CALL', 'PRINT', '\n', None),
    ('CALL', 'STOP', None, None)
]

# -----------------------------------------------------------------------------
# DICIONÁRIO DE LABELS, MEMÓRIA E LISTA DE OPERAÇÕES
# -----------------------------------------------------------------------------

dicionario_labels = {} # Armazena as variáveis e valores temporários usados durante a execução do código.
memoria_ram = {} 

lista_operacoes = [
    '+', '-', '*', '/', '>', '<', '>=', '<=', '=', '!',
    '<>', '==', '//', '%', '&&', '||'
]

# Preenche o dicionário de labels
for idx, tupla in enumerate(lista_tuplas):
    if tupla[0] == 'LABEL':
        dicionario_labels[tupla[1]] = idx

# -----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES: eh_numero, get_valor, realizaOp
# -----------------------------------------------------------------------------

def eh_numero(val):
    """Retorna True se val pode ser convertido para float/int."""
    try:
        float(val)
        return True
    except ValueError:
        return False

def get_valor(operando): # vai retornar o valor do operando, número, uma variável ou um valor temporário. Se for uma variável, busca o valor na memoria_ram.
    """
    - None -> 0
    - int/float -> retorna direto
    - str -> verifica na memoria_ram, ou se é número literal,
             ou se começa com 'temp'/'__temp', inicializa com 0
    """
    if operando is None:
        return 0

    if isinstance(operando, (int, float)):
        return operando

    if isinstance(operando, str):
        if operando in memoria_ram:
            return memoria_ram[operando]
        elif eh_numero(operando):
            return int(float(operando))
        elif operando.startswith("__temp") or operando.startswith("temp"):
            memoria_ram[operando] = 0
            return 0
        else:
            print("ERRO: Operando inválido ->", operando)
            sys.exit()

    print("ERRO: Operando inválido ->", operando)
    sys.exit()

def realizaOp(operacao, operando1, operando2=None): # operações aritméticas e lógicas
    """Executa a operação (binária ou unária) e retorna o resultado."""
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
    elif operacao == '<>':
        return operando1 != operando2
    elif operacao == '>':
        return operando1 > operando2
    elif operacao == '>=':
        return operando1 >= operando2
    elif operacao == '<':
        return operando1 < operando2
    elif operacao == '<=':
        return operando1 <= operando2
    elif operacao == '=':
        return operando1
    elif operacao == '!':
        return not operando1

    print("ERRO: Operação não reconhecida ->", operacao)
    sys.exit()

# -----------------------------------------------------------------------------
# INTERPRETADOR (LOOP) Percorre a lista de tuplas e executa cada comando.
# -----------------------------------------------------------------------------

i = 0
while i < len(lista_tuplas):
    comando = lista_tuplas[i][0]

    # 1) Operações
    if comando in lista_operacoes:
        op1 = get_valor(lista_tuplas[i][2])
        op2 = get_valor(lista_tuplas[i][3])
        memoria_ram[lista_tuplas[i][1]] = realizaOp(comando, op1, op2)

    # 2) JUMP
    elif comando == 'JUMP':
        label_destino = lista_tuplas[i][1]
        if label_destino in dicionario_labels:
            i = dicionario_labels[label_destino]
            continue
        else:
            print("ERRO: Label não encontrada ->", label_destino)
            sys.exit()

    # 3) IF
    elif comando == 'IF':
        condicao = get_valor(lista_tuplas[i][1])
        label_true = lista_tuplas[i][2]
        label_false = lista_tuplas[i][3]

        if condicao:  # Em Python, 0/False => False; qualquer outro valor => True
            i = dicionario_labels[label_true]
        else:
            i = dicionario_labels[label_false]
        continue

    # 4) CALL
    elif comando == 'CALL':
        func = lista_tuplas[i][1]
        if func == 'PRINT':
            valor_print = lista_tuplas[i][2]
            if valor_print is None:
                valor_print = lista_tuplas[i][3]
            if valor_print is None:
                print("ERRO: PRINT sem argumentos")
                sys.exit()
            # Se for variável, pega da memória
            if isinstance(valor_print, str) and valor_print in memoria_ram:
                valor_print = memoria_ram[valor_print]
            elif valor_print in memoria_ram:
                valor_print = memoria_ram[valor_print]
            # Imprime sem pular linha (até encontrar '\n')
            print(valor_print, end='')

        elif func == 'SCAN':
            var_name = lista_tuplas[i][2]
            if var_name is None:
                var_name = lista_tuplas[i][3]
            if var_name is None:
                print("ERRO: SCAN sem variável destino")
                sys.exit()
            entrada = input()
            memoria_ram[var_name] = int(entrada)

        elif func == 'STOP':
            break

        else:
            print("ERRO: Função CALL não reconhecida ->", func)
            sys.exit()

    # 5) LABEL
    elif comando == 'LABEL':
        # LABEL é só para marcador, não faz nada, so mostra aonde pular.
        pass

    else:
        print("ERRO: Comando não reconhecido ->", comando)
        sys.exit()

    i += 1