import argparse

# configuracion del parser para tomar argumentos por linea de comandos
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--semilla', help="semilla con la que se van a generar los numeros")
parser.add_argument('-c', '--constc', help="constante 'C' con la que ejecutar el generador. Dejar en blanco para metodo congruencial multiplicativo")
parser.add_argument('-a', '--consta', help="constante 'A' con la que ejecutar el generador")
parser.add_argument('-m', '--constm', help="constante 'M' con la que ejecutar el generador")

args = parser.parse_args()

# inicializacion de variables
flagGeneracionGuiada = False
A = 0.0
M = 0.0
C = 0.0
s = 0.0

# toma de variables en caso de que se hayan pasado por parametros
if args.semilla is None and args.constc is None and args.constm is None and args.consta is None:
	flagGeneracionGuiada = True
elif args.semilla is not None and args.consta is not None and args.constm is not None:
	A = float(args.consta)
	M = float(args.constm)
	s = float(args.semilla)
	if args.constc is not None or args.constc != "0":
		C = float(args.constc)


# toma de variables en caso de que no se hayan pasado por parametros
if flagGeneracionGuiada:
	s = float(input("Ingrese la semilla: "))
	M = float(input("Ingrese la constante M: "))
	A = float(input("Ingrese la constante A: "))
	C = float(input("Ingrese la constante C: "))

if C == 0:
	print("usando método congruencial multiplicativo")
else:
	print("usando método congruencial mixto")