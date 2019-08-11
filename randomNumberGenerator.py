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


# Metodo que calcula una cierta cantidad de numeros aleatorios
# con el metodo congruencial mixto/multiplicativo
def calcularNrosAleatoriosMetodoCongruencial(s, M, A, C, cantidad=20):
	n = []  # vector de numero de iteracion
	X = []  # vector de resultados
	R = []  # vector de residuos
	i = 0
	while i < cantidad:
		n.append(i)

		if i == 0:
			X.append(round(s, 4))
		else:
			newX = (A * X[i - 1] + C) % M
			newXRounded = round(newX, 4)
			X.append(newXRounded)

		newR = X[i] / M
		newRRounded = round(newR, 4)
		R.append(newRRounded)

		i += 1
	return n, X, R


#n, X, R = calcularNrosAleatoriosMetodoCongruencial(s, M, A, C, 100)

# print(n)
# print(X)
# print(R)

# for i in n:
#	print("Iteración nro: " + str(i) + ". Resultado: " + str(X[i]) + ". Residuo: " + str(R[i]))
#
#	opt = input("Presione enter para el próximo nro de la lista o cualquier otra tecla y enter para salir: ")
#	if opt is not "":
#		break

# def pruebaChiCuadrado(serie, nroIntervalos=10):
#

# metodo que divide en x cantidad de intervalos y devuelve
# un vector compuesto de tuplas, donde el primer valor indica
# limite inferior y el segundo el superior
# tambien devuelve un vector con las medias de cada intervalo
def dividirEnIntervalos(cantIntervalos, maximo=1, minimo=0):
	paso = (maximo - minimo) / cantIntervalos
	intervalos = []
	mediaDeCadaIntervalo = []
	i = 0
	while i < cantIntervalos:
		if i == 0:
			intervalos.append([round(minimo, 4), round(minimo + paso, 4)])
		else:
			minimoAnterior = round(intervalos[i - 1][1], 4)
			intervalos.append([minimoAnterior, round(minimoAnterior + paso, 4)])

		i += 1

	for i in intervalos:
		mediaDeCadaIntervalo.append(round((i[0] + i[1]) / 2, 4))

	return intervalos, mediaDeCadaIntervalo


# metodo que realiza el test de Chi cuadrado a una serie con una cantidad x de intervalos
# Para cada intervalo de frecuencia toma como mayor o igual al limite inferior y como
# menor a limite superior
# Devuelve un vector con las frecuencias esperadas y un vector con las frecuencias reales
def testChiCuadrado(serie, cantIntervalos):
	frecuenciaEsperada = [len(serie) / cantIntervalos] * cantIntervalos
	frecuenciaReal = []

	intervalos, mediaDeCadaIntervalo = dividirEnIntervalos(cantIntervalos)
	# print(intervalos)

	for i in intervalos:
		contadorApariciones = 0

		item = 0

		while item < len(serie):
			if serie[item] >= i[0] and serie[item] < i[1]:
				contadorApariciones += 1

			item += 1

		frecuenciaReal.append(contadorApariciones)

	return frecuenciaEsperada, frecuenciaReal


# frecuenciaEsperada, frecuenciaReal = testChiCuadrado(R, 10)

# print(len(R))
# print(frecuenciaEsperada)
# print(frecuenciaReal)
