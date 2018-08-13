#simulacion Monte Carlo de una bandita elastica en el ensamble canonico (ej 6 del tp 2 de ME)
import scipy as sc
import numpy as np
import random
#la bandita se modela como cadena formada por N moleculas
#cada molecula tiene 2 estados posibles (a y b), que tienen asociados energias E_a y E_b y longitudes L_a y L_b
#se dan valores a estos parametros para la simulacion
N=10
E_a=-1
E_b=1
L_a=1
L_b=2
#en vez de definir cte de Boltzmann y temp T defino un valor de kT para ver como cambia segun el orden de magnitud
kT=1
#---ARRANCA EL MONTECARLO---
#
#inicialmente tengo una configuracion dada para cada molecula, que queda representada por las componentes del vector config
#la componente j-esima de config indica la energia de la molecula j-esima
#arranca con todas las moleculas en el estado de mayor energia (energia 1)
config=np.ones(N)
#x iteraciones para que termalice
x=5000
for i in range(x):
	#toma la posicion j de config elegida al azar y calcula la variacion de energia deltaE
	j=random.randint(0,(N-1))
	deltaE=(-2)*config[j]
	#si deltaE disminuye se queda con la modificacion en la posicion j
	if deltaE < 0:
		config[j]=-(config[j])
	if deltaE > 0:
		#este coso es la condicion para decidir si aceptar o no la modificacion de j
		coso=random.random()
		if coso < (np.exp(-deltaE/kT)):
			config[j]=-(config[j])
num_a=0
num_b=0
#inicializa cantidad de moleculas en a y en b
E_0=0
for n in range(N):
	#mide primer valor de energia (E_0) y longitud (L_0)
	E_0=E_0+config[n]
	if config[n]==1:
		num_b=num_b+1
	else:
		num_a=num_a+1
print (E_0)
L_0=num_a*L_a+num_b*L_b
#tomo 10 medidas a ver que onda
for i in range(10):
	#toma la posicion j de config elegida al azar y calcula la variacion de energia deltaE
	j=random.randint(0,(N-1))
	deltaE=(-2)*config[j]
	#si deltaE disminuye se queda con la modificacion en la posicion j
	if deltaE < 0:
		config[j]=-(config[j])
		num_a=num_a+1
		num_b=num_b-1
	if deltaE > 0:
		#este coso es la condicion para decidir si aceptar o no la modificacion de j
		coso=random.random()
		if coso < (np.exp(-deltaE/kT)):
			config[j]=-(config[j])
			num_a=num_a-1
			num_b=num_b+1
	E=E_a*num_a+E_b*num_b
	print (E)