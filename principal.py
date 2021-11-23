#! /usr/bin/env python
import os, random, sys, math

import pygame
from pygame.locals import *
from configuracion import *
from extras import *

from funcionesVACIAS import *


#Funcion principal

# Definimos las variables de la dificultad, de acuerdo al click del jugador, cambiamos a True para la opcion elegida
principiante = False
intermedio = False
experto = False

def main():
    mouseClick = False
    while True:
        pygame.init()
        
       
        screen = pygame.display.set_mode((ANCHO, ALTO))
        screen.fill((0,0,0))

        pygame.display.set_caption("Cancionero...")
        
        defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
        dibujarTexto("Menu principal",defaultFont,(0,0,255),screen,420,20)

        # Almacenamos la posicion del mouse
        mouseX, mouseY = pygame.mouse.get_pos()

        # Creamos rectangulos y los dibujamos en la pantalla
        botonJugar = pygame.Rect(420,150,200,50)
        botonRecords = pygame.Rect(420,300,200,50)

        pygame.draw.rect(screen,(255,255,255),botonJugar)
        pygame.draw.rect(screen,(255,255,255),botonRecords)

        textoBoton(screen,botonJugar,"Jugar")
        textoBoton(screen,botonRecords,"Records")
        
        pygame.display.update()

        # Si el mouse esta sobre los botones y clickeamos, mouseClick vale True y entramos a la respectiva ventana
        if botonJugar.collidepoint((mouseX,mouseY)):
            if mouseClick:
                niveles()
        if botonRecords.collidepoint((mouseX,mouseY)):
            if mouseClick:    
                records()
        
        mouseClick = False

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouseClick = True


def niveles():
    mouseClick = False
    while True:
        pygame.init()
        
        screen = pygame.display.set_mode((ANCHO, ALTO))
        screen.fill((0,0,0))

        pygame.display.set_caption("Cancionero...")
        
        defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
        dibujarTexto("Niveles",defaultFont,(0,0,255),screen,420,20)

        # Almacenamos la posicion del mouse
        mouseX, mouseY = pygame.mouse.get_pos()

        # Creamos rectangulos y los dibujamos en la pantalla
        botonPrincipiante = pygame.Rect(420,150,200,50)
        botonIntermedio = pygame.Rect(420,300,200,50)
        botonExperto = pygame.Rect(420,450,200,50)

        pygame.draw.rect(screen,(255,255,255),botonPrincipiante)
        pygame.draw.rect(screen,(255,255,255),botonIntermedio)
        pygame.draw.rect(screen,(255,255,255),botonExperto)

        textoBoton(screen,botonPrincipiante,"Principiante")
        textoBoton(screen,botonIntermedio,"Intermedio")
        textoBoton(screen,botonExperto,"Experto")

        pygame.display.update()

        # Para que las dificultades anteriormente definidas al principio del programa cambien a True, usamos "global" para modificarla desde una variable local.
        if botonPrincipiante.collidepoint((mouseX,mouseY)):
            if mouseClick:
                global principiante 
                principiante = True
                juego()
        if botonIntermedio.collidepoint((mouseX,mouseY)):
            if mouseClick:
                global intermedio 
                intermedio = True    
                juego()
        if botonExperto.collidepoint((mouseX,mouseY)):
            if mouseClick:
                global experto 
                experto = True    
                juego()

        mouseClick = False

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouseClick = True

    
def juego():
        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        #pygame.mixer.init()

        #Preparar la ventana
        pygame.display.set_caption("Cancionero...")
        screen = pygame.display.set_mode((ANCHO, ALTO))
        #definimos funciones

        # Sonidos
        sonidoCorrecta = pygame.mixer.Sound(".\\sonidos\\Rise01.ogg")
        sonidoSeguidilla = pygame.mixer.Sound(".\\sonidos\\Rise03.ogg")
        sonidoIncorrecta = pygame.mixer.Sound(".\\sonidos\\Downer01.ogg")
        sonidoBurla = pygame.mixer.Sound(".\\sonidos\\doh.wav")
        
        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial
        artistaYcancion=[]
        puntos = 0
        palabraUsuario = ""
        letra=[]
        correctas=0
        elegidos= []
        masDeUnaVuelta = False
        errores = 0 # Cantidad de errores cometidos seguidos, se reinicia a 0 si se acierta una respuesta
        erroresNecesarios = 0 # Errores necesarios para obtener una ayuda
        
        #elige una cancion de todas las disponibles
        # De acuerdo a la dificultad elegida, modificamos el valor de N para desplegar una cantidad de canciones acorde a la opcion escogida.
        if principiante:
            N = 3
            # Hay ayuda para la primera vuelta
            azar=random.randrange(1,N+1)
        elif intermedio:
            N = 6
            # No hay ayuda al dar la primera vuelta
            erroresNecesarios = 4 # Errores necesarios para contar con una ayuda
            azar=random.randrange(1,N+1)
        elif experto:
            N = 9
            # No hay ayuda al dar la primera vuelta
            erroresNecesarios = 8 # Errores necesarios para contar con una ayuda
            azar=random.randrange(1,N+1)

        elegidos.append(azar) #la agrega a la lista de los ya elegidos
        archivo = open(".\\letras\\"+str(azar)+".txt","r", encoding='utf-8') # abre el archivo elegido con unicode.
    
        #lectura del archivo y filtrado de caracteres especiales, la primer linea es el artista y cancion
        lecturaFiltrada = lectura(archivo, letra, artistaYcancion)
        # Letra
        lecturaFiltrada = lecturaFiltrada[1]
        
        #elige una linea al azar y su siguiente
        lista=seleccion(lecturaFiltrada)
        
