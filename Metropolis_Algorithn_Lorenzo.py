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

N = 200 #Longitud de la cadena
e_alfa = 1 #Enerfia de la particulas alfa
e_beta = 2 #Energia de las particulas beta
k = c.Stefan_Boltzmann
kT0 = 0.1 #Temperatura
a = 1 #Longitud de alfa
b = 2#Longitud de beta
mcs = 100#Montecarlo steps

'Definicion de alguna cadena de longitud N, dos estados posibles,1 alfa,0 beta'
def Cadena(N):
    return np.array([np.random.randint(0,2) for i in range(N)])

'Cambiador del estado de una particula de la cadena'
def Change(cadena):
    N = len(cadena)
    i = np.random.randint(0,N)
    change = cp.deepcopy(cadena)
    if change[i]==1: change[i] = 0 #cambio de particula alfa a beta
    else:change[i]=1 #cambio de beta a alfa
    return change,i #devuelve una nueva cadena junto con el indice del cambio

'Maxwell Distribution Probability'    
def P(E,kT):
    beta = 1./(kT)
    return np.exp(-beta*E)

'Energia de la cadena'
def E(cadena):#Definir e_alfa y e_beta    
    N = len(cadena)
    alfa = sum(cadena) #el numero de alfas es el total de 1's en la cadena
    return e_alfa*alfa + e_beta*(N-alfa)
'Variacion de la energia al cambiiar el estado de una particula'
def DeltaE(cadena,i):
    if cadena[i]==1: #Si el cambio es de una particula beta a una alfa
        return (e_alfa-e_beta)
    else: return (e_beta - e_alfa) #caso contrario
    
'Montecarlo Step a temperatura T, mezclo mcs veces'
def MCS(cadena,kT,M  = N): 
    for j in range(M):
        potencial_cadena,i = Change(cadena) #me fijo que pasa cuando doy vuelta el estado de una particula. Tengo una potencial cadena nueva
        Delta = DeltaE(potencial_cadena,i)
        if Delta <0: cadena = potencial_cadena
        else:
            if np.random.random() < P(Delta,kT): cadena =  potencial_cadena
    return cadena #Si T es alta entonces va a ser posible ese cambio
            


'Longitud de la cadena'
def Longitud(cadena):return a*sum(cadena)+b*(len(cadena)-sum(cadena))
            
'Mido la llongitud y la enrgia media de la cadena, a una dada temperatura'
def Energia_Longitud(cadena,kT):
    Energias = []
#    Longitudes = []
    for i in range(1000000): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for i in range(1000000): #tomo 1000 medidas
        cadena = MCS(cadena,kT,1)#Mezclo
        Energias.append(E(cadena)) #Mido la energia
#        Longitudes.append(Longitud(cadena))#Mido la longitud
    Mean_Energy = np.mean(Energias)
#    Mean_Longitudes = np.mean(Longitudes)
    return Mean_Energy#,Mean_Longitudes

#print('Longitud media = ',Mean_Longitudes,'\nEnergia Media = ',Mean_Energy)
'Esta es la parte que hace todo, calcula la energia media para S distintas temperaturas a partir de una T0'
def Energia_per_temperatura(cadena,kT0,S = 50):
    Temperaturas = []
    Energy_per_temp = []
    for i in range(S):
        kT =kT0 + i*3./50
        Temperaturas.append(kT)       
        Energy_per_temp.append(Energia_Longitud(cadena,kT))
        print('iteracion = ',i,'kT =',round(kT,2),'Energy=',Energy_per_temp[i])
    return Temperaturas,Energy_per_temp #Dos listas:Temperaturas y enerrgias

#################################################
'Y aqui el script'
cadena = Cadena(N)#Crep cadena
Resultados = Energia_per_temperatura(cadena,kT0,10000)  # a partir de T0 obtengo resultados  
#Ploteo
fig = plb.figure(1)
plb.xlabel('Temperatura',fontsize = 20)
plb.ylabel('Energy_per_temp',fontsize = 20)
plb.scatter(Resultados[0],Resultados[1])
print("--- %s seconds ---" % (time.time() - start_time))
        
    
