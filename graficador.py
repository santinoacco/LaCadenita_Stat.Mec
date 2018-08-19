import matplotlib.pyplot as plt

#nombreArchivo deberia ser un string, siendo el nombre completo (la direccion desde el directorio actual) del archivo de texto	
def funcionGraficadora(nombreArchivo):
	X, Y = [], []
	for line in open(nombreArchivo, 'r'):
	  values = [float(s) for s in line.split()]
	  X.append(values[0])
	  Y.append(values[1])

	plt.scatter(X, Y)
	plt.show()