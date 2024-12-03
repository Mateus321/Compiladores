#tokens = lista de toknes no lexer
#token_atual = o token que ta sendo lido no meomento
#pos = posicao do token atual na lista
#avanca = avanca para o proximo token
#get_tipo_token = pega o tipo do token
#match = verifica se o token atual é do tipo esperado e avanca
#error = lanca erro de sintaxe

from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    OPERADOR_ATRIBUICAO,
    PALAVRAS_RESERVADAS,
    SIMBOLOS_ACEITOS,
    CARACTERE_COMENTARISO,
)

# inverter dicionario para saber o tipo 
def inverter_dicionario(dicionario):
    return {valor: chave for chave, valor in dicionario.items()}

TOKEN_TYPE_MAPPING = {}

# inverte e combina os dois
for dic in [
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    OPERADOR_ATRIBUICAO,
    PALAVRAS_RESERVADAS,
    SIMBOLOS_ACEITOS,
    CARACTERE_COMENTARISO,
]:
    TOKEN_TYPE_MAPPING.update(inverter_dicionario(dic))

# coloquei mais alguns que nao estavam no dicionairio
TOKEN_TYPE_MAPPING.update({
    "45": "NUMoct",
    "46": "NUMint",
    "47": "NUMfloat",
    "48": "NUMhex",
    "49": "IDENT",
    "51": "STR",
})


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens (tuplas)
        self.token_atual = None  # Token atual (tupla)
        self.pos = -1  # Posição atual na lista de tokens
        self.avanca()  # Avança para o primeiro token

    def avanca(self):
        """Avança para o próximo token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]
        else:
            self.token_atual = None  # Fim dos tokens
            # print("Fim dos tokens")
                
    def get_tipo_token(self, token):
        """Obtém o tipo do token a partir do código do token."""
        if token is None:
            return None
        token_code = token[0]
        tipo_token = TOKEN_TYPE_MAPPING.get(token_code)
        if tipo_token is None:
            self.error(f"Código de token desconhecido: {token_code}")
        return tipo_token

    def get_valor_token(self, token):
        """Obtém o valor do token."""
        if token is None:
            return None
        return token[1]

    def match(self, tipo_esperado):
        """Verifica se o token atual é do tipo esperado e avança."""
        tipo_atual = self.get_tipo_token(self.token_atual)
        
        if tipo_atual == tipo_esperado:
            self.avanca()
        else:
            valor_esperado = tipo_esperado
            tipo_atual = tipo_atual if tipo_atual else 'EOF'
            self.error(f"Esperado '{valor_esperado}', encontrado '{tipo_atual}'")


    def error(self, message):
        """Lança uma exceção de erro de"""
        linha = self.token_atual[2] if self.token_atual else 'EOF'
        coluna = self.token_atual[3] if self.token_atual else ''
        raise Exception(f"Erro de sintaxe na linha {linha}, coluna {coluna}: {message}")

    #aqui comeca as funcoes da gramatica 

    def parse_function_star(self):
        """<function*> -> <type> 'IDENT' '(' ')' <bloco> ;""" #funcao principal comeca
        self.parse_type()
        self.match('IDENT')
        self.match('(')
        self.match(')')
        self.parse_bloco()
        if self.token_atual is not None:
            self.error("Tokens extras após o fim da função")

    def parse_type(self):
        """<type> -> 'int' | 'float' | 'string' ;"""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('int', 'float', 'string'):
            self.avanca()
        else:
            self.error("Tipo esperado ('int', 'float' ou 'string')")

    def parse_bloco(self):
        """<bloco> -> '{' <stmtList> '}' ;"""
        self.match('{')
        self.parse_stmtList()
        self.match('}')

    def parse_stmtList(self):
        """<stmtList> -> <stmt> <stmtList> | & ;"""
        while self.token_atual and self.is_first_of_stmt():
            self.parse_stmt()
        # epsilon é permitido

    def is_first_of_stmt(self):
        """Verifica se o token atual pode iniciar uma instrução."""
        primeiro_token = {
            'for', 'system', 'while', 'if', '{', 'break', 'continue',
            'int', 'float', 'string', 'IDENT', ';'
        }
        tipo_atual = self.get_tipo_token(self.token_atual)
        return tipo_atual in primeiro_token

    def parse_stmt(self):
        """<stmt> -> várias alternativas conforme a gramática."""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual == 'for':
            self.parse_forStmt()
        elif tipo_atual == 'system':
            self.parse_ioStmt()
        elif tipo_atual == 'while':
            self.parse_whileStmt()
        elif tipo_atual == 'if':
            self.parse_ifStmt()
        elif tipo_atual == '{':
            self.parse_bloco()
        elif tipo_atual == 'break':
            self.avanca()
            self.match(';')
        elif tipo_atual == 'continue':
            self.avanca()
            self.match(';')
        elif tipo_atual in ('int', 'float', 'string'):
            self.parse_declaracao()
        elif tipo_atual == 'IDENT':
            # Verifica se é uma atribuição
            next_tipo_token = self.get_tipo_token(self.tokens[self.pos + 1]) if (self.pos + 1) < len(self.tokens) else None
            if next_tipo_token in ('=', '+=', '-=', '*=', '/=', '%='):
                self.parse_atrib()
                self.match(';')
            else:
                self.parse_expr()
                self.match(';')
        elif tipo_atual == ';':
            self.avanca()
        else:
            self.error("Instrução não é válida")
            
    def parse_atrib(self):
        """<atrib> -> 'IDENT' <opAtrib> <expr>"""
        self.match('IDENT')
        self.parse_opAtrib()
        self.parse_expr()
        
    def parse_opAtrib(self):
        """<opAtrib> -> '=' | '+=' | '-=' | '*=' | '/=' | '%='"""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('=', '+=', '-=', '*=', '/=', '%='):
            self.avanca()
        else:
            self.error("Operador de atribuição esperado")
  
    def parse_declaracao(self):
        """<declaracao> -> <type> <lista_declarador_iniciado> ';' ;"""
        self.parse_type()
        self.parse_lista_declarador_iniciado()  
        self.match(';')
        
    def parse_lista_declarador_iniciado(self):
        """<lista_declarador_iniciado> -> <declaracao_inicial> {',' <declaracao_inicial>}"""
        self.parse_declaracao_inicial()
        while self.get_tipo_token(self.token_atual) == ',':
            self.avanca()
            self.parse_declaracao_inicial()

    def parse_declaracao_inicial(self):
        """<declaracao_inicial> -> 'IDENT' [ '=' <expr> ]"""
        self.match('IDENT')
        if self.get_tipo_token(self.token_atual) == '=':
            self.avanca()
            self.parse_expr()
     
    def parse_identList(self):
        """<identList> -> 'IDENT' <restoIdentList> ;"""
        self.match('IDENT')
        self.parse_restoIdentList()

    def parse_restoIdentList(self):
        """<restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;"""
        while self.get_tipo_token(self.token_atual) == ',':
            self.avanca()
            self.match('IDENT')

    def parse_forStmt(self):
        """<forStmt> -> 'for' '(' <optAtrib> ';' <optExpr> ';' <optAtrib> ')' <stmt> ;"""
        self.match('for')
        self.match('(')
        
        self.parse_optAtrib()  # Primeiro componente
        self.match(';')
        
        self.parse_optExpr()  # Segundo componente
        self.match(';')

        self.parse_optAtrib()  # Terceiro componente
        self.match(')')
        
        self.parse_stmt()  # Corpo do for


    def parse_optAtrib(self):
        """<optAtrib> -> <atrib> | & ;"""
        if self.get_tipo_token(self.token_atual) in ('int', 'float', 'string'):
            self.parse_declaracao()
        
        elif self.get_tipo_token(self.token_atual) == 'IDENT':
            self.parse_atrib()
            # print(self.token_atual)
        
        else:
            pass  # Produção vazia



    def parse_atrib(self):
        """<atrib> -> 'IDENT' <opAtrib> <expr> ;"""
        self.match('IDENT')  # Identificador
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('=', '+=', '-=', '*=', '/=', '%='):
            self.avanca()  # Avança o operador de atribuição
            self.parse_expr()  # Analisa a expressão
        else:
            self.error("Operador de atribuição esperado")


    def parse_optExpr(self):
        """<optExpr> -> <expr> | & ;"""
        if self.primeiro_expr():
            self.parse_expr()
        else:
            self.parse_expr()


    def primeiro_expr(self):
        """Verifica se o token atual pode iniciar uma expressão."""
        primeiro_token = {
            'IDENT', 'NUMint', 'NUMfloat', 'NUMoct', 'NUMhex', 'STR',
            '+', '-', '!', '('
        }
        tipo_atual = self.get_tipo_token(self.token_atual)
        return tipo_atual in primeiro_token


    def parse_expr(self):
        """<expr> -> <or> ;"""
        self.parse_or()

    def parse_or(self):
        """<or> -> <and> <restoOr> ;"""
        self.parse_and()
        self.parse_restoOr()

    def parse_restoOr(self):
        """<restoOr> -> '||' <and> <restoOr> | & ;"""
        while self.get_tipo_token(self.token_atual) == '||':
            self.avanca()
            self.parse_and()

    def parse_and(self):
        """<and> -> <not> <restoAnd> ;"""
        self.parse_not()
        self.parse_restoAnd()

    def parse_restoAnd(self):
        """<restoAnd> -> '&&' <not> <restoAnd> | & ;"""
        while self.get_tipo_token(self.token_atual) == '&&':
            self.avanca()
            self.parse_not()

    def parse_not(self):
        """<not> -> '!' <not> | <rel> ;"""
        if self.get_tipo_token(self.token_atual) == '!':
            self.avanca()
            self.parse_not()
        else:
            self.parse_rel()

    def parse_rel(self):
        """<rel> -> <add> <restoRel> ;"""
        self.parse_add()
        self.parse_restoRel()

    def parse_restoRel(self):
        """<restoRel> -> operadores relacionais ou vazio."""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('==', '!=', '<', '<=', '>', '>='):
            self.avanca()
            self.parse_add()
        # Produção vazia (epsilon) é permitida

    def parse_add(self):
        """<add> -> <mult> <restoAdd> ;"""
        self.parse_mult()
        self.parse_restoAdd()

    def parse_restoAdd(self):
        """<restoAdd> -> '+' <mult> <restoAdd> | '-' <mult> <restoAdd> | & ;"""
        while self.get_tipo_token(self.token_atual) in ('+', '-'):
            self.avanca()
            self.parse_mult()

    def parse_mult(self):
        """<mult> -> <uno> <restoMult> ;"""
        self.parse_uno()
        self.parse_restoMult()

    def parse_restoMult(self):
        """<restoMult> -> '*' <uno> <restoMult> | '/' <uno> <restoMult> | '%' <uno> <restoMult> | & ;"""
        while self.get_tipo_token(self.token_atual) in ('*', '/', '%', '/*'):
            self.avanca()
            self.parse_uno()        

    def parse_uno(self):
        """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('+', '-'):
            self.avanca()
            self.parse_uno()
        else:
            self.parse_fator()

    def parse_fator(self):
        """<fator> -> várias possibilidades de fator."""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('NUMint', 'NUMfloat', 'NUMoct', 'NUMhex', 'IDENT', 'STR'):
            self.avanca()
        elif tipo_atual == '(':
            self.avanca()
            self.parse_expr()
            self.match(')')
        else:
            #print par ver oq ta cehgadno
            self.error(f"Fator inválido '{self.token_atual}'")

    def parse_ioStmt(self):
        """<ioStmt> -> comandos de entrada/saída."""
        self.match('system')
        self.match('.')
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual == 'out':
            self.avanca()
            self.match('.')
            self.match('print')
            self.match('(')
            self.parse_outList()
            self.match(')')
            self.match(';')
        elif tipo_atual == 'in':
            self.avanca()
            self.match('.')
            self.match('scan')
            self.match('(')
            self.parse_type() # ve se é int, float ou string
            self.match(',')
            self.match('IDENT')
            self.match(')')
            self.match(';')
        else:
            self.error("Esperado 'out' ou 'in' após 'system.'")

    def parse_outList(self):
        """<outList> -> <out> <restoOutList> ;"""
        self.parse_out()
        self.parse_restoOutList()

    def parse_out(self):
        """<out> -> 'STR' | 'IDENT' | números ;"""
        tipo_atual = self.get_tipo_token(self.token_atual)
        if tipo_atual in ('STR', 'IDENT', 'NUMint', 'NUMfloat', 'NUMoct', 'NUMhex'):
            self.avanca()
        else:
            self.error(f"Elemento inválido em outList: '{self.token_atual}' (tipo: {tipo_atual})")

    def parse_restoOutList(self):
        """<restoOutList> -> ',' <out> <restoOutList> | & ;"""
        while self.get_tipo_token(self.token_atual) == ',':
            self.avanca()
            self.parse_out()

    def parse_whileStmt(self):
        """<whileStmt> -> 'while' '(' <expr> ')' <stmt> ;"""
        self.match('while')
        self.match('(')
        self.parse_expr()
        self.match(')')
        self.parse_stmt()

    def parse_ifStmt(self):
        """<ifStmt> -> 'if' '(' <expr> ')' <stmt> <elsePart> ;"""
        self.match('if')
        self.match('(')
        self.parse_expr()
        self.match(')')
        self.parse_stmt()
        self.parse_elsePart()

    def parse_elsePart(self):
        """<elsePart> -> 'else' <stmt> | & ;"""
        if self.get_tipo_token(self.token_atual) == 'else':
            self.avanca()
            self.parse_stmt()
        #epsilon é permitido

# Função de entrada
def parse_function_star(tokens):
    parser = Parser(tokens)
    parser.parse_function_star()