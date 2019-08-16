# Simulacion2019
Este repositorio aloja los diferentes ejercicios realizados por alumnos de la UTN-FRC para la cátedra de Simulación en el año 2019

## Curso: 4K4

## Alumnos:
 - Gersicich, Jeremias
 - Venturi, Agustin
 - Grober, Luciana
 - Bacca, Josue
 - Britos Anabel
 
## Generar EXE

Se debe realizar en una máquina con Windows.

Instalar todas las dependencias listadas en setup.py.

Instalar PyInstaller con el comando:

`pip install pyinstaller`

Luego ir a la raiz del proyecto y correr:

`pyinstaller --onefile ./generador.py --hiddenimport 'numpy.random.common' --hiddenimport 'numpy.random.bounded_integers' --hiddenimport 'numpy.random.entropy'`
