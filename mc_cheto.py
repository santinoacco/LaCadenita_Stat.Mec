#MONTECHARLY
import numpy as np
import random
import matplotlib.pyplot as plt	
#from matplotlib import pyplot as plt
#defino numero de sitios N, energias de estados a y b y longitudes asociadas
N=10
E_a=-1
E_b=1
L_a=1
L_b=2
E_prom=0

#plt.rcParams['agg.path.chunksize'] = 20000
#kk=np.zeros(1000)
#E_prom=np.zeros(1000)
f=open('archivito.txt','w')
print('kT','Energias',file=f)
#para obtener el grafico de muchos valores de E vs kT
for num in range(1000):
	kT=0.01+num/400.
	config=np.ones(N)
	#x es el numero de iteraciones para que termalice (x=100*N pasos y cada paso es hacer el primer 'for' N veces)
	x=10000
	E_0=0
	num_a=0
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
	for n in range(N):
		#mide primer valor de energia (E_0)
		E_0=E_0+config[n]
		if config[n]==(-1):
			num_a=num_a+1
	energia=np.zeros(x+1)
	energia[0]=E_0
	#tomamos x medidas para promediar
	for i in range(1,x+1):
		#toma la posicion j de config elegida al azar y calcula la variacion de energia deltaE
		j=random.randint(0,(N-1))
		deltaE=(-2)*config[j]
		#si deltaE disminuye se queda con la modificacion en la posicion j
		if deltaE < 0:
			config[j]=-(config[j])
			num_a=num_a+1
		if deltaE > 0:
			#este coso es la condicion para decidir si aceptar o no la modificacion de j
			coso=random.random()
			if coso < (np.exp(-deltaE/kT)):
				config[j]=-(config[j])
				num_a=num_a-1
		energia[i]=E_a*num_a+E_b*(N-num_a)
	E_prom=np.mean(energia)
	#guarda en el archivito los valores de kT y energia para graficar
	print(kT,E_prom,file=f)
	#kk[j]=kT
f.close()
X, Y = [], []
for line in open('archivito.txt', 'r'):
	values = [float(s) for s in line.split()]
	X.append(values[0])
	Y.append(values[1])
plt.scatter(X, Y)
plt.show()
#plt.scatter(kk,E_prom)
#plt.show()
