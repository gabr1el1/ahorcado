#importamos las librerías que necesitarémos tkinter para la GUI, random para barajear los nombres, time para hacer menos brusca la interfaz,
#ImageTk e Image para manejar las imagenes
import tkinter
import random
import time
from PIL import Image,ImageTk



#creamos la ventana y la configuramos
ventana=tkinter.Tk()
ventana.title("Ahorcado, Estados de México")
ventana.geometry("800x650")
ventana.resizable(0,0)

#hacemos un arreglo con las palabras a adivinar
estados=["JALISCO","VERACRUZ","OAXACA","NAYARIT","COLIMA","CIUDAD DE MÉXICO",
         "CHIHUAHUA","SONORA","COAHUILA","NUEVO LEÓN","TABASCO","ESTADO DE MÉXICO",
         "YUCATÁN","QUINTANA ROO","CHIAPAS","PUEBLA","SAN LUIS POTOSÍ",
         "CAMPECHE","AGUASCALIENTES","TLAXCALA","HIDALGO","MORELOS","DURANGO",
         "QUERÉTARO","ZACATECAS","BAJA CALIFORNIA","BAJA CALIFORNIA SUR",
         "MICHOACÁN","TAMAULIPAS","GUANAJUATO","SINALOA"]
         
#generamos un index al azar
nestado=random.randint(0,30)


#creamos una lista vacía para almacenar las imágenes del ahorcado
etiquetas=[]
#inicializamos el contador de errores, 6 va a ser el máximo
cont_error=0
#inicializamos el numero de letras para compararlo con los contadores descritos más adelante para saber si ganó el usuario
numletras=0

#creamos y colocamos las etiquetas de los __ y los espacios
for i in range(len(estados[nestado])):
    if estados[nestado][i]==" ":

        etiquetas.append(tkinter.Label(ventana,text="    ",font=("Arial",14)))

        etiquetas[i].pack(side = tkinter.LEFT)
    else:
        
        etiquetas.append(tkinter.Label(ventana,text="___",font=("Arial",14)))
        
        etiquetas[i].pack(side = tkinter.LEFT)
        numletras+=1


#almacenamos las imágenes del ahorcado

pasos=[None]*7
for i in range(1,7):
    imagen_agrega=Image.open(f"imagenes_ahorcado/paso {i}.jpg").resize((160,190))
    pasos[i]=ImageTk.PhotoImage(imagen_agrega)




#creamos y colocamos la etiqueta que mostrará las imagenes de los pasos
etiqueta=tkinter.Label(ventana)
etiqueta.place(x=310,y=50)



#creamos variables para manipular la posición de los botones que tienen las letras

contador_x=10
contador_y=350
contador_espacio=0
#creamos una lista vacía para los botones
botones=[]
#creamos una lista con los caracteres de nuestro teclado
caracter=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P",
          "Q","R","S","T","U","V","W","X","Y","Z","Á","É","Í","Ó","Ú"]

#hacemos un ciclo para crear y colocar nuestros botones, hacemos un 
# uso particular de lambda que nos permite asignar argumentos diferentes para cada uno de los botones
for i in range(32):
    
    contador_espacio+=1
    
    boton=tkinter.Button(ventana,text=caracter[i],width="5",height="2",font=("Arial",8),
                         command=lambda let=caracter[i],op=1: eleccion(let,op),bg="blue",fg="white",relief="ridge")
    botones.append(boton)
        
    
    
    if contador_espacio==9:
        botones[i].place(x=contador_x,y=contador_y)
        contador_y+=50
        contador_x=10
        contador_espacio=0
            
    else:
        botones[i].place(x=contador_x,y=contador_y)
        contador_x+=45
        


#creamos la función si se va a utilizar la caja de texto con el botón Enter (Return)
def enviarReturnKey(event):
    texto=cajaTexto.get()
    texto=texto.upper()
    
    eleccion(texto,2)
    

cajaTexto=tkinter.Entry(ventana,font=("Impact",18),relief="groove")
cajaTexto.place(x=500,y=350)

