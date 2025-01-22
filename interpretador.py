from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    PALAVRAS_RESERVADAS,
    SIMBOLOS_ACEITOS,
)

class Interpretador:
    def __init__(self):
        self.variaveis = {}  # Armazena variáveis e valores
        self.ponteiro = 0  # Controla a posição de execução
        self.tuplas = []  # Lista de tuplas a executar
        self.labels = {}  # Armazena as posições dos labels

    def carregar_tuplas(self, tuplas):
        """Carrega a lista de tuplas e processa os labels."""
        self.tuplas = tuplas
        for index, instrucao in enumerate(tuplas):
            if instrucao[0] == "LABEL":
                self.labels[instrucao[1]] = index

    def executar(self):
        """Executa as tuplas na ordem, respeitando alterações de fluxo."""
        while self.ponteiro < len(self.tuplas):
            instrucao = self.tuplas[self.ponteiro]
            self.processar_instrucao(instrucao)

    def processar_instrucao(self, instrucao):
        """Processa uma única instrução com base no operador."""
        operador = instrucao[0]
        if operador in OPERADOR_ARITMETICO:
            self.processar_aritmetica(instrucao)
        elif operador in OPERADOR_LOGICO:
            self.processar_logica(instrucao)
        elif operador in OPERADOR_RELACIONAL:
            self.processar_relacional(instrucao)
        elif operador == "IF":
            self.processar_condicional(instrucao)
        elif operador == "JUMP":
            self.processar_jump(instrucao)
        elif operador == "CALL":
            self.processar_chamada(instrucao)
        elif operador == "=":
            self.processar_atribuicao(instrucao)
        self.ponteiro += 1

    def processar_aritmetica(self, instrucao):
        """Processa operadores aritméticos."""
        operador, guardar, op1, op2 = instrucao
        valor1 = self.get_valor(op1)
        valor2 = self.get_valor(op2) if op2 is not None else 0

        if operador == "+":
            self.variaveis[guardar] = valor1 + valor2
        elif operador == "-":
            self.variaveis[guardar] = valor1 - valor2
        elif operador == "*":
            self.variaveis[guardar] = valor1 * valor2
        elif operador == "/":
            self.variaveis[guardar] = valor1 / valor2
        elif operador == "%":
            self.variaveis[guardar] = valor1 % valor2

    def processar_logica(self, instrucao):
        """Processa operadores lógicos."""
        operador, guardar, op1, op2 = instrucao
        valor1 = self.get_valor(op1)
        valor2 = self.get_valor(op2) if op2 is not None else None

        if operador == "||":
            self.variaveis[guardar] = valor1 or valor2
        elif operador == "&&":
            self.variaveis[guardar] = valor1 and valor2
        elif operador == "!":
            self.variaveis[guardar] = not valor1

    def processar_relacional(self, instrucao):
        """Processa operadores relacionais."""
        operador, guardar, op1, op2 = instrucao
        valor1 = self.get_valor(op1)
        valor2 = self.get_valor(op2)

        if operador == "==":
            self.variaveis[guardar] = valor1 == valor2
        elif operador == "!=":
            self.variaveis[guardar] = valor1 != valor2
        elif operador == ">":
            self.variaveis[guardar] = valor1 > valor2
        elif operador == "<":
            self.variaveis[guardar] = valor1 < valor2
        elif operador == ">=":
            self.variaveis[guardar] = valor1 >= valor2
        elif operador == "<=":
            self.variaveis[guardar] = valor1 <= valor2

    def processar_condicional(self, instrucao):
        """Processa instruções do tipo IF."""
        _, condicao, label_true, label_false = instrucao
        if self.get_valor(condicao):
            self.ponteiro = self.labels[label_true]
        else:
            self.ponteiro = self.labels[label_false]

    def processar_jump(self, instrucao):
        """Processa instruções do tipo JUMP."""
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label]

    def processar_chamada(self, instrucao):
        """Processa chamadas de sistema."""
        _, comando, valor, _ = instrucao
        if comando == "PRINT":
            print(self.get_valor(valor))
        elif comando == "SCAN":
            entrada = input("Digite um valor: ")
            self.variaveis[valor] = entrada

    def processar_atribuicao(self, instrucao):
        """Processa instruções de atribuição."""
        _, guardar, valor, _ = instrucao
        self.variaveis[guardar] = self.get_valor(valor)

    def get_valor(self, token):
        """Retorna o valor de uma variável ou o próprio token, se for um literal."""
        if isinstance(token, str) and token in self.variaveis:
            return self.variaveis[token]
        return token
