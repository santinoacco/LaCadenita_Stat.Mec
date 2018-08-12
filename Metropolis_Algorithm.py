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
N=200 #cantidad de sitios
mcs=2*N #cantidad de pasos MonteCarlo
k=C.Boltzmann #const de Boltzmann en J/K
#k2=C.Stefan_Boltzmann #const de Boltzmann en eV/K
T=300 #temperatura en grados Kelvin
beta = 1./k*T
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
def contar(state):
    x=0
    for place in state:
        if place == e1:
            x+=1
    return x

def energy(x):
    E=(e1-e2)*x + N*e2
    return E
'''
def p(beta,x):
    return np.exp(-beta*(e1*x + (N-x)*e2))
'''
#==============================================================================
# def length_1(x):
#     return (b*N+(a-b)*x)
#==============================================================================


contar(state)

print(energy(contar(state)))

def dist(Delta): return np.exp(-beta*Delta)

y=[]
x=[]
for b in range(0,50): #variamos la temperatura
    T = 10 + b*10
    x.append(T)
    print( 'va por %s'% T)
    for i in range(mcs):
        
        for j in range(N):
            
            q=int(rnd.uniform(0,N)) #nro random para elegir posicion de la cadena
            E=energy(contar(state))
            state[q]= -state[q]
            Eq=energy(contar(state))
            Delta = E-Eq
#==============================================================================
#             if Delta<0:
#                 break
#==============================================================================
    
            if Delta>0:
                p=rnd.uniform(0,1)
                if p<dist(Delta):
                    state[q]= -state[q]
                    
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