cajaTexto.bind("<Return>",enviarReturnKey)



#creamos la función de va a utilizar la caja de texto con el botón
def enviarBoton():
    texto=cajaTexto.get()
    texto=texto.upper()
    eleccion(texto,2)
    

    
botonCaja=tkinter.Button(ventana,text="Adivinar",width="36",height="1",command=enviarBoton,bg="blue",fg="white")
botonCaja.place(x=500,y=385)




contador_gana=0

#creamos un diccionario para más adelante borrar los botones si acertó la letra
diccionario={}
for i in range (32):
    diccionario[caracter[i]]=botones[i]

def eleccion(letra,opcion):
    global cont_error,contador_gana
    #nuestra opción 1 es que haya usado los botones 
    if opcion==1:
           
        cont=0
        #si la letra se encuentra en la palabra a adivinar
        if letra in estados[nestado]:

            #borramos el botón acertado
            botones[botones.index(diccionario[letra])].destroy()
            
            #recorremos la palabra para ver cuantas veces está la letra seleccionada      
            for c in estados[nestado]:
                #si la encuentra en una posición 
                if letra==c:
                    #cambia las etiquetas que tienen los espacios y las __
                    etiquetas[cont].config(text=letra)
                    #un contador que cuenta el número letras que has adivinado (si existe la letra que seleccionaste más de una vez, el contador incrementará en más de uno
                    contador_gana+=1
                #necesitaremos un contador cont para rque en caso se que haya encontrado minimo una letra en la palabra sepa que __ cambiar
                cont+=1
                
            
            if contador_gana==numletras:
                tkinter.Label(ventana,text="¡BIEN HECHO!",fg="Red",font=("BIEN HECHO",30)).place(x=10,y=500)
                for i in range(len(estados[nestado])):
                    etiquetas[i].config(text=estados[nestado][i])
                for i in range(len(botones)):
                    botones[i].destroy()
                
                cajaTexto.destroy()
                botonCaja.destroy()
                ventana.update()
                
                
                
        #si la letra no se encuentra en la palabra a adivinar se suma un error al cont_error       
        else:
            cont_error+=1
            etiqueta.config(image=pasos[cont_error])  
            #si se cometen 6 errores mostrará una etiqueta y destruirá los widgets
            if cont_error==6:
                
                tkinter.Label(text="Perdiste :( "+"     El estado era  "+estados[nestado],font=("Impact",20)).place(x=10,y=500)
                cajaTexto.destroy()
                botonCaja.destroy()
                for i in range(len(botones)):
                    botones[i].destroy()
                ventana.update()
                
    #la opción 2 es la caja de texto  
    elif(opcion==2):
        #si "letra" el argumento que mandó el botón de la caja de texto a la función es igual a la palabra a adivinar el usuario gana
        if letra==estados[nestado]:
            tkinter.Label(ventana,text="¡BIEN HECHO!",fg="Red",font=("Impact",30)).place(x=10,y=500)
            #cambiamos las letras por los __ ya que adivinó
            for i in range(len(estados[nestado])):
                etiquetas[i].config(text=estados[nestado][i])
            #destruimos los widgets que pueden hacer que falle el programa si el usuario hace algo después de ganar

            #botonCaja.destroy()
            cajaTexto.destroy()
            #borramos botones
            for i in range(len(botones)):
                    botones[i].destroy()
            #refrescamos para que se vean los cambios
            ventana.update()
            
            
        #si se comete un error aumenta el cont_error   
        else:
            cont_error+=1
            #se cambia la etiqueta para que la imagen del ahorcado concuerde con el número de error
            etiqueta.config(image=pasos[cont_error])
            #si se cometen 6 errores mostrará una etiqueta y destruirá los widgets
            if cont_error==6:
                tkinter.Label(text="Perdiste :( "+"    El estado era "+estados[nestado],font=("Impact",20)).place(x=10,y=500)
                cajaTexto.destroy()
                botonCaja.destroy()
                for i in range(len(botones)):
                    botones[i].destroy()
                ventana.update()        
                

ventana.mainloop()
