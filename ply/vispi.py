import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import vispi_lex
import vispi_parse

# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# the other mode below
if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = vispi_parse.parse(data)
    
else:
    vispi_parse.parse('''
    	PROGRAM primerTest
		CAM webcam : cam1
		INPUT 8 : boton1, 9: boton2
		OUTPUT 5: led1

		int elefante, paloma
		float tigre
		bool si_o_no

		int funcionextra(int parametro1)
			int otroAnimal
			otroAnimal = parametro1 - 1
			if (otroAnimal != 0)
				funcionextra(4)
			else 
				funcionextra(3)

		void main()
			string estoEsUnMensaje
		    char letra

			estoEsUnMensaje = "el elefante rosa corre en la pradera"
		    esteEsUnChar = 'a'

			print(estoEsUnMensaje)
			tigre = tigre + 5 * 8 - elefante / (si_o_no + 9)''')