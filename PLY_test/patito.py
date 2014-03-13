import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import patito_lex
import patito_parse

# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# the other mode below
if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = patito_parse.parse(data)
    
else:
    patito_parse.parse("PROGRAM test ; VAR x : int ; { x = 5; IF ( x > 4.0) { x = x + 1; }  ELSE {  x = x - 1;};}")