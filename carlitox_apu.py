
# coding: utf-8

# In[1]:


import numpy.random as random
import math
from numpy import mean as mean
import matplotlib.pyplot as plt
import copy 


# In[2]:


#Variables / Condiciones Ininciales
Energias = [] #Energias que quiero calcular para luego graficar
Atomos = 10
Temperatura = 150 #Temperatura maxima en la que voy a medir
Estado_Actual=[] 
Estados_Energeticos = [-1,1] #Las energias de los distintos estados
temperaturas = [] 
Iteraciones = 20000 #Numero de veces que voy a medir la energia en una dada temperatura
Interaccion = 1 #Esto me mide la energia de a pares, si es positivo/negativo, me dice si es ferro/antiferro
Prender_Interaccion = True #Si pongo la interaccion de a pares o no, esto puede valer solo True/False


# In[3]:


#Funciones del programa 
def Medir_Energia(Estados):
    E = 0
    for j in Estados:
        if j == 1:
            E += 1
        else:
            E -= 1
    return E
            
#Evoluciona el Estado_Actual
def Evolucionar(kt,Estados):
    cambiar = random.randint(Atomos)

    Estados_Energeticos_Auxiliares= copy.copy(Estados_Energeticos)
    Estados_Energeticos_Auxiliares.remove(Estados[cambiar])

    Estado_Auxiliar = copy.copy(Estados)
    Estado_Auxiliar[cambiar] = random.choice(Estados_Energeticos_Auxiliares)

    Energia_Actual = Medir_Energia(Estados)
    Energia_Futura = Medir_Energia(Estado_Auxiliar)

    if Prender_Interaccion == True :
        Energia_Futura += Medir_Interaccion(Estado_Auxiliar)
        Energia_Actual += Medir_Interaccion(Estados)

    if Energia_Futura < Energia_Actual:
        Estados = copy.copy(Estado_Auxiliar)
    else:
        condicion = random.random()
        if (condicion < math.exp(-2/kt) ):
            Estados = copy.copy(Estado_Auxiliar)
            
    return Estados

def Medir_Interaccion(estados):
    """Voy a suponer que tengo una energía de interaccion de a pares (de 1ros vecinos)"""
    E = 0
    for j in range(Atomos-1):
        E += Interaccion*estados[j]*estados[j+1]
#        E += Interaccion*estados[j]*estados[j-1]
    return E

def Termalizar(kt,Estados):
    for j in range(2*Atomos):
        Estados = Evolucionar(kt,Estados)
    return Estados


# In[4]:


#Doy un estado inicial
Estado_Actual  = [max(Estados_Energeticos) for j in range(Atomos) ]


for t in range(Temperatura):
    kt = 0.01 + t/50
    temperaturas.append(kt)
    Energia_Auxiliar = []
    Estado_Actual = Termalizar(kt,Estado_Actual) #Termalizo antes de medir la energia
    
    for j in range(Iteraciones):
        Estado_Actual = Evolucionar(kt,Estado_Actual)
        
        Energia_Parcial = Medir_Energia(Estado_Actual)
        
        if Prender_Interaccion == True:
            Energia_Parcial += Medir_Interaccion(Estado_Actual)
                
        Energia_Auxiliar.append(Energia_Parcial)
        
    Energias.append(mean(Energia_Auxiliar))


#Solucion Exacta del Sistema de 2 Niveles
Energias1 = []
kt1 = []
for t in range(0,150):
    kt = 0.01+t/50
    kt1.append(kt)
    Energias1.append(10*((1-math.exp(2/kt) )/(1+math.exp(2/kt)) ))

plt.scatter(temperaturas,Energias)
plt.scatter(kt1,Energias1)
plt.show()