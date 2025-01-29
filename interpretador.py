# Classe Interpretador para executar o código intermediário
class Interp:
    def __init__(self, fonte=None):
        # Memória de variáveis
        self.mem = {}
        # Rótulos (para controle de fluxo)
        self.rotulos = {}
        # Ponteiro de instrução
        self.ip = 0
        # Lista de instruções
        self.instrucoes = []
        # Controle de execução
        self.executando = True

        # Carrega instruções de um arquivo ou de uma lista
        if isinstance(fonte, str):
            with open(fonte, 'r') as f:
                linhas = f.readlines()
                for linha in linhas:
                    instr = eval(linha.strip(', \n'))
                    if isinstance(instr, tuple):
                        self.instrucoes.append(instr)
                    else:
                        raise ValueError("Instrucao invalida: " + linha.strip(', \n'))
        elif isinstance(fonte, list):
            self.instrucoes = fonte
        else:
            raise ValueError("Fonte invalida, deve ser um caminho de arquivo ou uma lista de instrucoes.")

    def iniciar(self):
        """Inicia a execução das instruções"""
        self.preprocessar_rotulos()

        while self.executando and self.ip < len(self.instrucoes):
            instrucao = self.instrucoes[self.ip]
            self.ip += 1
            self.executar(instrucao)

    def preprocessar_rotulos(self):
        """Armazena os rótulos (LABEL) e suas posições"""
        for i, instr in enumerate(self.instrucoes):
            if instr[0] == "LABEL":
                self.rotulos[instr[1]] = i

    def executar(self, instr):
        """Executa uma única instrução"""
        op, destino, op1, op2 = instr

        # DECLARE (declaração de variável)
        if op == "DECLARE":
            self.mem[destino] = 0 if op1 == "int" else (0.0 if op1 == "float" else "")

        # ASSIGN (atribuição simples)
        elif op == "ASSIGN" or op == "=":
            self.mem[destino] = self.obter_valor(op1)

        # Operações aritméticas (agora processa corretamente)
        elif op in {"+", "-", "*", "/", "%", "//"}:
            val1 = self.obter_valor(op1)
            val2 = self.obter_valor(op2)
            resultado = self.fazer_aritmetica(op, val1, val2)
            self.mem[destino] = resultado  # ✅ Salva o resultado na memória
            self.mostrar_resultado(op, resultado)

        # Operações lógicas e relacionais
        elif op in {"||", "&&", "!", "==", "<>", ">", "<", ">=", "<="}:
            val1 = self.obter_valor(op1)
            val2 = self.obter_valor(op2) if op2 else None
            self.mem[destino] = self.fazer_logica(op, val1, val2)

        # IF e JUMP (controle de fluxo)
        elif op == "IF":
            condicao = self.obter_valor(destino)  # Obtém o valor da comparação
            if condicao:
                self.ip = self.rotulos[op1]  # Vai para LABEL_TRUE
            else:
                self.ip = self.rotulos[op2]  # Vai para LABEL_FALSE

        elif op == "JUMP":
            self.ip = self.rotulos[destino]  # Pula para o label indicado
            
        # LABEL (rótulos são ignorados em tempo de execução)
        elif op == "LABEL":
            return  # ignora LABEL e continua
            
        # PRINT e SCAN
        elif op == "CALL":
            if destino == "PRINT":
                print(self.obter_valor(op1))
            elif destino == "SCAN":
                self.mem[op1] = input("Digite um valor: ")

        # STOP (encerra a execução)
        elif op == "STOP":
            self.executando = False

        else:
            raise ValueError("Operacao desconhecida: " + str(op))


    def fazer_aritmetica(self, op, v1, v2):
        """Executa operações matemáticas"""
        return {
            "+": v1 + v2,
            "-": v1 - v2,
            "*": v1 * v2,
            "/": v1 / v2,
            "%": v1 % v2,
            "//": v1 // v2
        }[op]

    def fazer_logica(self, op, v1, v2):
        """Executa operações lógicas e relacionais"""
        return {
            "||": v1 or v2,
            "&&": v1 and v2,
            "!": not v1,
            "==": v1 == v2,
            "<>": v1 != v2,
            ">": v1 > v2,
            "<": v1 < v2,
            ">=": v1 >= v2,
            "<=": v1 <= v2
        }[op]

    def obter_valor(self, op):
        """Retorna o valor de um operando"""
        if op is None:
            return None
        try:
            return float(op) if "." in str(op) else int(op)
        except ValueError:
            return self.mem.get(op, None)

    def mostrar_instrucao(self, op, destino, op1, op2):
        # mostra passo
        print(f"OP: {op} DEST: {destino} OP1: {op1} OP2: {op2 if op2 else 'None'}")

    def mostrar_resultado(self, op, res):
        # mostra resultado de operacao
        print(f"RESULT {op}: {res}")