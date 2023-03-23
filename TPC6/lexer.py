import ply.lex as lex

# Lista de tokens
tokens = [
    'INT', 'FUNCTION', 'PROGRAM', 'IDENTIFIER', 'LB', 'RB',
    'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'FROMTO', 'COM',
    'SEMICOLON', 'COMMA', 'EQUALS', 'PLUS', 'MINUS', 'SMCOM', 'MCOM', 'EMCOM',
    'TIMES', 'DIVIDE', 'GREATER', 'LESS', 'GREATEREQUAL',
    'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'IF', 'WHILE', 'PRINT',
]

t_LB = r'\('
t_RB = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_COMMA = r','
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_EQUAL = r'=='
t_NOTEQUAL = r'!='


def t_FROMTO(t):
    r'\.\.'
    return t

def t_INT(t):
    r'\d+'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_IF(t):
    r'if'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_COM(t):
    r'//[ \w\+\-\.\,\;]+'
    return t

def t_SMCOM(t):
    r'/\*[ \w\.\,\+\-\:]*'
    return t

def t_MCOM(t):
    r'--[ \w\.\,\+\-\;]*'
    return t

def t_EMCOM(t):
    r'[ \w\.\,\+\-\;]*\*/'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z]\w*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços em branco e tabulações
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()

# Testar com um arquivo de exemplo
with open("exemplo1.p", "r") as f:
    lexer.input(f.read())

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
