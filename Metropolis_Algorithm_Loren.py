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
S = 10
N = 10 #Longitud de la cadena
e_a = 1 #Enerfia de la particulas alfa
e_b = 2
e_g = 6#Energia de las particulas beta
k = c.Stefan_Boltzmann
kT0 = 0.1 #Temperatura
a = 1 #Longitud de alfa
b = 2#Longitud de beta
mcs = 100#Montecarlo steps

# =============================================================================
# 'Definicion de alguna cadena de longitud N, dos estados posibles,1 alfa,0 beta'
# def Cadena(N):
#     return np.array([np.random.randint(0,2) for i in range(N)])
# 
# =============================================================================
'''Cambiador del estado de una particula de la cadena'''
def Change(cadena):
    i = np.random.randint(0,N)
    change = cp.deepcopy(cadena)
    s = cadena[i]
    while change[i] == s:
        change[i] = np.random.randint(-1,2)
    return change,i #devuelve una nueva cadena junto con el indice del cambio

'''Maxwell Distribution Probability''' 
def P(E,kT):
    beta = 1./(kT)
    return np.exp(-beta*E)

'''Mapeo entre los estados y las energias'''
def Mapeo_energia(i):
    if i == 0:return e_a
    if i == 1:return e_b
    if i == -1:return e_g

'''Energia de la cadena'''
def E(cadena):#Definir e_alfa y e_beta       
    alfa = cadena.count(0)
    beta = cadena.count(1)
    gamma = cadena.count(-1)#el numero de alfas es el total de 1's en la cadena
    return e_a*alfa + e_b*beta + e_g*gamma


'''Variacion de la energia al cambiiar el estado de una particula'''
def DeltaE(cadena,potencial_cadena,i):
    return Mapeo_energia(potencial_cadena[i])-Mapeo_energia(cadena[i])
    
'''Montecarlo Step a temperatura T, mezclo M veces'''
def MCS(cadena,kT,M  = N): 
    for j in range(M):
        potencial_cadena,i = Change(cadena) #me fijo que pasa cuando doy vuelta el estado de una particula. Tengo una potencial cadena nueva
        Delta = DeltaE(cadena,potencial_cadena,i)
        if Delta <0: cadena = potencial_cadena
        else:
            if np.random.random() < P(Delta,kT): cadena = potencial_cadena
       # print(cadena)
    return cadena #Si T es alta entonces va a ser posible ese cambio
            
# =============================================================================
# 'Longitud de la cadena'
# def Longitud(cadena):return a*sum(cadena)+b*(len(cadena)-sum(cadena))
# =============================================================================
#def Control(KT):return (N*e_beta + N*e_alfa*np.exp(-1/np.array(KT)*(e_alfa-e_beta)))/(np.exp(-1/np.array(KT)*(e_alfa-e_beta))+1)
'''Mido la llongitud y la enrgia media de la cadena, a una dada temperatura'''

'''Calculamos la energía analiticamente para 2 estados'''
def Control(KT):
    E_control = (N*e_beta + N*e_alfa*np.exp(-1/np.array(KT)*(e_alfa-e_beta)))/(np.exp(-1/np.array(KT)*(e_alfa-e_beta))+1)
    return E_control
def Energia_cadena(cadena,kT):
    Energias = []
#    Longitudes = []
    for i in range(1000): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for i in range(1000): #tomo 1000 medidas
        cadena = MCS(cadena,kT,10)#Mezclo
        Energias.append(E(cadena)) #Mido la energia
#        Longitudes.append(Longitud(cadena))#Mido la longitud
    Mean_Energy = np.mean(Energias)
#    Mean_Longitudes = np.mean(Longitudes)
    return Mean_Energy#,Mean_Longitudes
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


    
'''Esta es la parte que hace todo, calcula la energia media para S distintas temperaturas a partir de una T0'''


#################################################
cadena = list(np.ones(N))#Crep cadena
'''Y aqui el script'''
KT = []
Energy_per_temp = []
for i in range(S):
    kT =kT0 + i*3./S
    KT.append(kT)       
    Energy_per_temp.append(Energia_cadena(cadena,kT))
    print('iteracion = ',i,'kT =',round(kT,2),'Energy=',Energy_per_temp[i]) 
#Ploteo
fig = plb.figure(1)
plb.xlabel('KT',fontsize = 20)
plb.ylabel('Energy_per_temp',fontsize = 20)
plb.scatter(KT,Energy_per_temp)
#plb.plot(KT,Control(np.array(KT)),c = 'k')
print("--- %s seconds ---" % (round(time.time() - start_time,2)))
    
    
'''Graficamos'''
fig = plb.figure(1)
plb.xlabel('kT',fontsize = 20)
plb.ylabel('Energia',fontsize = 20)
plb.plot(KT,Energy_per_temp,'r.')
plb.plot(KT,Control(np.array(KT)),'k-')

