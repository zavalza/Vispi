# ------------------------------------------------------------
# patito.py
#
# scanner and parser for a simple language
# ------------------------------------------------------------
import ply.lex as lex

reserved = {
   'PROGRAM' : 'PROGRAM',
   'CAM' : 'CAM',
   'webcam' : 'WEBCAM',
   'picam': 'PICAM',
   'INPUT' : 'INPUT',
   'OUTPUT': 'OUTPUT',
   'PWM': 'PWM',
   'BOOL': 'bool',
   'VOID': 'void',
   'INT':'int',
   'FLOAT': 'float',
   'CHAR': 'char',
   'STRING':'string',
   'IMAGE':'image',
   'IF' : 'if',
   'ELSE' : 'else',
   'PRINT' : 'print',
   'int' : 'INT',
   'float' : 'FLOAT',
}
# List of token names.
tokens = [
    'ID',
    'CONSTANTE_I',
    'CONSTANTE_F',
    'CONSTANTE_STRING',
    'PUNTO_Y_COMA',
    'DOS_PUNTOS',
    'COMA',
    'IGUAL',
    'MAS',
    'MENOS',
    'ASTERISCO',
    'DIAGONAL',
    'MAYOR_QUE',
    'MENOR_QUE',
    'MAYOR_MENOR',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_CONSTANTE_F(t):
    r'(\d+)(\.)(\d+)'
    t.value = float(t.value)
    return t

def t_CONSTANTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_CONSTANTE_STRING = r'\"[^\n"]+\"'

#literals = [+','-','*','/']
t_PUNTO_Y_COMA = r';'
t_DOS_PUNTOS = r':'
t_COMA = r','
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_ASTERISCO = r'\*'
t_DIAGONAL = r'\/'
t_MAYOR_QUE = r'>'
t_MENOR_QUE = r'<'
t_MAYOR_MENOR = r'<>'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex(debug=0)

# # Build the lexer
# lexer = lex.lex()

# ### Test the parser####
# data = '''
# PROGRAM test ; int
# IF ( x > 4.0) { x = x + 1; }  ELSE {  x = x - 1;};}
# '''

# # Give the lexer some input
# lexer.input(data)

# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     print tok

