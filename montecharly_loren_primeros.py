import numpy as np
import copy as cp
import time
'Parametros'
start_time = time.time()
S = 100
N = 10 #Longitud de la cadena
#e_a = 0 #Enerfia de la particulas a
e_a=-1
e_b = 1 #Energia de las particulas b
 #Energia de las particulas c
kT0 = 0.1 #Temperatura
a = 1 #Longitud de a
b = 2 #Longitud de b
c = 3
mcs = 100#Montecarlo steps


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
    E_int=0
    for i in range(N-1):
        E_int+=-Mapeo(cadena[i+1])*Mapeo(cadena[i])
    eneryi=E0+E_int
    return eneryi

'''Longitud de la cadena'''
def length(Mean_E): #se calcula a partir del valor medio de la Energia.. es decir por la funcion Energia_cadena
    long = b*N+(a-b)*((Mean_E-N*e_b)/(e_b-e_a))
    return long

'Variacion de la energia al cambiiar el estado de una particula'
def DeltaE(cadena,i):
    if cadena[i]==1: #Si el cambio es de una particula beta a una alfa
        return (e_a-e_b)
    else: return (e_b - e_a) #caso contrario
    
def DeltaE_int(oldcadena,newcadena,i):
    if i==0:
        return -Mapeo(newcadena[0])*Mapeo(newcadena[1])+Mapeo(oldcadena[0])*Mapeo(oldcadena[1])
    else:
        if i==N-1:
            return -Mapeo(newcadena[N-2])*Mapeo(newcadena[N-1])+Mapeo(oldcadena[N-2])*Mapeo(oldcadena[N-1])
        else: return -Mapeo(newcadena[i+1])*Mapeo(newcadena[i])-Mapeo(newcadena[i-1])*Mapeo(newcadena[i])+Mapeo(oldcadena[i])*Mapeo(oldcadena[i-1])+Mapeo(oldcadena[i])*Mapeo(oldcadena[i+1])
    
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

'''Mido la llongitud y la enrgia media de la cadena, a una dada temperatura'''
def Energia_cadena(cadena,kT):
    Energias = []
    Energias2 = []
    for i in range(100): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for j in range(1000): #tomo 1000 medidas
            cadena = MCS(cadena,kT,10)#Mezclo
            EE=E(cadena)
            EE2=EE**2
            Energias.append(EE) #Mido la energia
            Energias2.append(EE2) #Mido <E^2>
    Mean_Energy = np.mean(Energias)
    Mean_Energy_Square = np.mean(Energias2)
    var = Mean_Energy_Square - Mean_Energy**2 
    
    return Mean_Energy, Mean_Energy_Square, var

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
Var=[] #varianza de la energia
for i in range(S):
    kT =kT0 + i*3./S
    KT.append(kT)
    E_media= Energia_cadena(cadena,kT)[0]
    varianza = Energia_cadena(cadena,kT)[2]
    Energy_per_temp.append(E_media)
    Var.append(varianza)
#==============================================================================
#     Var.append(Varianza_E(cadena,kT))
#==============================================================================

#    auxL=length(E_media) #calculo el valor esperado de L[i]
#    L.append(auxL)
#    auxL2=length(Control(kT))
#L_c.append(auxL2)
import matplotlib.pyplot as plt
plt.plot(KT,Energy_per_temp,'r.')
plt.plot(KT,Control(KT),'b.')
plt.show()