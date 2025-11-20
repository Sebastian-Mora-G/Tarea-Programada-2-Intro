"""
    ! Fecha de entrega: 28-11-2025
    TODO: cuando terminemos, hay que hacer el repositorio público en GitHub para la evaluacion 
    """
import tkinter as tk
from tkinter import messagebox #Iconos posibles: 'error', 'info', 'question', 'warning'
import time
import Clases.camino as camino
import Clases.lianas as lianas
import Clases.tuneles as tuneles
import Clases.muros as muros
import Clases.jugador as jugador_clase
import random
#CLASES DE LOS CAMINOS ==========================================================================


#Lista global de jugadores
user_jugadores = []

"""///--------------FUNCIONES GUI---------------///"""
class Gui:
    #TODO: agregar el __init__. Podemos hacer que cree la ventana, tipo como el profe lo hizo en el ejemplo de los autos de carreras con Threads. 
    """E: Ninguna
    S: Modifica lista user_jugadores \
    R: Nombre no vacío
    Funcionalidad: Ventana registro jugador"""
    def registrar_jugador():
        
        """#E: Evento tecla \n
        #S: Ejecuta procesar_registro\n
        #R: Solo responde a tecla Enter\n
        #Funcionalidad: Detectar Enter"""
        def enter_presionado(event): 
            procesar_registro()
        
        def procesar_registro():
            """
            #E: Ninguna \n
            #S: Modifica user_jugadores o muestra error \n
            #R: Nombre no vacío \n
            #Funcionalidad: Procesar nombre ingresado \n
            """
            nombre = entry_nombre.get().strip()
            
            if nombre:
                user_jugadores.append(nombre)
                messagebox.showinfo("Éxito", f"Jugador '{nombre}' registrado")
                ventana.destroy()
                Gui.mostrar_mapa()
            else:
                messagebox.showerror("Error", "Tu nombre no puede ser vacío, escribe uno válido", icon="warning")

        ventana = tk.Tk()
        ventana.title("Registro Jugador")
        ventana.geometry("300x300")

        label_instruccion = tk.Label(ventana, text="Escribe tu nombre:")
        label_instruccion.pack(pady=10)

        entry_nombre = tk.Entry(ventana, width=30)
        entry_nombre.pack(pady=10)
        entry_nombre.focus()
        entry_nombre.bind("<Return>", enter_presionado)

        boton_registrar = tk.Button(ventana, text="Comenzar Juego", command=procesar_registro)
        boton_registrar.pack(pady=10)

        boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy);boton_salir.pack()

        ventana.mainloop()

    def generar_mapa_aleatorio(filas=15, columnas=15): #Por ahora solo es visual, debemos implementar los efectos de cada casilla
        #0: Muro, 1: Camino, 2: Túnel, 3: Lianas
        mapa = [[0 for _ in range(columnas)] for _ in range(filas)]
        
        #Crear camino básico desde inicio hasta fin
        x, y = 0, 0
        mapa[x][y] = 1
        
        while x < filas-1 or y < columnas-1:
            if random.random() < 0.5 and x < filas-1:
                x += 1
            elif y < columnas-1:
                y += 1
            mapa[x][y] = 1
        
        #Rellenar resto del mapa aleatoriamente
        for i in range(filas):
            for j in range(columnas):
                if mapa[i][j] == 0:
                    rand_val = random.random()
                    if rand_val < 0.4:
                        mapa[i][j] = 0
                    elif rand_val < 0.7:
                        mapa[i][j] = 2
                    else:
                        mapa[i][j] = 3
        
        return mapa

    def mostrar_mapa():
        mapa_ventana = tk.Tk()
        mapa_ventana.title("Mapa del Juego")
        mapa_ventana.geometry("800x600")
        
        main_frame = tk.Frame(mapa_ventana)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        #Frame para el mapa
        mapa_frame = tk.Frame(main_frame, width=600, height=600, bg="white")
        mapa_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mapa_frame.pack_propagate(False)
        
        #Frame para opciones futuras como correr(si no logramos hacerlo con shift, ponemos un botón) y los tops
        opciones_frame = tk.Frame(main_frame, width=150, height=600, bg="lightgray")
        opciones_frame.pack(side=tk.RIGHT, fill=tk.Y)
        opciones_frame.pack_propagate(False)
        
        #Generar mapa y crear jugador usando la clase importada
        mapa = Gui.generar_mapa_aleatorio()
        jugador = jugador_clase.Jugador(0, 0)  #Jugador empieza en posición (0,0)
        cell_size = 35
        #Matriz para almacenar los canvas de cada celda y poder actualizar el jugador
        celdas_canvas = [[None for _ in range(len(mapa[0]))] for _ in range(len(mapa))]
        
        def dibujar_mapa():
            for i in range(len(mapa)):
                for j in range(len(mapa[0])): #va calculando y posicionando cada celda del mapa, en base a coordenadas
                    x1 = j * cell_size + 5
                    y1 = i * cell_size + 5
                    
                    cell_type = mapa[i][j]
                    canvas = tk.Canvas(mapa_frame, width=cell_size, height=cell_size, 
                                      bg='white', highlightthickness=1, highlightbackground='black')
                    canvas.place(x=x1, y=y1)
                    celdas_canvas[i][j] = canvas  #Guardar referencia al canvas
                    
                    if cell_type == 0:  #Muro con forma de tablero de gato
                        #Líneas horizontales
                        canvas.create_line(0, cell_size/3, cell_size, cell_size/3, width=2)
                        canvas.create_line(0, 2*cell_size/3, cell_size, 2*cell_size/3, width=2)
                        #Líneas verticales
                        canvas.create_line(cell_size/3, 0, cell_size/3, cell_size, width=2)
                        canvas.create_line(2*cell_size/3, 0, 2*cell_size/3, cell_size, width=2)
                    elif cell_type == 1:  #Camino
                        canvas.configure(bg='white')
                    elif cell_type == 2:  #Túnel
                        canvas.configure(bg='white')
                        canvas.create_oval(5, 5, cell_size-5, cell_size-5, fill='black', outline='black')
                    elif cell_type == 3:  #Lianas
                        canvas.configure(bg='green')
            
            #Dibujar jugador en su posición inicial después de crear todo el mapa
            dibujar_jugador()
        
        def dibujar_jugador():
            #Limpiar posición anterior del jugador (eliminar estrella de todas las celdas)
            for i in range(len(mapa)):
                for j in range(len(mapa[0])):
                    canvas = celdas_canvas[i][j]
                    #Buscar y eliminar la estrella si existe en esta celda
                    items = canvas.find_all()
                    for item in items:
                        if canvas.type(item) == "text":  #Si es texto (la estrella)
                            canvas.delete(item)
            
            #Dibujar jugador en nueva posición actual
            canvas_jugador = celdas_canvas[jugador.fila][jugador.columna]
            canvas_jugador.create_text(cell_size/2, cell_size/2, text=jugador.simbolo, 
                                     fill=jugador.color, font=("Arial", 12, "bold"))
        
        def tecla_presionada(event):
            #Detectar teclas de flecha y mover jugador en dirección correspondiente volviendolo a dibujar y borrandolo en su pos anterior
            if event.keysym == "Up":
                jugador.mover("up", len(mapa), len(mapa[0]))  #Usar método mover de la clase Jugador
                dibujar_jugador()
            elif event.keysym == "Down":
                jugador.mover("down", len(mapa), len(mapa[0]))
                dibujar_jugador()
            elif event.keysym == "Left":
                jugador.mover("left", len(mapa), len(mapa[0]))
                dibujar_jugador()
            elif event.keysym == "Right":
                jugador.mover("right", len(mapa), len(mapa[0]))
                dibujar_jugador()
        
        #Dibujar mapa inicial con todas las celdas
        dibujar_mapa()
        
        #Configurar bindings de teclado para capturar eventos de flechas
        mapa_ventana.bind("<KeyPress>", tecla_presionada)
        mapa_ventana.focus_set()  #Asegurar que la ventana reciba eventos de teclado
        
        mapa_ventana.mainloop()

if __name__ == "__main__":
    Gui.registrar_jugador()