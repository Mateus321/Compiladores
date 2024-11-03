int x = 1;                   // Declaração de variável inteira
float y = 2.5;               // Declaração de variável flutuante
string msg = "Hello, World!"; // Declaração de variável string

// Estruturas de repetição e condicionais
for (int i = 0; i < 10; i += 1) {
    if (i == 5) {
        continue;            // Pula a iteração atual
    } else {
        x = x + i;
    }
}

// Operações aritméticas
x = x + (-15) / 5 + 1;
y = y * 3.14 % 2.0;

// Operadores lógicos
if (x != 0 && y > 1 || msg == "/Hello") {
    x = x - 1;
}

// Números em diferentes formatos
int decimal = 123;
int octal = 0123;            // Número octal
int hexadecimal = 0x7B;      // Número hexadecimal
float decimalFloat = 123.45; // Número flutuante
float decimalFloat2 = 123.;  // ESSE AINDA TA FALTANDO TRATAR

// Entrada e saída
system.out.print("Digite um valor: ");
int input = system.in.scan();

// Estrutura de repetição while
while (x != 0) {
    x = x - (-15.15) / 5 + 1;
    // comentário
}

// Outros operadores de atribuição
x += 5;
y -= 2.5;
x *= 2;
y /= 3.0;
x %= 10;

// Delimitadores e separadores
{ ; , . }
