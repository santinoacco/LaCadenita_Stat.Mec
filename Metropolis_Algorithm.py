# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 21:55:56 2018

@author: Santiago
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd
from scipy import constants as C
plt.style.use('ggplot')


rnd.seed()


#parametros

a=1
b=2
e1=-1
e2=1
N=100 #cantidad de sitios
mcs=10*N #cantidad de pasos MonteCarlo
#k=C.Boltzmann #const de Boltzmann en J/K
#k2=C.Stefan_Boltzmann #const de Boltzmann en eV/K
#T=300 #temperatura en grados Kelvin

Mean_E=0
Mean_L=0
mean_E2=0
#auxiliares
Eaux=0
Laux=0
Ea2ux=0
#=============================================================================#

#-------#
#state = rnd.rand(N) me genera una lista con elem aleat de N comp.
#-------#
'''creamos la bandita/estado'''
state = np.ones(N)
print(state)

def contar(state): #devuelve la cantidad de sitios en el estado de energía e1
    x=0
    for place in state:
        if place == e1:
            x+=1
    return x

def energy(x):
    E=e1*x + (N-x)*e2
    return E


def dist(kT,Delta):
    return np.exp(-Delta/kT)


y=[]
x=[]




for b in range(0,50): #variamos la temperatura
    kT = 0.01 + b
    x.append(kT)
    print( 'va por %s'% kT)
    #termalizar
    for i in range(mcs):
        for j in range(N):
            
            q=rnd.randint(0,N) #nro random para elegir posicion de la cadena
            E=energy(contar(state))
            state[q]= -state[q]
            Eq=energy(contar(state))
            Delta = (-2)*state[q]
    
            if Delta>0:
                p=rnd.uniform(0,1)
                if p<dist(kT,Delta):
                    state[q]= -state[q]
    
    #cambio los estados y mido       
    
    for i in range(mcs):
        q=rnd.randint(0,N) #nro random para elegir posicion de la cadena
        E=energy(contar(state))
        state[q]= -state[q]
        Eq=energy(contar(state))
        Delta = (-2)*state[q]
        if Delta>0:
             p=rnd.uniform(0,1)
             if p<dist(kT,Delta):
                 state[q]= -(state[q])
                 #Eq=energy(contar(state))
        Eaux+=energy(contar(state))
        
       # Laux+=length_1(contar(state))
        
    Mean_E= Eaux/mcs
    y.append(Mean_E)
#Mean_L           
#    print(state)


'''graficamos'''
  
fig = plt.figure()

plt.plot(x,y,'b.')
plt.xlabel('Tempreture')
plt.ylabel("Energy")


#plt.title()
plt.show()
