# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 21:06:09 2018

@author: Santiago
"""

import numpy as np
import matplotlib.pyplot as plb
plb.style.use('ggplot')
import time
import random as rn
'Parametros'
start_time = time.time()
S = 300
N = 10 #Longitud de la cadena
e_a = 0 #Enerfia de la particulas a
e_b = 1 #Energia de las particulas b
e_c = 2 #Energia de las particulas c
kT0 = 0.1 #Temperatura
a = 1 #Longitud de a
b = 2 #Longitud de b
c = 3 #Longitud de c
mcs = 100*N#Montecarlo steps


'''Energia de la cadena'''
def Energia(cadena):#Definir e_alfa y e_beta con count
    num_a = cadena.count(e_a)
    num_b = cadena.count(e_b)
    energia = e_a*num_a +e_b*num_b + (N-num_a-num_b)*e_c 
    return energia

'''Longitud de la cadena'''
def length(Mean_E): #se calcula a partir del valor medio de la Energia.. es decir por la funcion Energia_cadena
    long = b*N+(a-b)*((Mean_E-N*e_b)/(e_b-e_a))
    return long

    
'''Mapeo de estado a energía'''    
def Mapeo(rand):
    if rand == 0:
        e_rand = e_a
    elif rand == 1:
        e_rand = e_b
    elif rand == 2:
        e_rand = e_c
    return e_rand
    
'''Montecarlo Step a temperatura T, mezclo M veces'''
def MCS(cadena,kT,M  = N): 
    for j in range(M):
        r1 = rn.randint(0,2) #define energía del nuevo estado
        r2 = rn.randint(0,N-1)
        while r1 == cadena[r2]:
             r1 = rn.randint(0,2)

        DeltaE = Mapeo(r1) - Mapeo(cadena[r2])
        
        if DeltaE<0:
            cadena[r2] = r1
        else:
            r3 = rn.random()
            if r3 < (np.exp(-DeltaE/kT)):
                cadena[r2] = r1
    
    return cadena

'''Calculamos la energía analiticamente para 2 estados'''
def Control(KT):
    E_control = N*(e_b*np.exp(-1/KT*e_b)+e_c*np.exp(-1/KT*e_c)+ e_a*np.exp(-1/KT*e_a))/(np.exp(-1/KT*e_b)+np.exp(-1/KT*e_c)+np.exp(-1/KT*e_a))
    return E_control

'''Mido la longitud y la energia media de la cadena, a una dada temperatura'''
def Energia_cadena(cadena,kT):
    Energias = []
    Energias2 = []
    for i in range(100): #mezclo 100 veces
        cadena =  MCS(cadena,kT,M = N)
    for j in range(1000): #tomo 1000 medidas
            cadena = MCS(cadena,kT,10)#Mezclo
            E=Energia(cadena)
            E2=E**2
            Energias.append(E) #Mido la energia
            Energias2.append(E2) #Mido <E^2>
    Mean_Energy = np.mean(Energias)
    Mean_Energy_Square = np.mean(Energias2)
    var = Mean_Energy_Square - Mean_Energy**2 
    
    return Mean_Energy, var


    
'''Esta es la parte que hace todo, calcula la energia media para S distintas temperaturas a partir de una T0'''


#################################################
cadena = N*[2] #Creo cadena
#==============================================================================
# print(cadena)
#==============================================================================
'''Y aqui el script''' 
KT = []
Energy_per_temp = [] #energia por kT
L=[] #longitud por kT
L_c=[]#longitud de control, utiliza la funcion Control para calcular la energía
Calor=[] #calor especifico
from scipy.constants import Boltzmann as k
for i in range(S):
    kT =kT0 + i*3./S
    KT.append(kT)
    E_media, varianza= Energia_cadena(cadena,kT)
    Energy_per_temp.append(E_media)
    c_v=varianza/(kT**2)*k**2
    Calor.append(c_v)
    auxL=length(E_media) #calculo el valor esperado de L[i]
    L.append(auxL)
    auxL2=length(Control(kT))
    L_c.append(auxL2)
    
    
    
#==============================================================================
#     print('iteracion = ',i,'kT =',round(kT,2),'Energy=',Energy_per_temp[i]) 
#==============================================================================
print("--- %s seconds ---" % round((time.time() - start_time),2)) 
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
plb.ylabel('Calor especifico',fontsize = 20)
plb.plot(KT,Calor,'b.')
plb.legend()
plb.show()

