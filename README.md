# Analisador Léxico (Parser)

## Descrição

Este projeto é fruto da disciplina de Compiladores do curso de graduação em Engenharia de Computação do Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG) campus Leopoldina. Ele consiste em um analisador léxico (lexer) que faz parte de um compilador. O analisador léxico desenvolvido em Python será responsável por ler cada caractere do arquivo em Java-- e dividir o texto em tokens, que são as unidades essenciais do código.

## Funcionalidades

- Identificação de operadores aritméticos, lógicos, relacionais e de atribuição;
- Reconhecimento de símbolos aceitos e palavras reservadas;
- Tratamento de strings, caracteres especias, números inteiros, floats, negativos, octais e hexadecimais;
- Suporte para identificadores (variáveis);
- Tratamento de tokens não conhecidos;
- Identificação de Lexema, linha e coluna;
- Execução via terminal
- entre outros...

## Estrutura do Projeto

## `AnalisadorArquivo.py`

Este arquivo tem a lógica principal para ler o arquivo java -- , identificar tokens e encontrar alguns erros.

As funções mais usadas neste arquivo são:

- **`open()`** e **`read()`**: Abrem e leem o arquivo caractere a caractere para construir os tokens e processar cada um.
- **`print()`**: Exibe os tokens e possíveis erros no console, mostrando o tipo do token, valor e posição no arquivo (linha e coluna).
- **`isdigit()`** e **`isspace()`**: Verificam se o caractere é um número ou um espaço, assim ajuda a identificar números e ignorar espaços em branco.
- **`replace()`**: Remove temporariamente o ponto em números para validar a estrutura de decimais.
- **`seek()`** e **`tell()`**: Controlam o ponteiro de leitura no arquivo. Se for necessário voltar um caractere, `seek()` usa a posição atual obtida com `tell()`.

## `TipoToken.py`

Este arquivo define a função `token_type`, que identifica o tipo de um token ou palavra no código fonte. Ele utiliza `Biblioteca.py` para determinar o tipo, verificando se o token está nela.

- **`token_type(word)`**: Essa é a função principal que vai identificar o tipo de um token e retornar o tipo correspondente ao token com base nas verificações:

  - **Números Decimais**: Se tem ponto e tem somente dígitos, é identificado como decimal.
  - **Operadores e Palavras Reservadas**: Verifica se o token está nos operadores aritméticos, lógicos, relacionais, de atribuição, ou nas palavras reservadas.
  - **Números Octais**: Começa com `0` e tem apenas dígitos de `0` a `7`.
  - **Números Hexadecimais**: Começa com `0x` e tem dígitos ou letras de `a` a `f`.
  - **Variável**: Caso não seja operador nem palavra reservada, é uma variável.
  - **Erro de Variável Inválida**: Se começa com um dígito, é tratado como erro.

## `tratar_erros.py`:

Este arquivo tem três funções importante que verificam os tokens e as strings para ver os erros, as funções sao usadas principalmente no `AnalisadorArquivo.py`.

As funções mais usadas neste arquivo são:

1. **`multi_pontos(token)`**:

   - Vai verificar se o token tem mais de um ponto (`.`) e ai indica um número mal formatado.
   - Se tem múltiplos pontos, mostra um erro informando o problema.

2. **`verificar_token(token)`**:

   - Vai verificar o formato do token para identificar se é hexadecimal ou misturado.
   - **Hexadecimal**: Se o caracter comecar com `0x`, vai verificar se todos os caracteres seguintes são válidos em hexadecimal (`0-9` e `A-F`), ai retorna uma mensagem de token válido ou erro de formato.
   - **Misto (letras e números)**: Se o token contém tanto letras quanto números, ele é valido, se nao, vai retornar um erro indicando que o token deve misturar letras e números.

3. **`verificar_string(f, string_token, linha_atual, col_atual)`**:
   - Lê a string entre aspas (`"`), ai vai garantir que ela seja fechada.
   - Verifica o final do arquivo ou ponto e vírgula (`;`) sem fechar a string, retornando um erro nesses casos.
   - Vai retornar a string corretamente formatada ou um erro, mostrando a linha e coluna do erro

- `Biblioteca.py`: Este arquivo vai definir a biblioteca de constantes que basicamente armazena os tokens básicos que vao ser usados no analisador léxico, cada constante vai representar um tipo de categoria e associa o símbolo a um número que vai identificar ele.

Constantes Usadas:

1. **OPERADOR_ARITMETICO**: Tem os operadores aritméticos básicos (`+`, `-`, `*`, `/`, `%`), nomeando como(`1`, `2`,`3`, `4`,`5`).

2. **OPERADOR_LOGICO**: Tem os operadores lógicos (`||`, `&&`, `!`), nomeando como (`6`, `7`, `8`).

3. **OPERADOR_RELACIONAL**: Tem os operadores relacionais (`==`, `!=`, `>`, `>=`, `<`, `<=`), nomeando como (`9`, `10`, `11`, `12`, `13`, `14`).

4. **OPERADOR_ATRIBUICAO**: Tem os operadores de atribuição (`=`, `+=`, `-=`, `*=`, `/=`, `%=`), nomeando como (`15`, `16`, `17`, `18`, `19`, `20`).

5. **PALAVRAS_RESERVADAS**: Tem as palavras reservadas da linguagem, como (`int`, `float`, `string`, `for`, `while`, `break`, `continue`, `if`, `else`, `return`, `system`, `out`, `print`, `in`, `scan`), nomeando como (`21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `32`, `33`, `34`, `35`).

6. **SIMBOLOS_ACEITOS**: Tem os símbolos aceitos na linguagem, como (`;`, `,`, `{`, `}`, `(`, `)`, `.`), nomeando como (`36`, `37`, `38`, `39`, `40`, `41`, `42`).

O arquivo também tem comentários que mostram de forma pratica o identificador e o tipo dele.

- `arqTeste.java`: Este é um exemplo de código Java-- completo para o analisador Léxico, estruturas de controle (`for`, `if-else`, `while`), operadores aritméticos e lógicos, diferentes tipos de números e comandos de entrada e saída. Cada parte do código mostra tokens que o analisador léxico reconhece, como:

- **Tipos de dados** (`int`, `float`, `string`)
- **Operadores** (`+`, `-`, `*`, `/`, `%`, `&&`, `||`)
- **Palavras reservadas** (`for`, `if`, `else`, `while`, `system`, `print`, `scan`)
- **Números variados** (decimal, octal `0123`, hexadecimal `0x7B`, float `123.45`)

## Como Utilizar o Analisador Léxico

1. Primeiro, você vai precisar de um ambiente para rodar o projeto. Recomendamos usar o **VSCode**.
2. Depois, instale o **Python** e o **Git** na sua máquina, você pode fazer pesquisar sobre em: https://www.python.org/downloads/ e https://git-scm.com/downloads
3. Com o Python e Git instalado, clone o repositório do GitHub. No terminal, digite: `git clone https://github.com/Mateus321/Compiladores.git`
4. Para executar o analisador, abra o terminal e digite: `python main.py arqTeste.java`
5. Isso vai mostrar a análise do código no terminal. Um arquivo de teste (`arqTeste.java`) já está incluído, mas você pode usar qualquer outro arquivo seguindo o mesmo padrão: `python main.py nomedoseuarquivo.java`
