from ply import *
import vispi_lex

tokens = vispi_lex.tokens
counter_modules = 0 #Will be the key to explore module dictionaries
counter_variables = 0 #Will be the key to explore variable dictionaries
module_variables={0:[]}
module_names = {0:'global'}
variable_names = {0:0}
variable_types = {0:0}


#Grammatic rules
def p_program(p):
    'program : PROGRAM ID NEWLINE hardware vars assign functions'
    print "programa exitoso"
    print module_variables
    print module_names
    print variable_names
    print variable_types

def p_empty(p):
    'empty :'
    pass

def p_hardware(p):
	'hardware : camDeclaration inputsDeclaration outputsDeclaration pwmDeclaration'

def p_camDeclaration(p):
    '''camDeclaration : empty
				      | CAM WEBCAM COLON ID NEWLINE
                      | CAM PICAM COLON ID NEWLINE'''

def p_inputsDeclaration(p):
    '''inputsDeclaration : empty
					     | INPUT saveType pinList NEWLINE'''

def p_ouputsDeclaration(p):
    '''outputsDeclaration : empty
					      | OUTPUT saveType pinList NEWLINE'''

def p_pwmDeclaration(p):
    '''pwmDeclaration : empty
				      | PWM saveType pinList NEWLINE'''

def p_pinList(p):
    '''pinList : C_INT COLON ID
               | C_INT COLON ID COMMA pinList'''
    global counter_variables
    module_variables[counter_modules].append(p[3])
    variable_names[counter_variables] = p[3]      
    counter_variables += 1

def p_vars(p):
    '''vars : tipo saveType idList NEWLINE vars
            | tipo saveType assign vars
            | empty'''

def p_saveType(p):
    'saveType :'
    if((p[-1]=='INPUT')or(p[-1]=='OUTPUT')):
        variable_types[counter_variables]= 'BOOL'
    if(p[-1]=='PWM'):
        variable_types[counter_variables]= 'INT'

def p_idList(p):
    '''idList : ID
              | ID COMMA idList'''

def p_tipo(p):
    '''tipo : BOOL
            | INT
            | FLOAT
            | CHAR
            | STRING
            | IMAGE'''

def p_functions(p):
    '''functions : DEF tipo ID LPAREN RPAREN COLON NEWLINE block functions
                 | DEF tipo ID LPAREN tipo ID parameterList RPAREN COLON NEWLINE block functions
                 | DEF VOID ID LPAREN RPAREN COLON NEWLINE block functions
                 | DEF VOID ID LPAREN tipo ID parameterList RPAREN COLON NEWLINE block functions
                 | DEF VOID MAIN LPAREN RPAREN COLON NEWLINE block functions
                 | DEF VOID MAIN LPAREN tipo ID parameterList RPAREN COLON NEWLINE block functions
                 | empty'''

def p_parameterList(p):
    '''parameterList : empty
                     | COMMA tipo ID parameterList'''

def p_assign(p):
    '''assign : idList EQUAL expression NEWLINE assign
              | empty'''

# def p_main(p):
#     '''main : DEF VOID MAIN LPAREN RPAREN COLON NEWLINE block 
# 			| DEF VOID MAIN LPAREN tipo ID parameterList RPAREN COLON NEWLINE block'''

def p_block(p):
    '''block : empty
             | TAB statement moreStatements'''

def p_moreStatements(p):
    '''moreStatements : empty
                      | TAB statement moreStatements'''

def p_statement(p):
    '''statement : vars 
                 | assign
                 | condition
                 | cycle
                 | funct NEWLINE
                 | RETURN expression NEWLINE'''

def p_condition(p):
    '''condition : IF expression COLON NEWLINE block
                 | IF expression COLON NEWLINE block ELSE COLON NEWLINE block'''

def p_cycle(p):
    '''cycle : WHILE expression COLON NEWLINE block
             | DO COLON NEWLINE block WHILE expression NEWLINE'''

def p_funct(p):
    '''funct : ID LPAREN RPAREN
             | ID LPAREN expression expressionList RPAREN'''

def p_expressionList(p):
    '''expressionList : empty
                      | COMMA expression expressionList'''

def p_expression(p):
    '''expression : exp
                  | exp compareToken exp'''

def p_compareToken(p):
    '''compareToken : GREATER_THAN
                    | LESS_THAN
                    | LESS_EQUAL_THAN
                    | GREATER_EQUAL_THAN
                    | NOT_EQUAL_THAN
                    | SAME_AS'''

def p_exp(p):
    'exp : term moreTerms'

def p_moreTerms(p):
    '''moreTerms : empty
                 | PLUS term moreTerms
                 | MINUS term moreTerms'''

def p_term(p):
    'term : factor moreFactors'

def p_moreFactors(p):
    '''moreFactors : empty
                   | DIVIDE factor moreFactors
                   | TIMES factor moreFactors
                   | MOD factor moreFactors'''

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | cvar
              | funct'''

def p_cvar(p):
    '''cvar : ID
            | C_BOOL
            | C_INT
            | C_FLOAT
            | C_CHAR
            | C_STRING'''


### Following code is Little Duck code ###

def p_error(p):
    if p:
        print("Syntax error at '%s'" %(p.value))
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def parse(data):
    parser.error = 0
    p = parser.parse(data, debug=1, tracking=True)
    if parser.error: return None
    return p

# while 1:
#     try:
#         s = raw_input('calc > ')
#     except EOFError:
#         break
#     if not s: continue
#     yacc.parse(s)line
