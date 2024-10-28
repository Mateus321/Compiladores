def tratar_erros(token):
    # Verifica se o token contém múltiplos pontos ou termina com um ponto, o que indica um número mal formatado
    if token.count(".") > 1 or token.endswith("."):
        # Dividir o token por pontos e verificar se cada parte é um dígito
        partes = token.split(".")
        if any(not parte.isdigit() for parte in partes if parte):  # Ignora partes vazias e verifica se todas são dígitos
            return [f"Erro de número mal formatado: '{token}' - múltiplos pontos ou ponto no final."]
    
    # Verifica se o token é um número misturado com letras
    if any(char.isdigit() for char in token) and any(char.isalpha() for char in token):
        return [f"Erro de número misturado com letras: '{token}'"]

    # Se nenhum erro foi encontrado
    return []

def verificar_string(f, string_token, linha_atual, col_atual):
    while True:
        prox_caractere = f.read(1)
        if not prox_caractere:  # Verifica final do arquivo sem fechar string
            print(f"Erro encontrado: Erro de string não fechada: {string_token}")
            return None  # Indica erro
        string_token += prox_caractere
        if prox_caractere == '"':  # Fecha a string
            print(
                f"[ STRING, '{string_token}', Linha: {linha_atual}, Coluna: {col_atual} ]"
            )
            return string_token  # Retorna a string bem formada
