import numpy as np
import copy as cp
import time
'Parametros'
start_time = time.time()
S = 100
N = 10 #Longitud de la cadena
#e_a = 0 #Energia de la particulas a
e_a=-1
e_b = 1 #Energia de las particulas b
 #Energia de las particulas c
kT0 = 0.1 #Temperatura
a = 1 #Longitud de a
b = 2 #Longitud de b
c = 3
mcs = 100#Montecarlo steps
#esto dice hasta que vecino hay interaccion
Alcance=N-1


'''Cambiador del estado de una particula de la cadena'''
def Change(cadena):
    i = np.random.randint(0,N)
    change = cp.deepcopy(cadena)
    if change[i]==1: change[i] = 0 #cambio de particula alfa a beta
    else:change[i]=1 #cambio de beta a alfa
    return change,i #devuelve una nueva cadena junto con el indice del cambio


'''Energia de la cadena'''
def E(cadena):#Definir e_alfa y e_beta con count
    a=0
#    for count in range(N):
#        if cadena[count]==1:
#            a+=1
    a = sum(cadena) #el numero de alfas es el total de 1's en la cadena
    E0=e_a*a + e_b*(N-a)
    E_int=E_interaccion(cadena,Alcance)
    eneryi=E0-E_int
    return eneryi

#esto calcula la energia asociada con la interaccion que hayas puesto
def E_interaccion(states,num_vecinos):
    E=0
    for sitio in range(N-1):
        for lugar in range(sitio+1,sitio+num_vecinos+1):
            if sitio+num_vecinos+1<=N:
                #J es el tipo de interaccion (aca esta puesta la de la inversa de la distancia)
                J=1./np.abs(sitio-lugar)
                E+=J*Mapeo(states[sitio])*Mapeo(states[lugar])
    return E
                           
'''Longitud de la cadena'''
def length(n_a): #se calcula a partir del valor medio de la Energia.. es decir por la funcion Energia_cadena
    long = b*(N-n_a)+a*n_a
    return long

'Variacion de la energia al cambiar el estado de una particula'
def DeltaE(cadena,i):
    if cadena[i]==1: #Si el cambio es de una particula beta a una alfa
        return (e_a-e_b)
    else: return (e_b - e_a) #caso contrario
    
def DeltaE_int(oldcadena,newcadena,i):
    if i==0:
        return (-Mapeo(newcadena[0])+Mapeo(oldcadena[0]))*suma(oldcadena,0,Alcance)
    else:
        if i==N-1:
            return (-Mapeo(newcadena[N-2])+Mapeo(oldcadena[N-2]))*suma(oldcadena,N-1,Alcance)
        else: return (-Mapeo(newcadena[i])+Mapeo(oldcadena[i]))*suma(oldcadena,i,Alcance)
#la funcion "suma" calcula la suma de la energia toda la cadena sin contar el sitio que le indicas
#"sitio" es la posicion donde esta parado y "num_vecinos" hasta que vecino queres que considere pa interatuar
#aca podes cambiar el tipo de interaccion modificando "interaccion"
def suma(states,sitio,num_vecinos):
    total=0
    for i in range(N):
        distancia=np.abs(sitio-i)
        if i !=sitio and distancia<=num_vecinos:
                #en este caso es la aburrida inversa de la distancia
                interaccion=1./distancia
                total+=interaccion*Mapeo(states[i])
    return total
    
'Montecarlo Step a temperatura T, mezclo M veces'
def MCS(cadena,kT,M  = N): 
    for j in range(M):
        potencial_cadena,i = Change(cadena) #me fijo que pasa cuando doy vuelta el estado de una particula. Tengo una potencial cadena nueva
        Delta1 = DeltaE(potencial_cadena,i)
        Delta2= DeltaE_int(cadena,potencial_cadena,i)
        Delta=Delta1+Delta2
        if Delta <0: cadena = potencial_cadena
        else:
            if np.random.random() < np.exp(-Delta/(kT)): cadena =  potencial_cadena
    return cadena #Si T es alta entonces va a ser posible ese cambio
            
'''Calculamos la energia analiticamente para 2 estados'''
def Control(KT):
    E_control = (N*e_b + N*e_a*np.exp(-1/np.array(KT)*(e_a-e_b)))/(np.exp(-1/np.array(KT)*(e_a-e_b))+1)
    return E_control

'''Mido la longitud y la energia media de la cadena, a una dada temperatura'''
def Energia_cadena(cadena,kT):
    Energias = []
    Energias2 = []
    n=[]
    for i in range(100): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for j in range(1000): #tomo 1000 medidas
            cadena = MCS(cadena,kT,10)#Mezclo
            EE=E(cadena)
            EE2=EE**2
            Energias.append(EE) #Mido la energia
            Energias2.append(EE2) #Mido <E^2>
            n.append(sum(cadena))
    Mean_Energy = np.mean(Energias)
    Mean_Energy_Square = np.mean(Energias2)
    var = Mean_Energy_Square - Mean_Energy**2 
    n_a=np.mean(n)
    return Mean_Energy, n_a, var
#como el vector cadena tiene como componentes 0 y 1 esto asigna las energias segun el valor de la componente
def Mapeo(numerito):
    if numerito==1:
        return e_a
    else:
        return e_b

cadena = np.ones(N)#Creo cadena
'''Y aqui el script''' 
KT = []
Energy_per_temp = [] #energia por kT
L=[] #longitud por kT
L_c=[]#longitud de control, utiliza la funcion Control para calcular la energia
Calor=[] #calor especifico
from scipy.constants import Boltzmann as k
for i in range(S):
    kT =kT0 + i*10./S
    KT.append(kT)
    E_media, num_a, varianza= Energia_cadena(cadena,kT)
    Energy_per_temp.append(E_media)
    c_v=varianza/(kT**2)*k**2
    Calor.append(c_v)
    auxL=length(num_a) #calculo el valor esperado de L[i]
    L.append(auxL)

print("--- %s seconds ---" % round((time.time() - start_time),2))
##GRAFICOS##
import matplotlib.pyplot as plt
fig = plt.figure(1)
plt.xlabel('kT',fontsize = 20)
plt.ylabel('Energia',fontsize = 20)
plt.plot(KT,Energy_per_temp,'r.')
#=====================================
fig = plt.figure(2)
plt.xlabel('kT',fontsize = 20)
plt.ylabel('Longitud',fontsize = 20)
plt.plot(KT,L,'g.')
#=====================================
fig = plb.figure(3)
plb.xlabel('kT',fontsize = 20)
plb.ylabel('Calor especifico',fontsize = 20)
plb.plot(KT,Calor,'b.')
plb.legend()
plt.show()
