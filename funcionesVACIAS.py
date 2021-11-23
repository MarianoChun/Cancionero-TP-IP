from configuracion import *
import random
import math
import unicodedata

import unidecode

def removerSaltosDeLinea(lista): # Remueve los \n
    lista1 = []
    for elemento in lista:
        lista1.append(elemento.strip())
    return lista1

def artistaCancion(artistaYCancion,archivo):
    archivo1 =  archivo
    x = archivo1.readline()
    cancionArtista = artistaYCancion
    cancionArtista.append(x)
    cancionArtista = removerSaltosDeLinea(cancionArtista)
    
    return cancionArtista



def letras(letra,archivo):
    archivo1 = archivo
    x = archivo1.readlines()
    letra = removerSaltosDeLinea(x)
    indice = 0
    for elemento in letra:
        elementoNuevo = elemento
        elementoNuevo = unidecode.unidecode(elementoNuevo) # Las cadenas son inmutables, hay que crear nuevas con la funcion unidecode y meterlo en una lista
        letra[indice] = elementoNuevo.lower()
        indice = indice + 1

            
    return letra


def seleccion(letra):#elige uno al azar, devuelve ese y el siguiente
    fin = len(letra) - 1
    aleatorio = random.randint(0,fin)
    n = aleatorio
    if n == len(letra)-1:
        linea1 = letra[len(letra)-1]
        linea2 = letra[0]
    else:
        linea1 = letra[n]
        linea2 = letra[n + 1]
    
    return ([str(linea1),str(linea2)])

def lectura(archivo, letra, artistaYcancion): #se queda solo con los oraciones de cierta longitud y filtra tildes por ej
    artista1 = artistaCancion(artistaYcancion,archivo)
    letra = letras(letra,archivo)

    letrasPermitidas = []

    for linea in letra:
        if len(linea) <= 44:
            letrasPermitidas.append(linea)
        
    return (artista1,letrasPermitidas)


def artista(listaArtistas):
    nombreArtista = ""
    listaArtistasNueva = []
    for linea in listaArtistas:
        for letra in linea:
            if letra != ";":
                nombreArtista = nombreArtista + letra
            else:
                listaArtistasNueva.append(nombreArtista)
                nombreArtista = ""
    return listaArtistasNueva



def puntos(rtasCorrectas):
    #devuelve el puntaje, segun seguidilla
    puntaje = 0
    if rtasCorrectas == 0:
        puntaje = -5
    elif rtasCorrectas >= 1:
        puntaje = 2 ** (rtasCorrectas - 1) # Si hay una rta correcta, hacer 2 ** 0, que es 1. Si hay dos, hacer 2 ** 1, que es 2,etc.
    return puntaje


    

def esCorrecta(palabraUsuario, artistaYCancion, correctas):
    #chequea que sea correcta, que pertenece solo a la frase siguiente. Devuelve puntaje segun seguidilla
    nombresArtistasYCanciones = artista(artistaYCancion) 
    respuestas = correctas

    for elemento in nombresArtistasYCanciones:
        if palabraUsuario == elemento:
                if correctas == 0:
                    return puntos(respuestas + 1)
                else:
                    return puntos(respuestas)

    respuestas = 0
    return puntos(respuestas)

def lecturaRecords():
    # Abrimos el archivo y lo leemos
    archivo = open("records.txt","r")
    texto = archivo.readlines()
    
    texto = removerSaltosDeLinea(texto)

    nombres = []
    puntajes = []
    numeros = []
    for i in range(5000): # Crea una lista de numeros hasta 5000, con el objetivo de comparar mas abajo si el elemento recorrido en readlines es un numero.
        numeros.append(str(i))
    
    
    for elemento in texto:
        if "Nombre:" in elemento and elemento != "":
            nombres.append(elemento)
        elif elemento in numeros and elemento != "": # Si el elemento es un numero (puntaje), sumarlo a los puntajes
            puntajes.append(elemento)
 
    
    archivo.close() 
    return (nombres,puntajes)


def escrituraRecords(nombre,puntos): # Reescribe el contenido de records. Se recorren los puntajes y se reemplaza si el puntaje ingresado como parametro es mayor al recorrido.
    archivo = open("records.txt","r")
    texto = archivo.readlines()
    texto = removerSaltosDeLinea(texto)

    nombres = []
    puntajes = []
    numeros = []
    for i in range(5000):
        numeros.append(str(i))
    
    for elemento in texto:
        if "Nombre:" in elemento and elemento != "":
            nombres.append(elemento)
        elif elemento in numeros and elemento != "": # Si el elemento es un numero (puntaje), sumarlo a los puntajes
            puntajes.append(elemento)
    archivo.close() 

    archivo = open("records.txt","w")

    puntajeReemplazado = False
    auxPuntaje = 0
    auxNombre = 0
    for i in range(10): # En este bucle se busca en que posicion "puntos" es mayor a los puntajes existentes y reemplaza este primero por un puntaje menor
        if puntajeReemplazado == False:
            if puntos > int(puntajes[i]):
                auxPuntaje = puntajes[i]
                auxNombre = nombres[i]
                
                nombres[i] = "Nombre:" + str(nombre)
                puntajes[i] = puntos
                #print(puntajes,nombres)
                puntajeReemplazado = True
    
    for i in range(10): # Este bucle tiene como objetivo ir corriendo los puntajes y los nombres en caso de que se reemplace un valor de "puntajes".
        if int(auxPuntaje) > int(puntajes[i]):
            
            aux2Puntajes = puntajes[i]
            aux2Nombres = nombres[i]

            puntajes[i] = auxPuntaje
            nombres[i] = auxNombre

            auxPuntaje = aux2Puntajes
            auxNombre = aux2Nombres

    
                
    # Reescribimos el archivo "records" con los nuevos valores de nombres y puntajes
    for i in range(10):
        archivo.write(str(nombres[i])+"\n"+str(puntajes[i])+"\n")
        

    archivo.close() 
    






