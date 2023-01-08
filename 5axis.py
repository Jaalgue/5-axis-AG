#Algoritmo génetico - Robot de 5 ejes planos
#Computación Bioinspirada - GIIC UEX
#Javier Alonso Guerra

import turtle
import random
import math
import time

#Longuitud de los diferentes tramos del robot
La, Lb, Lc, Ld, Le = 0.35, 0.3, 0.25, 0.2, 0.15

pob = 100
mut = 0.4
kotE = 0.009
maxG = 100

def uR(k = 1.0):
    return k*random.random()

def uT(k = 1.0):
    return k*random.triangular(-1.0,1.0)

def u012():
    return random.randrange(3)

def iniR5():
    return [uR(), uR(), uR(), uR(), uR()]

def posR5(a, b, c, d, e):
    x = La*math.cos(a) + Lb*math.cos(a+b) + Lc*math.cos(a+b+c) + Ld*math.cos(a+b+c+d) + Le*math.cos(a+b+c+d+e)
    y = La*math.sin(a) + Lb*math.sin(a+b) + Lc*math.sin(a+b+c) + Ld*math.sin(a+b+c+d) + Le*math.sin(a+b+c+d+e)
    return x,y

def fitR5(x,y):
    return math.sqrt(math.pow(x-oX,2) + math.pow(y-oY,2))

def punto(t,x,y,col):
    t.goto(300*x,300*y)
    t.dot(5,col)

def pinta(sol,t,c="yellow",d=1):
    for s in sol:
        punto(t,*s[1],c)
    time.sleep(d)

def isol(s):
    z = s[:]
    for i in range(5):
        z[i] *= 2*math.pi
    x,y = posR5(*z)
    return [s,[x,y],fitR5(x,y)]   

def ini_sol(t):
    sol = []
    for i in range(2*pob):
        s = isol(iniR5())
        sol.append(s)
    pinta(sol,t)
    sol = sorted(sol,key=lambda s: s[2])[:pob]
    pinta(sol,t,c="blue")
    return sol

def n01(n): return n%1.0

def muta(s):     
    m = s[:]
    i = random.randrange(5)
    m[i] = n01(m[i] + uT(0.3))
    return m

def cruza(p,m):     
    u = u012()

    if u < 1:
        h1 = p[0][:]
        h2 = m[0][:]
        h1[3] = m[0][3]
        h1[4] = m[0][4]
        h2[3] = p[0][3]
        h2[4] = p[0][4]

    elif u < 2:
        h1 = p[0][:]
        h2 = m[0][:]
        h1[2] = 0.5*(p[0][2] + m[0][2])
        h2[2] = 0.5*(p[0][2] + m[0][2])
        h1[3] = m[0][3]
        h1[4] = m[0][4]
        h2[3] = p[0][3]
        h2[4] = p[0][4]

    else:
        h1 = m[0][:]
        h2 = p[0][:]
        h1[0] = p[0][0]
        h1[1] = p[0][1]
        h2[0] = m[0][0]
        h2[1] = m[0][1]

    if uR() < mut: h1 = muta(h1)
    if uR() < mut: h2 = muta(h2)
    return [isol(h1),isol(h2)]

def cruzaPonderado(p, m):
    h1 = p[0][:]
    h2 = m[0][:]
    
    for i in range (5):
        h1[i] = ((p[0][i] * 0.75) + (m[0][i] * 0.25))
        h2[i] = ((p[0][i] * 0.25) + (m[0][i] * 0.75))
    
    if uR() < mut: h1 = muta(h1)
    if uR() < mut: h2 = muta(h2)

    return [isol(h1), isol(h2)]

def nocaza(s,g):
    return s[2] > kotE and g < maxG

def jump(k=1.0):
    nok = True
    while nok:
        new = isol(iniR5())
        nok = k/3 < new[2] > k
    return new[1][0],new[1][1]

def torneo(sol):
    return sorted(random.sample(sol,2), key = lambda z: z[2])

def mejor(sol):
    return sorted(sol)

#### INIZ
win = turtle.Screen()
win.bgcolor("black")

eje = turtle.Turtle()
eje.speed(0)
eje.ht()
eje.pencolor("white")
eje.fd(340)
eje.fd(-660)
eje.home()
eje.lt(90)
eje.fd(340)
eje.fd(-660)
eje.up()

bicho = turtle.Turtle()
bicho.speed(0)
bicho.ht()
bicho.pencolor("gray")
bicho.up()

rob = turtle.Turtle()
rob.speed(0)
rob.ht()
rob.up()

oX,oY = uT(0.7),uT(0.7)
punto(bicho,oX,oY,"red")
sol = ini_sol(rob)

## LOOP
while True:
    gen = 0
    bs = sol[0]
    fs = sol[0]
    rob.clear()
    punto(rob,*bs[1],"blue")
    
    while nocaza(bs,gen):
        
        txt = "("+str(round(oX,2))+","+str(round(oY,2))+") -- "
        txt += "[" + str(gen) + "] --> " + str(round(bs[2],5))
        win.title(txt)

        new = sol[:3]  ##Elitismo
        #new = [] ##No elitismo
        
        for s in sol:
            resultado = torneo(sol) ## Realizamos un torneo 
            #resultado = mejor(sol) ## Elegimos siempre el mejor
            new += cruza(s,resultado[0]) ##Realizamos el cruce de 1 corte
            #new += cruzaPonderado(s, resultado[0]) #Realizamos el cruce ponderado

        sol = sorted(new,key=lambda s: s[2])[:pob]

        bs = sol[0]
        punto(rob,*bs[1],"blue")
        if bs[2] > kotE:
            fs = sol[0]
            gen += 1

    print("("+str(round(oX,2))+","+str(round(oY,2))+")")
    txt = " -- [" + str(gen) +"] " + str(round(fs[2],5)) + " -- "
    for i in range(3):
        txt += str(round(fs[0][i]*360,2)) + " "
    print(txt)
    
    bicho.clear()
    punto(bicho,oX,oY,"gray")
    bicho.down()
    oX,oY = jump()
    punto(bicho,oX,oY,"red")

    for s in sol: s[2] = fitR5(*s[1])
    sol = sorted(sol,key=lambda s: s[2])