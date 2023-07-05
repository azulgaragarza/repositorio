import matplotlib.pyplot as plt
import csv
listaG=[]
listaN=[]

with open("docs\\google.csv") as f:
    n=csv.reader(f,delimiter=";")
    for i in n:
        listaG.append(i[0].split(","))
listaG.remove(listaG[0])

with open("docs\\nike.csv") as l:
    s=csv.reader(l,delimiter=";")
    for x in s:
        listaN.append(x[0].split(","))
listaN.remove(listaN[0])

#Aca se crean las listas para los ejes (X,Y) (para las gráficas)
ejeX=[]
n=0
while n<len(listaG):
   ejeX.append(n) 
   n=n+1

listaGY=[]
listaNY=[]
for y in listaG:
    listaGY.append(float(y[1]))
for z in listaN:
    listaNY.append(float(z[1]))
    
listaGN=[]
for i in listaG:
    p= ((float(i[1])-min(listaGY))/(max(listaGY)-min(listaGY)))
    listaGN.append(p)

listaNN=[]
for j in listaN:
    p= ((float(j[1])-min(listaNY))/(max(listaNY)-min(listaNY)))
    listaNN.append(p)

listaGP=[]
for n in listaG:
    p= (((float(n[1])-float(listaG[0][1]))/float(listaG[0][1]))*100)
    listaGP.append(p)

listaNP=[]
for m in listaN:
    p= (((float(m[1])-float(listaN[0][1]))/float(listaN[0][1]))*100)
    listaNP.append(p)



#Creo una lista que incluya los precios de Google en el primer trimestre (9o dias)
listaG1T=[]
for t in range(90):
    listaG1T.append(listaGY[t])
    
#Calculo la caida porcentual de Google en el primer trimestre
maxG=max(listaG1T)
minG=min(listaG1T)
caidaP=(((minG-maxG)/maxG)*100)
print("La caida porcentual de Google es de:", round(caidaP, 2), "%")

#Aca empieza la grafica 1
plt.plot(ejeX, listaGN, label="Google") 
plt.plot(ejeX, listaNN, label="Nike")
plt.grid()
plt.legend()

#Calculo el porcentaje de repunte de Google
repunte=(((listaGY[-1]-minG)/minG)*100)
print("El porcentaje de repunte de Google es de:", round(repunte, 2), "%")

#Aca empiezan las dos graficas juntas
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Primera gráfica en el primer eje (Google)
axs[0].plot(ejeX, listaGN, label="Google")
axs[0].plot(ejeX, listaNN, label="Nike")
axs[0].set_title('Precios normalizados entre 0 y 1')
axs[0].grid(True)

# Segunda gráfica en el segundo eje (Nike)
axs[1].plot(ejeX, listaGP, label='Google')
axs[1].plot(ejeX, listaNP, label='Nike')
axs[1].set_title('Tasa de variacion como porcentaje del precio inicial')
axs[1].grid(True)

# Agregar leyendas
axs[0].legend(loc='upper left')
axs[1].legend(loc='upper left')

# Ajustar el espacio entre los subplots
plt.subplots_adjust(wspace=0.3)

# Mostrar la figura
plt.show()

