from ply import *
import patito_lex

tokens = patito_lex.tokens


#Grammatic rules
def p_program(p):
    'program : PROGRAM ID NEWLINE hardware sectionOfVariables sectionOfAssigments	sectionOfFuntions main'
    print "Great, programm was sucessfull!"

def p_empty(p):
    'empty :'
    pass

def p_hardware(p):
	'hardware : camDeclaration inputsDeclaration outputsDeclaration pwmDeclaration '

def p_camDeclaration(p):
'''camDeclaration : empty
				  | CAM WEBCAM COLON ID NEWLINE
                  | CAM PICAM COLON ID NEWLINE'''

def p_inputsDeclaration(p):
'''inputsDeclaration : empty
					 | INPUT pinList NEWLINE'''

def p_ouputsDeclaration(p):
'''outputsDeclaration : empty
					  | OUTPUT pinList NEWLINE'''

def p_pwmDeclaration(p):
'''pwmDeclaration : empty
				  | PWM pinList NEWLINE'''

def p_pinList(p):
'''pinList : C_INT COLON ID
           | C_INT COLON ID COMMA pinList'''


#####Little Duck Codee####

def p_codigo(p):
    '''codigo : bloque
              | variables bloque'''

def p_variables(p):
    'variables : VAR declaracion'

def p_declaracion(p):
    '''declaracion : ID mas_ids DOS_PUNTOS tipo PUNTO_Y_COMA declaracion
                    | empty '''

def p_mas_ids(p):
    '''mas_ids : empty
                | COMA ID mas_ids'''

def p_tipo(p):
    '''tipo : INT
            | FLOAT'''

def p_bloque(p):
    'bloque : LLAVE_IZQ estatuto LLAVE_DER'

def p_estatuto(p):
    '''estatuto : empty
                | asignacion estatuto
                | condicion estatuto
                | escritura estatuto'''

def p_asignacion(p):
    'asignacion : ID IGUAL expresion PUNTO_Y_COMA'

def p_escritura(p):
    'escritura : PRINT PARENTESIS_IZQ evalua_e_imprime PARENTESIS_DER PUNTO_Y_COMA'

def p_evalua_e_imprime(p):
    '''evalua_e_imprime : expresion continua_imprime
                        | CONSTANTE_STRING continua_imprime'''
def p_continua_imprime(p):
    '''continua_imprime :  empty
                        | COMA evalua_e_imprime'''
def p_condicion(p):
    'condicion : IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque otra_condicion PUNTO_Y_COMA'

def p_otra_condicion(p):
    '''otra_condicion : empty
                        | ELSE bloque'''

def p_expresion(p):
    'expresion : exp mas_exp'

def p_exp(p):
    'exp :  termino mas_terminos'

def p_mas_exp(p):
    ''' mas_exp :  empty
          | MAYOR_QUE exp
          | MENOR_QUE exp
          | MAYOR_MENOR exp '''

def p_mas_terminos(p):
    '''mas_terminos : empty
                      | MAS exp
                      | MENOS exp'''

def p_termino(p):
    'termino : factor mas_factores'

def p_mas_factores(p):
    '''mas_factores : empty
                    | ASTERISCO termino
                    | DIAGONAL termino'''

def p_factor(p):
    '''factor : PARENTESIS_IZQ expresion PARENTESIS_DER
              | MAS var_cte
              | MENOS var_cte
              | var_cte'''

def p_var_cte(p):
    '''var_cte : ID
                | CONSTANTE_I
                | CONSTANTE_F'''

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def parse(data,debug=0):
    parser.error = 0
    p = parser.parse(data,debug=debug)
    if parser.error: return None
    return p

# while 1:
#     try:
#         s = raw_input('calc > ')
#     except EOFError:
#         break
#     if not s: continue
#     yacc.parse(s)