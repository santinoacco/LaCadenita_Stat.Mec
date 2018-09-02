# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 23:10:18 2018

@author: Lorenzo Emiliano
"""

import numpy as np
import matplotlib.pylab as plb
from scipy import constants as c
import copy as cp
plb.style.use('ggplot')
import time
'Parametros'
start_time = time.time()
S = 200
N = 10 #Longitud de la cadena
e_alfa = 1 #Enerfia de la particulas alfa
e_beta = 2 #Energia de las particulas beta
k = c.Stefan_Boltzmann
kT0 = 0.1 #Temperatura
a = 1 #Longitud de alfa
b = 2#Longitud de beta
mcs = 100#Montecarlo steps


'''Cambiador del estado de una particula de la cadena'''
def Change(cadena):
    N = len(cadena)
    i = np.random.randint(0,N)
    change = cp.deepcopy(cadena)
    if change[i]==1: change[i] = 0 #cambio de particula alfa a beta
    else:change[i]=1 #cambio de beta a alfa
    return change,i #devuelve una nueva cadena junto con el indice del cambio

'''Maxwell Distribution Probability'''
def P(E,kT):
    beta = 1./(kT)
    return np.exp(-beta*E)

'''Energia de la cadena'''
def E(cadena):#Definir e_alfa y e_beta    
    N = len(cadena)
    alfa = sum(cadena) #el numero de alfas es el total de 1's en la cadena
    return e_alfa*alfa + e_beta*(N-alfa)
'''Longitud de la cadena'''
def length(Mean_E): #se calcula a partir del valor medio de la Energia.. es decir por la funcion Energia_cadena
    long = b*N+(a-b)*((Mean_E-N*e_beta)/(e_beta-e_alfa))
    return long

'Variacion de la energia al cambiiar el estado de una particula'
def DeltaE(cadena,i):
    if cadena[i]==1: #Si el cambio es de una particula beta a una alfa
        return (e_alfa-e_beta)
    else: return (e_beta - e_alfa) #caso contrario
    
'Montecarlo Step a temperatura T, mezclo M veces'
def MCS(cadena,kT,M  = N): 
    for j in range(M):
        potencial_cadena,i = Change(cadena) #me fijo que pasa cuando doy vuelta el estado de una particula. Tengo una potencial cadena nueva
        Delta = DeltaE(potencial_cadena,i)
        if Delta <0: cadena = potencial_cadena
        else:
            if np.random.random() < P(Delta,kT): cadena =  potencial_cadena
    return cadena #Si T es alta entonces va a ser posible ese cambio
            
'''Calculamos la energía analiticamente para 2 estados'''
def Control(KT):
    E_control = (N*e_beta + N*e_alfa*np.exp(-1/np.array(KT)*(e_alfa-e_beta)))/(np.exp(-1/np.array(KT)*(e_alfa-e_beta))+1)
    return E_control

'''Mido la llongitud y la enrgia media de la cadena, a una dada temperatura'''
def Energia_cadena(cadena,kT):
    Energias = []
    Energias2 = []
    for i in range(100): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for i in range(1000): #tomo 1000 medidas
        cadena = MCS(cadena,kT,10)#Mezclo
        EE=E(cadena)
        EE2=EE**2
        Energias.append(EE) #Mido la energia
        Energias2.append(EE2) #Mido <E^2>
    Mean_Energy = np.mean(Energias)
    Mean_Energy_Square = np.mean(Energias2)

    return Mean_Energy, Mean_Energy_Square

def Varianza_E(cadena,kT): #sigma^2 = <E^2>-<E>^2
    var = Energia_cadena(cadena,kT)[1] - Energia_cadena(cadena,kT)[0]**2
    return var


    
'''Esta es la parte que hace todo, calcula la energia media para S distintas temperaturas a partir de una T0'''


#################################################
cadena = np.ones(N)#Crep cadena
'''Y aqui el script''' 
KT = []
Energy_per_temp = [] #energia por kT
L=[] #longitud por kT
L_c=[]#longitud de control, utiliza la funcion Control para calcular la energía
Var=[] #varianza de la energía
for i in range(S):
    kT =kT0 + i*3./S
    KT.append(kT)
    E_media= Energia_cadena(cadena,kT)[0]      
    Energy_per_temp.append(E_media)
    Var.append(Varianza_E(cadena,kT))
    
    
    auxL=length(E_media) #calculo el valor esperado de L[i]
    L.append(auxL)
    auxL2=length(Control(kT))
    L_c.append(auxL2)
    
    
    
#==============================================================================
#     print('iteracion = ',i,'kT =',round(kT,2),'Energy=',Energy_per_temp[i]) 
#==============================================================================
    
'''Graficamos'''
fig = plb.figure(1)
plb.xlabel('kT',fontsize = 20)
plb.ylabel('Energia',fontsize = 20)
plb.plot(KT,Energy_per_temp,'r.')
plb.plot(KT,Control(np.array(KT)),'k-')

#=====================================
fig = plb.figure(2)
plb.xlabel('kT',fontsize = 20)
plb.ylabel('Longitud',fontsize = 20)
plb.plot(KT,L,'g.')
plb.plot(KT,L_c,'k-')
#=====================================
fig = plb.figure(3)
plb.xlabel('kT',fontsize = 20)
plb.ylabel('Varianza de Energia',fontsize = 20)
plb.plot(KT,Var,'b.')


print("--- %s seconds ---" % (round(time.time() - start_time),2))

