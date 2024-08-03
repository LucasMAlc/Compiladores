import ply.lex as lex
import ply.yacc as yacc

class BlackjackParser:
    # Definição dos tokens disponíveis no parser
    tokens = [
        'INT', 'ID', 'PLUS', 'MINUS', 'EQUALS',
        'DOUBLE', 'SPLIT', 'HIT'
    ]

    # Expressões regulares para operadores
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_EQUALS = r'\='

    # Expressões regulares para comandos de jogo
    t_DOUBLE = r'double'
    t_SPLIT = r'split'
    t_HIT = r'hit'

    # Caracteres que serão ignorados pelo lexer
    t_ignore = r''

    # Definição do token INT, que representa números inteiros
    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Definição do token ID, que representa identificadores (variáveis)
    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        t.type = 'ID'
        return t

    # Tratamento de erros no léxico
    def t_error(self, t):
        print("Illegal characters!")
        t.lexer.skip(1)

    # Inicialização do lexer e parser
    def __init__(self):
        self.env = {}  # Dicionário para armazenar variáveis
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    # Definição da precedência dos operadores
    precedence = (
        ('left', 'PLUS', 'MINUS'),
    )

    # Regras gramaticais para o parser

    # Regra principal que define como expressões ou ações são processadas
    def p_print(self, p):
        '''
        print : E
              | empty
              | action
        '''
        if p[1]:
            print(self.run(p[1]))

    # Regra para uma expressão do tipo 'R = S'
    def p_E(self, p):
        '''
        E : R EQUALS S
        '''
        p[0] = ('=', p[1], p[3])

    # Regra para identificar uma variável
    def p_R(self, p):
        '''
        R : ID
        '''
        p[0] = p[1]

    # Regra para uma expressão do tipo 'L - F'
    def p_S(self, p):
        '''
        S : L MINUS F
        '''
        p[0] = (p[2], p[1], p[3])

    # Regra para uma expressão do tipo 'F + L'
    def p_F(self, p):
        '''
        F : F PLUS L
        '''
        p[0] = (p[2], p[1], p[3])

    # Regra para um termo simples 'L'
    def p_F_L(self, p):
        '''
        F : L
        '''
        p[0] = p[1]

    # Regra para identificar um número inteiro
    def p_L(self, p):
        '''
        L : INT
        '''
        p[0] = p[1]

    # Regra para identificar uma ação no jogo
    def p_action(self, p):
        '''
        action : DOUBLE
               | SPLIT
               | HIT
        '''
        p[0] = p[1]

    # Tratamento de erros sintáticos
    def p_error(self, p):
        print('Syntax error found!')

    # Regra para lidar com entradas vazias
    def p_empty(self, p):
        '''
        empty :
        '''
        p[0] = None

    # Função que executa as operações interpretadas pelo parser
    def run(self, p):
        if type(p) == tuple: 
            if p[0] == '+':
                return self.run(p[1]) + self.run(p[2])
            elif p[0] == '-':
                return self.run(p[1]) - self.run(p[2])
            elif p[0] == '=':
                self.env[p[1]] = self.run(p[2])
        elif p == 'double':
            print("Jogador escolheu dobrar a aposta!")
        elif p == 'split':
            print("Jogador escolheu dividir as cartas!")
        elif p == 'hit':
            print("Jogador escolheu comprar uma carta!")
        else:
            return p

    # Método para iniciar o processo de parsing
    def parse(self, data):
        self.parser.parse(data)