##        print(lista)

        ayuda = "Cancionero"
        #menu(screen,ayuda)
        dibujar(screen, palabraUsuario, lista, puntos, segundos, ayuda)
        

        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
            	fps = 3

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letraApretada = dameLetraApretada(e.key)
                    palabraUsuario += letraApretada
                    if e.key == K_BACKSPACE:
                        palabraUsuario = palabraUsuario[0:len(palabraUsuario)-1]
                    if e.key == K_RETURN:
                        #chequea si es correcta y suma o resta puntos
                        sumar=esCorrecta(palabraUsuario, artistaYcancion, correctas)
                        
                        puntos+=sumar
                        
                        if sumar>0:
                            if correctas < 1:
                                sonidoCorrecta.play() # Si es una opcion correcta sin seguidilla, ejecutar este sonido
                            else:
                                sonidoSeguidilla.play() # Si es una opcion correcta en seguidilla, ejecutar este sonido
                            errores = 0
                            correctas=correctas+1
                        else:
                            if palabraUsuario != "":
                                # Si es una opcion incorrecta, sumar errores y ejecutar sonido de respuesta incorrecta
                                errores += 1
                                correctas=0
                                sonidoIncorrecta.play() 
                       
                        if len(elegidos)==N:
                                elegidos=[]
                                masDeUnaVuelta = True
                
                        azar=random.randrange(1,N+1)
                        while(azar in elegidos):
                            azar=random.randrange(1,N+1)

                        elegidos.append(azar)
                        if palabraUsuario == "": # Si no se escribe nada, burlarse y dar ayuda
                            ayuda = artistaYcancion[0]
                            sonidoBurla.play()
                        else:
                            ayuda = "Cancionero"

                        # Proporciona ayudas de acuerdo al nivel de dificultad
                        if masDeUnaVuelta == True and principiante: 
                            ayuda = artistaYcancion[0]
                        elif errores >= erroresNecesarios and intermedio:
                            ayuda = artistaYcancion[0]
                        elif errores >= erroresNecesarios and experto:
                            ayuda = artistaYcancion[0]

                        archivo= open(".\\letras\\"+str(azar)+".txt","r", encoding='utf-8')
                        palabraUsuario = ""
                        #lectura del archivo y filtrado de caracteres especiales
                        artistaYcancion=[]
                        letra = []
                        lecturaFiltrada = lectura(archivo, letra, artistaYcancion)
                        lecturaFiltrada = lecturaFiltrada[1]

                        #elige una linea al azar y su siguiente
                        lista=seleccion(lecturaFiltrada)

            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000
            
                    
            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, palabraUsuario, lista, puntos, segundos, ayuda)

            pygame.display.flip()
        # Se reestablece el fondo negro para solicitar el nombre a poner en records.
        screen.fill(COLOR_FONDO)
        titulo = "Ingrese su nombre para guardar su record"

        dibujarNombreRecords(screen,palabraUsuario,titulo)
        
        recordIngresado = True
        while recordIngresado:
            for e in pygame.event.get():

                    #QUIT es apretar la X en la ventana
                    if e.type == QUIT:
                        pygame.quit()
                        return()

                    #Ver si fue apretada alguna tecla
                    if e.type == KEYDOWN:
                        letraApretada = dameLetraApretada(e.key)
                        palabraUsuario += letraApretada
                        if e.key == K_BACKSPACE:
                            palabraUsuario = palabraUsuario[0:len(palabraUsuario)-1]
                        if e.key == K_RETURN:
                            nombrePuntajes = lecturaRecords() # Se lee el archivo de records
                            nombres = nombrePuntajes[0] # Se toma la lista de nombres del return de lecturaRecords()
                            puntajes = nombrePuntajes[1] # Se toma la lista de puntajes del return de lecturaRecords()
                            
                            escrituraRecords(palabraUsuario,puntos)

                            recordIngresado = False
                            


            screen.fill(COLOR_FONDO)
            dibujarNombreRecords(screen,palabraUsuario,titulo)
            
            pygame.display.flip()

        # Dibujamos de nuevo la pantalla
        palabraUsuario = ""
        screen.fill(COLOR_FONDO)
        dibujarNombreRecords(screen,palabraUsuario,titulo)
        pygame.display.flip()
        while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return


        archivo.close()

def records():
    programa = True
    while programa:
        
        pygame.init()
        screen = pygame.display.set_mode((ANCHO, ALTO))
        screen.fill((0,0,0))
        pygame.display.set_caption("Cancionero...")
        
        defaultFont= pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
        dibujarTexto("Records",defaultFont,(251,255,5),screen,420,20)
        
        for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        programa = False

        nombreYPuntajes = lecturaRecords() # Se lee el archivo de records
        nombres = nombreYPuntajes[0] # Se toma la lista de nombres del return de lecturaRecords()
        puntajes = nombreYPuntajes[1] # Se toma la lista de puntajes del return de lecturaRecords()

        posX = 100
        posY = 50
        # Dibujamos los nombres almacenados en "nombres"
        for nombre in nombres:
            dibujarTexto(str(nombre),defaultFont,(0,0,255),screen,posX,posY)
            posY = posY + 55
        
        posX = 500 # Asignamos una posicion nueva para la posicion X
        posY = 50 # Reestablecemos la posicion en Y para los puntajes

        # Dibujamos los puntajes almacenados en "puntajes"
        for puntaje in puntajes:
            dibujarTexto("Puntaje:",defaultFont,(0,0,255),screen,posX,posY)
            dibujarTexto(str(puntaje),defaultFont,(0,0,255),screen,posX + 120,posY) # Se le suma 120 para correrlo mas a la derecha.
            posY = posY + 55
        pygame.display.flip()
#Programa Principal ejecuta Main
if __name__ == "__main__":
    main()

