#tokens = lista de toknes no lexer
#current_token = o token que ta sendo lido no meomento
#pos = posicao do token atual na lista
#advance = avanca para o proximo token
#get_token_type = pega o tipo do token
#match = verifica se o token atual é do tipo esperado e avanca
#error = lanca erro de sintaxe

from Biblioteca import (
    OPERADOR_ARITMETICO,
    OPERADOR_LOGICO,
    OPERADOR_RELACIONAL,
    OPERADOR_ATRIBUICAO,
    PALAVRAS_RESERVADAS,
    SIMBOLOS_ACEITOS,
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
        self.current_token = None  # Token atual (tupla)
        self.pos = -1  # Posição atual na lista de tokens
        self.advance()  # Avança para o primeiro token

    def advance(self):
        """Avança para o próximo token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None  # Fim dos tokens
                
    def get_token_type(self, token):
        """Obtém o tipo do token a partir do código do token."""
        if token is None:
            return None
        token_code = token[0]
        token_type = TOKEN_TYPE_MAPPING.get(token_code)
        if token_type is None:
            self.error(f"Código de token desconhecido: {token_code}")
        return token_type

    def get_token_value(self, token):
        """Obtém o valor do token."""
        if token is None:
            return None
        return token[1]

    def match(self, expected_type):
        """Verifica se o token atual é do tipo esperado e avança."""
        actual_type = self.get_token_type(self.current_token)
        if actual_type == expected_type:
            self.advance()
        else:
            expected_value = expected_type
            actual_value = actual_type if actual_type else 'EOF'
            self.error(f"Esperado '{expected_value}', encontrado '{actual_value}'")


    def error(self, message):
        """Lança uma exceção de erro de sintaxe."""
        line = self.current_token[2] if self.current_token else 'EOF'
        column = self.current_token[3] if self.current_token else ''
        raise Exception(f"Erro de sintaxe na linha {line}, coluna {column}: {message}")

    #aqui comeca as funcoes da gramatica 

    def parse_function_star(self):
        """<function*> -> <type> 'IDENT' '(' ')' <bloco> ;"""
        self.parse_type()
        self.match('IDENT')
        self.match('(')
        self.match(')')
        self.parse_bloco()
        if self.current_token is not None:
            self.error("Tokens extras após o fim da função")

    def parse_type(self):
        """<type> -> 'int' | 'float' | 'string' ;"""
        current_type = self.get_token_type(self.current_token)
        if current_type in ('int', 'float', 'string'):
            self.advance()
        else:
            self.error("Tipo esperado ('int', 'float' ou 'string')")

    def parse_bloco(self):
        """<bloco> -> '{' <stmtList> '}' ;"""
        self.match('{')
        self.parse_stmtList()
        self.match('}')

    def parse_stmtList(self):
        """<stmtList> -> <stmt> <stmtList> | & ;"""
        while self.current_token and self.is_first_of_stmt():
            self.parse_stmt()
        # epsilon é permitido

    def is_first_of_stmt(self):
        """Verifica se o token atual pode iniciar uma instrução."""
        first_tokens = {
            'for', 'system', 'while', 'if', '{', 'break', 'continue',
            'int', 'float', 'string', 'IDENT', ';'
        }
        current_type = self.get_token_type(self.current_token)
        return current_type in first_tokens

    def parse_stmt(self):
        """<stmt> -> várias alternativas conforme a gramática."""
        current_type = self.get_token_type(self.current_token)
        if current_type == 'for':
            self.parse_forStmt()
        elif current_type == 'system':
            self.parse_ioStmt()
        elif current_type == 'while':
            self.parse_whileStmt()
        elif current_type == 'if':
            self.parse_ifStmt()
        elif current_type == '{':
            self.parse_bloco()
        elif current_type == 'break':
            self.advance()
            self.match(';')
        elif current_type == 'continue':
            self.advance()
            self.match(';')
        elif current_type in ('int', 'float', 'string'):
            self.parse_declaration()
        elif current_type == 'IDENT':
            # Verifica se é uma atribuição
            next_token_type = self.get_token_type(self.tokens[self.pos + 1]) if (self.pos + 1) < len(self.tokens) else None
            if next_token_type in ('=', '+=', '-=', '*=', '/=', '%='):
                self.parse_atrib()
                self.match(';')
            else:
                self.parse_expr()
                self.match(';')
        elif current_type == ';':
            self.advance()
        else:
            self.error("Instrução não é válida")
            
    def parse_atrib(self):
        """<atrib> -> 'IDENT' <opAtrib> <expr>"""
        self.match('IDENT')
        self.parse_opAtrib()
        self.parse_expr()
        
    def parse_opAtrib(self):
        """<opAtrib> -> '=' | '+=' | '-=' | '*=' | '/=' | '%='"""
        current_type = self.get_token_type(self.current_token)
        if current_type in ('=', '+=', '-=', '*=', '/=', '%='):
            self.advance()
        else:
            self.error("Operador de atribuição esperado")
  
    def parse_declaration(self):
        """<declaration> -> <type> <initDeclaratorList> ';' ;"""
        # print("Entrou")
        self.parse_type()
        self.parse_initDeclaratorList()
        self.match(';')
        
    def parse_initDeclaratorList(self):
        """<initDeclaratorList> -> <initDeclarator> {',' <initDeclarator>}"""
        self.parse_initDeclarator()
        while self.get_token_type(self.current_token) == ',':
            self.advance()
            self.parse_initDeclarator()

    def parse_initDeclarator(self):
        """<initDeclarator> -> 'IDENT' [ '=' <expr> ]"""
        self.match('IDENT')
        if self.get_token_type(self.current_token) == '=':
            self.advance()
            self.parse_expr()
     
    def parse_identList(self):
        """<identList> -> 'IDENT' <restoIdentList> ;"""
        self.match('IDENT')
        self.parse_restoIdentList()

    def parse_restoIdentList(self):
        """<restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;"""
        while self.get_token_type(self.current_token) == ',':
            self.advance()
            self.match('IDENT')

    def parse_forStmt(self):
        """<forStmt> -> 'for' '(' <optAtrib> ';' <optExpr> ';' <optAtrib> ')' <stmt> ;"""
        self.match('for')
        self.match('(')
        self.parse_optAtrib()
        self.match(';')
        self.parse_optExpr()
        self.match(';')
        self.parse_optAtrib()
        self.match(')')
        self.parse_stmt()

    def parse_optAtrib(self):
        """<optAtrib> -> <atrib> | & ;"""
        if self.get_token_type(self.current_token) == 'IDENT':
            self.parse_atrib()
        # Produção vazia (epsilon) é permitida

    def parse_atrib(self):
        """<atrib> -> várias formas de atribuição."""
        self.match('IDENT')
        current_type = self.get_token_type(self.current_token)
        if current_type in ('=', '+=', '-=', '*=', '/=', '%='):
            self.advance()
            self.parse_expr()
        else:
            self.error("Operador de atribuição esperado")
            
    def parse_optExpr(self):
        """<optExpr> -> <expr> | & ;"""
        if self.is_first_of_expr():
            self.parse_expr()
        #epsilon é permitido

    def is_first_of_expr(self):
        """Verifica se o token atual pode iniciar uma expressão."""
        first_tokens = {
            'IDENT', 'NUMint', 'NUMfloat', 'NUMoct', 'NUMhex', 'STR',
            '+', '-', '!', '('
        }
        current_type = self.get_token_type(self.current_token)
        return current_type in first_tokens

    def parse_expr(self):
        """<expr> -> <or> ;"""
        self.parse_or()

    def parse_or(self):
        """<or> -> <and> <restoOr> ;"""
        self.parse_and()
        self.parse_restoOr()

    def parse_restoOr(self):
        """<restoOr> -> '||' <and> <restoOr> | & ;"""
        while self.get_token_type(self.current_token) == '||':
            self.advance()
            self.parse_and()

    def parse_and(self):
        """<and> -> <not> <restoAnd> ;"""
        self.parse_not()
        self.parse_restoAnd()

    def parse_restoAnd(self):
        """<restoAnd> -> '&&' <not> <restoAnd> | & ;"""
        while self.get_token_type(self.current_token) == '&&':
            self.advance()
            self.parse_not()

    def parse_not(self):
        """<not> -> '!' <not> | <rel> ;"""
        if self.get_token_type(self.current_token) == '!':
            self.advance()
            self.parse_not()
        else:
            self.parse_rel()

    def parse_rel(self):
        """<rel> -> <add> <restoRel> ;"""
        self.parse_add()
        self.parse_restoRel()

    def parse_restoRel(self):
        """<restoRel> -> operadores relacionais ou vazio."""
        current_type = self.get_token_type(self.current_token)
        if current_type in ('==', '!=', '<', '<=', '>', '>='):
            self.advance()
            self.parse_add()
        # Produção vazia (epsilon) é permitida

    def parse_add(self):
        """<add> -> <mult> <restoAdd> ;"""
        self.parse_mult()
        self.parse_restoAdd()

    def parse_restoAdd(self):
        """<restoAdd> -> '+' <mult> <restoAdd> | '-' <mult> <restoAdd> | & ;"""
        while self.get_token_type(self.current_token) in ('+', '-'):
            self.advance()
            self.parse_mult()

    def parse_mult(self):
        """<mult> -> <uno> <restoMult> ;"""
        self.parse_uno()
        self.parse_restoMult()

    def parse_restoMult(self):
        """<restoMult> -> '*' <uno> <restoMult> | '/' <uno> <restoMult> | '%' <uno> <restoMult> | & ;"""
        while self.get_token_type(self.current_token) in ('*', '/', '%'):
            self.advance()
            self.parse_uno()

    def parse_uno(self):
        """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
        current_type = self.get_token_type(self.current_token)
        if current_type in ('+', '-'):
            self.advance()
            self.parse_uno()
        else:
            self.parse_fator()

    def parse_fator(self):
        """<fator> -> várias possibilidades de fator."""
        current_type = self.get_token_type(self.current_token)
        if current_type in ('NUMint', 'NUMfloat', 'NUMoct', 'NUMhex', 'IDENT', 'STR'):
            self.advance()
        elif current_type == '(':
            self.advance()
            self.parse_expr()
            self.match(')')
        else:
            self.error("Fator inválido")

    def parse_ioStmt(self):
        """<ioStmt> -> comandos de entrada/saída."""
        self.match('system')
        self.match('.')
        current_type = self.get_token_type(self.current_token)
        if current_type == 'out':
            self.advance()
            self.match('.')
            self.match('print')
            self.match('(')
            self.parse_outList()
            self.match(')')
            self.match(';')
        elif current_type == 'in':
            self.advance()
            self.match('.')
            self.match('scan')
            self.match('(')
            self.parse_outList()
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
        current_type = self.get_token_type(self.current_token)
        if current_type in ('STR', 'IDENT', 'NUMint', 'NUMfloat', 'NUMoct', 'NUMhex'):
            self.advance()
        else:
            self.error("Elemento inválido em outList")

    def parse_restoOutList(self):
        """<restoOutList> -> ',' <out> <restoOutList> | & ;"""
        while self.get_token_type(self.current_token) == ',':
            self.advance()
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
        if self.get_token_type(self.current_token) == 'else':
            self.advance()
            self.parse_stmt()
        #epsilon é permitido

# Função de entrada
def parse_function_star(tokens):
    parser = Parser(tokens)
    parser.parse_function_star()