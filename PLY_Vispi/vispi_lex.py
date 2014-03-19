# ------------------------------------------------------------
# Vispi_Lex.py
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
	'void':'VOID',
    'bool':'BOOL',
	'int':'INT',
	'float':'FLOAT',
	'char':'CHAR',
	'string':'STRING',
	'image':'IMAGE',
	'if':'IF',
    'else':'ELSE',
    'while':'WHILE',
    'do':'DO',
	'true':'TRUE',
	'false':'FALSE',
	'main' : 'MAIN',
	'return' : 'RETURN',
	'def' : 'DEF'
}
# List of token names.
tokens = [
    'ID',
	#Constants
	'C_BOOL',
    'C_INT',
    'C_FLOAT',
	'C_CHAR',
	'C_STRING',
	# Operators + - / * % > < <= >= != == && || ! 
	'PLUS',
	'MINUS',
	'DIVIDE',
	'TIMES',
	'MOD',
	'GREATER_THAN',
	'LESS_THAN',
	'LESS_EQUAL_THAN',
	'GREATER_EQUAL_THAN',
	'NOT_EQUAL_THAN',
	'SAME_AS',
	'AND',
	'OR',
	'NOT',
    # Assignment =
	'EQUAL',
	# Other Symbols ( ) , . : \t \n
	'LPAREN', 
	'RPAREN', 
	'COMMA',
	'PERIOD',
	'COLON',  
	'TAB',
	'NEWLINE',
] + list(reserved.values())

#Check these tokens first
t_ignore_COMMENT = r'\#.*'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_C_FLOAT(t):
    r'(\d+)(\.)(\d+)'
    t.value = float(t.value)
    return t

def t_C_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_C_BOOL = r'(true|false)'
t_C_CHAR = r'\'[^\']\''
t_C_STRING = r'\"[^\"]*\"'

# Operators
t_PLUS      	= r'\+'
t_MINUS         = r'-'
t_DIVIDE        = r'/'
t_MOD			= r'%'
t_TIMES         = r'\*'
t_GREATER_THAN          = r'>'
t_LESS_THAN				= r'<'
t_LESS_EQUAL_THAN		= r'<='
t_GREATER_EQUAL_THAN	= r'>='
t_NOT_EQUAL_THAN		= r'!='
t_SAME_AS				= r'=='
t_AND					= r'&&'
t_OR					= r'\|\|'
t_NOT					= r'!'

# Assignment operator
t_EQUAL         = r'='

# Delimeters
t_COMMA         = r'\,'
t_COLON         = r':'
t_PERIOD        = r'\.'
t_TAB 			=r'\t'
#t_NEWLINE		=r'\n+'

#Maybe we will need to define a rule to count tabs
#def t_TAB(t)
	#r'\t+'

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# A string containing ignored characters (spaces)
t_ignore  = ' '

# Error handling rule
def t_error(t):
    print "Illegal character '%s' in line '%s'" % (t.value[0],t.lexer.lineno)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex(debug=0)


### Test the parser####
# data = ''' PROGRAM primerTest
# CAM webcam : cam1
# INPUT 8 : boton1, 9: boton2
# OUTPUT 5: led1

# int elefante, paloma
# float tigre
# bool si_o_no

# int funcionextra(int parametro1)
# 	int otroAnimal
# 	otroAnimal = parametro1 - 1
# 	if (otroAnimal != 0)
# 		funcionextra(4)
# 	else 
# 		funcionextra(3)

# void main()
# 	string estoEsUnMensaje
#     char letra

# 	estoEsUnMensaje = "el elefante rosa corre en la pradera"
#     esteEsUnChar = 'a'

# 	print(estoEsUnMensaje)
# 	tigre = tigre + 5 * 8 - elefante / (si_o_no + 9)
# '''


# ##Test just the lexer###
# # # Give the lexer some input
# lexer.input(data)

# # # Tokenize
# while True:
# 	tok = lexer.token()
# 	if not tok: break      # No more input
# 	print tok


