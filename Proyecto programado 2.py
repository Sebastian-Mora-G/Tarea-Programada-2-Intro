"""
    ! Fecha de entrega: 28-11-2025
"""
import tkinter as tk
from tkinter import messagebox
import time
import Clases.camino as camino
import Clases.lianas as lianas
import Clases.tuneles as tuneles
import Clases.muros as muros
import Clases.jugador as jugador_clase
import Clases.enemigo as enemigo_clase
import Clases.energia as energia_clase
import random
import os

#Lista global de jugadores
nombre_jugador = ""
#Variables globales de juego
modo_actual = "escapa"
dificultad_actual = "facil"
puntaje_actual = 0
enemigos = []
tiempo_inicio = 0
juego_activo = True
ultimo_tiempo_movimiento = 0

top_jugadores_escapa = []
top_jugadores_caza = []

#COMMONS(Archivos)-----------------------------------------------------------------
class Archivo:
    def salvar_tabla_puntajes(): 
        """
        Salva en 2 archivos distintos para el top 5 de Escapa y el top 5 de caza. \n
        No hay que preocuparse por formato. Lo único, que a la lista de top_jugadores_escapa/caza
        se añadan los elementos así: ["nombre_jugador", puntaje(int)]
        """
        global top_jugadores_escapa, top_jugadores_caza
        top_5_escapa = Archivo.buscar_top_5(top_jugadores_escapa)
        top_5_caza = Archivo.buscar_top_5(top_jugadores_caza)

        top_5_escapa = str(top_5_escapa)
        top_5_caza = str(top_5_caza)

        with open("top_5_escapa.txt","w") as file:
            file.write(top_5_escapa)
        with open("top_5_caza.txt","w") as file:
            file.write(top_5_caza)


    def leer_top_5_escapa():
        """
        Lee el archivo de escapa
        """
        global top_jugadores_escapa
        try: 
            with open("top_5_escapa.txt","r") as file:
                top_jugadores_escapa = eval(file.read())
        except:
            top_jugadores_escapa = []

    def leer_top_5_caza():
        """
        Lee el archivo de Caza
        """
        global top_jugadores_caza
        try: 
            with open("top_5_caza.txt","r") as file:
                top_jugadores_caza = eval(file.read())
        except:
            top_jugadores_caza = []

    def buscar_top_5(lista:list): #van de Mayor a Menor
        """
        Busca el top 5 de la lista dada. \n
        Usado a la hora de mostrar visualmente
        """
        top_5 = []
        lista.sort(key=lambda x: x[1], reverse=True)
        if len(lista) < 5:
            return lista
        #top_5.append(lista[0]);top_5.append(lista[1]);top_5.append(lista[2]);top_5.append(lista[3]);top_5.append(lista[4])
        return lista


#Que lea los archivos:
Archivo.leer_top_5_escapa()
Archivo.leer_top_5_caza()
#----------------------------------------------------------------------------------

"""///--------------FUNCIONES GUI---------------///"""
class Gui:
    
    #E:Ninguna
    #S:Crea ventana de registro y modifica nombre_jugador global
    #R:Ninguna
    #Funcionalidad:Ventana para registro de nuevo jugador con opciones de top
    def registrar_jugador():
        
        #E:evento tecla
        #S:Ejecuta procesar_registro
        #R:Tecla debe ser Enter
        #Funcionalidad:Detectar presión de tecla Enter en campo de texto
        def enter_presionado(event): 
            procesar_registro()
        
        #E:Ninguna
        #S:Modifica nombre_jugador global o muestra error
        #R:Nombre no puede ser vacío
        #Funcionalidad:Procesar y validar nombre ingresado por usuario
        def procesar_registro():
            global nombre_jugador
            nombre = entry_nombre.get().strip()
            if nombre:
                nombre_jugador = nombre
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

        boton_puntaje_escapa = tk.Button(ventana,text="Top 5(modo escapa)" ,command=Modficacion.mostrar_top_5_escapa)
        boton_puntaje_escapa.pack(anchor="center")
        
        boton_puntaje_cazador = tk.Button(ventana,text="Top 5(modo cazador)" ,command=Modficacion.mostrar_top_5_caza)
        boton_puntaje_cazador.pack(anchor="center")

        boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
        boton_salir.pack()

        ventana.mainloop()

    #E:filas(int)-número de filas del mapa, columnas(int)-número de columnas del mapa
    #S:matriz que representa el mapa con diferentes tipos de casillas
    #R:filas y columnas deben ser enteros positivos
    #Funcionalidad:Generar mapa aleatorio con camino garantizado desde inicio hasta meta
    def generar_mapa_aleatorio(filas=15, columnas=15):
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
                        mapa[i][j] = 0 #Muro
                    elif rand_val < 0.7:
                        mapa[i][j] = 2 #Tunel
                    else:
                        mapa[i][j] = 3 #Lianas
        
        return mapa

    #E:mapa(matriz)-matriz del juego, jugador(objeto)-objeto Jugador, modo(string)-modo actual de juego
    #S:lista de objetos Enemigo
    #R:mapa debe tener dimensiones válidas, jugador debe tener posición válida
    #Funcionalidad:Crear enemigos en posiciones aleatorias válidas del mapa
    def crear_enemigos(mapa, jugador, modo):
        enemigos = []
        cantidad = Modficacion.obtener_cantidad_enemigos()
        filas = len(mapa)
        columnas = len(mapa[0])
        
        posiciones_ocupadas = set()
        
        for _ in range(cantidad):
            intentos = 0
            while intentos < 50:
                fila = random.randint(0, filas-1)
                columna = random.randint(0, columnas-1)
                posicion = (fila, columna)
                
                if (mapa[fila][columna] == 1 and 
                    (fila != jugador.fila or columna != jugador.columna) and
                    posicion not in posiciones_ocupadas):
                    
                    enemigos.append(enemigo_clase.Enemigo(fila, columna))
                    posiciones_ocupadas.add(posicion)
                    break
                intentos += 1
            
            if len(enemigos) < _ + 1:
                break
        
        return enemigos

    #E:Ninguna
    #S:Crea y muestra ventana con mapa interactivo
    #R:Debe existir nombre_jugador registrado
    #Funcionalidad:Interfaz principal del juego con mapa, controles y lógica de juego
    def mostrar_mapa():
        global enemigos, modo_actual ,tiempo_inicio, puntaje_actual, juego_activo, top_jugadores_escapa, top_jugadores_caza, dificultad_actual, nombre_jugador, ultimo_tiempo_movimiento
        
        mapa_ventana = tk.Tk()
        mapa_ventana.title("Mapa del Juego")
        mapa_ventana.geometry("800x600")
        
        main_frame = tk.Frame(mapa_ventana)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        #Frame para el mapa
        mapa_frame = tk.Frame(main_frame, width=600, height=600, bg="white")
        mapa_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mapa_frame.pack_propagate(False)
        
        #Frame para opciones
        opciones_frame = tk.Frame(main_frame, width=150, height=600, bg="lightgray")
        opciones_frame.pack(side=tk.RIGHT, fill=tk.Y)
        opciones_frame.pack_propagate(False)
        
        #Generar mapa y crear jugador
        mapa = Gui.generar_mapa_aleatorio()
        jugador = jugador_clase.Jugador(nombre_jugador,0, 0)
        energia = energia_clase.Energia(dificultad_actual)
        
        enemigos = Gui.crear_enemigos(mapa, jugador, modo_actual)
        tiempo_inicio = time.time()
        ultimo_tiempo_movimiento = time.time() * 1000  #ms
        cell_size = 35
        juego_activo = True
        
        #Matriz para almacenar los canvas de cada celda
        celdas_canvas = [[None for _ in range(len(mapa[0]))] for _ in range(len(mapa))]
        
        #E:Ninguna
        #S:Actualiza el texto del botón de modo
        #R:Ninguna
        #Funcionalidad:Refrescar texto del botón para mostrar modo actual
        def actualizar_boton_modo():
            boton_modo.config(text=f"Modo: {modo_actual.capitalize()}")
        
        #E:Ninguna
        #S:Reinicia lista de enemigos global
        #R:Ninguna
        #Funcionalidad:Recrear enemigos según modo y dificultad actual
        def reiniciar_enemigos():
            global enemigos
            enemigos = Gui.crear_enemigos(mapa, jugador, modo_actual)
            #Actualizar dificultad en energia
            energia.actualizar_dificultad(dificultad_actual)
            dibujar_enemigos()
        
        #E:Ninguna
        #S:Actualiza barra de energia visual
        #R:Ninguna
        #Funcionalidad:Dibujar barra de energia con porcentaje actual
        def actualizar_barra_energia():
            porcentaje = energia.obtener_porcentaje()
            canvas_energia.delete("barra")
            canvas_energia.delete("texto")
            
            #Dibujar fondo de barra
            canvas_energia.create_rectangle(5, 5, 145, 25, fill="lightgray", outline="black", width=1)
            
            #Dibujar barra de energia
            ancho_barra = int(140 * (porcentaje / 100))
            color = "green" if porcentaje > 50 else "yellow" if porcentaje > 20 else "red"
            canvas_energia.create_rectangle(5, 5, 5 + ancho_barra, 25, fill=color, outline="", tags="barra")
            
            #Texto de energia
            texto_estado = "CORRIENDO" if energia.corriendo else "CAMINANDO"
            canvas_energia.create_text(75, 35, text=f"Energía: {int(porcentaje)}% - {texto_estado}", 
                                    font=("Arial", 8), tags="texto")
        
        #Botones de control
        boton_modo = tk.Button(opciones_frame, text=f"Modo: {modo_actual.capitalize()}", 
                            command=lambda: [Modficacion.cambiar_modo(jugador), actualizar_boton_modo(), reiniciar_enemigos()], 
                            width=15)
        boton_modo.pack(pady=10)
        
        #Frame para dificultad
        dificultad_frame = tk.Frame(opciones_frame, bg="lightgray")
        dificultad_frame.pack(pady=10)
        
        label_dificultad = tk.Label(dificultad_frame, text="Dificultad:", bg="lightgray")
        label_dificultad.pack()
        
        boton_facil = tk.Button(dificultad_frame, text="Fácil", 
                            command=lambda: [Modficacion.cambiar_dificultad("facil"), reiniciar_enemigos()], 
                            width=10)
        boton_facil.pack(pady=2)
        
        boton_intermedio = tk.Button(dificultad_frame, text="Intermedio", 
                                    command=lambda: [Modficacion.cambiar_dificultad("intermedio"), reiniciar_enemigos()], 
                                    width=10)
        boton_intermedio.pack(pady=2)
        
        boton_dificil = tk.Button(dificultad_frame, text="Difícil", 
                                command=lambda: [Modficacion.cambiar_dificultad("dificil"), reiniciar_enemigos()], 
                                width=10)
        boton_dificil.pack(pady=2)
        
        #Label para puntaje
        label_puntaje = tk.Label(opciones_frame, text="Puntaje: 0", 
                                bg="lightgray", font=("Arial", 12, "bold"))
        label_puntaje.pack(pady=20)
        
        #Label para tiempo transcurrido
        label_tiempo = tk.Label(opciones_frame, text="Tiempo: 0s", 
                            bg="lightgray", font=("Arial", 10))
        label_tiempo.pack(pady=10)
        
        #Frame para energia
        energia_frame = tk.Frame(opciones_frame, bg="lightgray")
        energia_frame.pack(pady=10)
        
        label_energia = tk.Label(energia_frame, text="Energía:", bg="lightgray")
        label_energia.pack()
        
        canvas_energia = tk.Canvas(energia_frame, width=150, height=40, bg="lightgray", highlightthickness=0)
        canvas_energia.pack(pady=5)
        
        tk.Button(energia_frame, text="Salir", command=lambda:finalizar_juego("Se presionó el botón para salir. ")).pack()
        #Inicializar barra de energia
        actualizar_barra_energia()
        
        #E:Ninguna
        #S:Dibuja el mapa en la interfaz gráfica
        #R:Ninguna
        #Funcionalidad:Renderizar todas las celdas del mapa según su tipo
        def dibujar_mapa():
            for i in range(len(mapa)):
                for j in range(len(mapa[0])):
                    x1 = j * cell_size + 5
                    y1 = i * cell_size + 5
                    
                    cell_type = mapa[i][j]
                    
                    canvas = tk.Canvas(mapa_frame, width=cell_size, height=cell_size, 
                                    bg='white', highlightthickness=1, highlightbackground='black')
                    canvas.place(x=x1, y=y1)
                    celdas_canvas[i][j] = canvas
                    
                    #Dibujar "Meta" en la esquina inferior derecha
                    if i == len(mapa)-1 and j == len(mapa[0])-1:
                        canvas.configure(bg='gold')
                        canvas.create_text(cell_size/2, cell_size/2, text="META", 
                                        fill='black', font=("Arial", 8, "bold"))
                    elif cell_type == 0:  #Muro
                        canvas.create_line(0, cell_size/3, cell_size, cell_size/3, width=2, fill="black")
                        canvas.create_line(0, 2*cell_size/3, cell_size, 2*cell_size/3, width=2, fill="black")
                        canvas.create_line(cell_size/3, 0, cell_size/3, cell_size, width=2, fill="black")
                        canvas.create_line(2*cell_size/3, 0, 2*cell_size/3, cell_size, width=2, fill="black")
                    elif cell_type == 1:  #Camino
                        canvas.configure(bg='white')
                    elif cell_type == 2:  #Túnel
                        canvas.configure(bg='white')
                        canvas.create_oval(5, 5, cell_size-5, cell_size-5, fill='black', outline='black')
                    elif cell_type == 3:  #Lianas
                        canvas.configure(bg='green')
            
            dibujar_jugador()   
            dibujar_enemigos()
        
        #E:Ninguna
        #S:Actualiza la posición visual del jugador en el mapa
        #R:Ninguna
        #Funcionalidad:Dibujar al jugador en su posición actual
        def dibujar_jugador():
            #Limpiar posición anterior
            for i in range(len(mapa)):
                for j in range(len(mapa[0])):
                    canvas = celdas_canvas[i][j]
                    items = canvas.find_all()
                    for item in items:
                        if canvas.type(item) == "text" and canvas.itemcget(item, "text") == jugador.simbolo:
                            canvas.delete(item)
            
            #Dibujar en nueva posición
            canvas_jugador = celdas_canvas[jugador.fila][jugador.columna]
            color_jugador = "orange" if energia.corriendo else jugador.color
            canvas_jugador.create_text(cell_size/2, cell_size/2, text=jugador.simbolo, 
                                    fill=color_jugador, font=("Arial", 12, "bold"))
        
        #E:Ninguna
        #S:Dibuja todos los enemigos en el mapa
        #R:Ninguna
        #Funcionalidad:Renderizar enemigos en sus posiciones actuales
        def dibujar_enemigos():
            #Limpiar enemigos anteriores
            for i in range(len(mapa)):
                for j in range(len(mapa[0])):
                    canvas = celdas_canvas[i][j]
                    items = canvas.find_all()
                    for item in items:
                        if canvas.type(item) == "text" and canvas.itemcget(item, "text") == "👹":
                            canvas.delete(item)
            
            #Dibujar enemigos
            for enemigo in enemigos:
                canvas_enemigo = celdas_canvas[enemigo.fila][enemigo.columna]
                canvas_enemigo.create_text(cell_size/2, cell_size/2, text=enemigo.carita, 
                                        fill=enemigo.color, font=("Arial", 10, "bold"))
        
        #E:Ninguna
        #S:Actualiza el label de tiempo en la interfaz
        #R:Ninguna
        #Funcionalidad:Mostrar tiempo transcurrido actualizado cada segundo
        def actualizar_tiempo():
            if juego_activo:
                tiempo_transcurrido = int(time.time() - tiempo_inicio)
                label_tiempo.config(text=f"Tiempo: {tiempo_transcurrido}s")
                mapa_ventana.after(1000, actualizar_tiempo)
        
        #E:Ninguna
        #S:Actualiza sistema de energia periodicamente
        #R:Ninguna
        #Funcionalidad:Actualizar consumo de energia y barra visual
        def actualizar_energia():
            if juego_activo:
                tiempo_actual = time.time()
                delta_tiempo = tiempo_actual - getattr(actualizar_energia, 'ultimo_tiempo', tiempo_actual)
                setattr(actualizar_energia, 'ultimo_tiempo', tiempo_actual)
                
                energia.actualizar(delta_tiempo)
                actualizar_barra_energia()
                mapa_ventana.after(100, actualizar_energia)
        
        #Inicializar tiempo de energia
        setattr(actualizar_energia, 'ultimo_tiempo', time.time())
        
        #E:mensaje(string)-mensaje a mostrar al usuario
        #S:Finaliza el juego y cierra la ventana
        #R:Ninguna
        #Funcionalidad:Terminar partida de manera controlada guardando puntajes
        def finalizar_juego(mensaje):
            global juego_activo, modo_actual, top_jugadores_escapa, top_jugadores_caza
            
            juego_activo = False
            
            
            #AGREGAR PUNTAJE
            nuevo_jugador = [jugador.nombre_usuario, jugador.puntaje]
            
            if modo_actual == "escapa":
                top_jugadores_escapa.append(nuevo_jugador)
            else:
                top_jugadores_caza.append(nuevo_jugador)
    
            #GUARDAR
            Archivo.salvar_tabla_puntajes()
            
            #MOSTRAR MENSAJES
            messagebox.showinfo("Info", mensaje)
            respuesta = messagebox.askyesno("Salir o no", "¿Desea volver a jugar?", default="no")
            
            if not respuesta:
                messagebox.showinfo("Fin del Juego", "Gracias por jugar!")
                mapa_ventana.destroy()
                Gui.registrar_jugador()
            else:
                mapa_ventana.destroy()
                modo_actual = "escapa"
                dificultad_actual = "facil"
                puntaje_actual = 0
                enemigos = []
                tiempo_inicio = 0
                juego_activo = True
                Gui.mostrar_mapa()
        
        #E:Ninguna
        #S:Verifica condiciones de victoria/derrota y muestra mensajes
        #R:Ninguna
        #Funcionalidad:Controlar estado del juego verificando colisiones y metas
        def verificar_estado_juego():
            if not juego_activo:
                return
                
            #Verificar colisiones (solo en modo escapa)
            for enemigo in enemigos:
                if enemigo.fila == jugador.fila and enemigo.columna == jugador.columna:
                    if modo_actual == "escapa":
                        #Jugador pierde en modo escapa - SIN PUNTAJE
                        finalizar_juego("¡Te atraparon!\nNo obtienes puntaje por ser atrapado.")
                        return
                    else:
                        #En modo cazador, reubicar enemigo y dar ptos a jugador
                        if modo_actual == "facil":
                            jugador.puntaje += 200
                        elif modo_actual == "intermedio":
                            jugador.puntaje += 600
                        else:
                            jugador.puntaje += 1000
                        while True:
                            fila = random.randint(0, len(mapa)-1)
                            columna = random.randint(0, len(mapa[0])-1)
                            if mapa[fila][columna] == 1:
                                enemigo.fila = fila
                                enemigo.columna = columna
                                break
            
            #Verificar si enemigos llegaron a la meta en modo cazador
            if modo_actual == "cazador":
                for enemigo in enemigos:
                    if enemigo.fila == len(mapa)-1 and enemigo.columna == len(mapa[0])-1:
                        #Reubicar enemigo en posición aleatoria y quitar ptos a jugador
                        if modo_actual == "facil":
                            jugador.puntaje -= 100
                        elif modo_actual == "intermedio":
                            jugador.puntaje -= 300
                        else:
                            jugador.puntaje -= 500
                        while True:
                            fila = random.randint(0, len(mapa)-1)
                            columna = random.randint(0, len(mapa[0])-1)
                            if mapa[fila][columna] == 1:
                                enemigo.fila = fila
                                enemigo.columna = columna
                                break
            
            #Verificar si jugador llegó al final (modo escapa) - SOLO AQUÍ SE OBTIENE PUNTAJE
            if modo_actual == "escapa" and jugador.fila == len(mapa)-1 and jugador.columna == len(mapa[0])-1:
                tiempo_transcurrido = time.time() - tiempo_inicio
                puntaje_final = Modficacion.calcular_puntaje(tiempo_transcurrido)
                jugador.puntaje += puntaje_final
                finalizar_juego(f"¡Escapaste!\nTiempo: {int(tiempo_transcurrido)} segundos\nPuntaje final: {puntaje_final}")
        
        #E:Ninguna
        #S:Mueve todos los enemigos según el modo actual y los redibuja
        #R:Ninguna
        #Funcionalidad:Actualizar posición de enemigos automáticamente según modo
        def mover_enemigos_automatico():
            if not juego_activo:
                return
                
            for enemigo in enemigos:
                if modo_actual == "cazador":
                    #En modo cazador, enemigos van hacia la meta (esquina inferior derecha)
                    enemigo.mover_hacia_meta(len(mapa)-1, len(mapa[0])-1, len(mapa), len(mapa[0]), enemigos)
                else:
                    #En modo escapa, enemigos persiguen/huyen según comportamiento normal
                    enemigo.mover(jugador.fila, jugador.columna, modo_actual, len(mapa), len(mapa[0]), enemigos)
            
            #Recargar energia cuando los enemigos se mueven
            energia.recargar()
            actualizar_barra_energia()
            
            dibujar_enemigos()
            verificar_estado_juego()
            
            #Programar próximo movimiento solo si el juego sigue activo
            if juego_activo:
                velocidad = Modficacion.obtener_velocidad_enemigos()
                mapa_ventana.after(velocidad, mover_enemigos_automatico)
        
        #E:evento(Event)-evento de teclado
        #S:Mueve al jugador y actualiza la visualización
        #R:Tecla debe ser una flecha direccional
        #Funcionalidad:Manejar movimiento del jugador con teclado
        def tecla_presionada(event):
            if not juego_activo:
                return
            
            #Manejar tecla Shift para correr
            if event.keysym in ["Shift_L", "Shift_R"]:
                if energia.toggle_correr():
                    actualizar_barra_energia()
                    dibujar_jugador()
                return
            
            #Verificar si puede moverse (cooldown)
            tiempo_actual_ms = time.time() * 1000
            if not energia.puede_moverse(tiempo_actual_ms):
                return
            
            #Mover jugador según tecla
            if event.keysym == "Up":
                jugador.mover("up", mapa ,len(mapa), len(mapa[0]))
            elif event.keysym == "Down":
                jugador.mover("down", mapa ,len(mapa), len(mapa[0]))
            elif event.keysym == "Left":
                jugador.mover("left", mapa, len(mapa), len(mapa[0]))
            elif event.keysym == "Right":
                jugador.mover("right", mapa, len(mapa), len(mapa[0]))
            else:
                return  #No es una tecla de movimiento
            
            #Actualizar cooldown
            energia.set_proximo_movimiento(tiempo_actual_ms)
            
            dibujar_jugador()
            verificar_estado_juego()
        
        #Dibujar mapa inicial
        dibujar_mapa()
        
        #Iniciar movimiento automático de enemigos
        velocidad = Modficacion.obtener_velocidad_enemigos()
        mapa_ventana.after(velocidad, mover_enemigos_automatico)
        
        #Iniciar actualización de tiempo
        actualizar_tiempo()
        
        #Iniciar actualización de energia
        actualizar_energia()
        
        #Configurar bindings de teclado
        mapa_ventana.bind("<KeyPress>", tecla_presionada)
        mapa_ventana.bind("<Shift_L>", tecla_presionada)
        mapa_ventana.bind("<Shift_R>", tecla_presionada)
        mapa_ventana.focus_set()
        
        mapa_ventana.mainloop()

class Modficacion:
    #E:Ninguna
    #S:Muestra ventana con top 5 del modo escapa
    #R:Ninguna
    #Funcionalidad:Mostrar ranking de mejores jugadores en modo escapa
    def mostrar_top_5_escapa():
        global top_jugadores_escapa
        
        mensaje = "TOP 5 - MODO ESCAPA\n\n"
        if top_jugadores_escapa:
            for i, jugador in enumerate(top_jugadores_escapa, 1):
                if i == 6:
                    break
                mensaje += f"{i}. {jugador[0]} - Puntuación: {jugador[1]}\n"
        else:
            mensaje += "No hay jugadores en este top aún"
        
        messagebox.showinfo("Top 5 - Modo Escapa", mensaje)
    
    #E:Ninguna
    #S:Muestra ventana con top 5 del modo caza
    #R:Ninguna
    #Funcionalidad:Mostrar ranking de mejores jugadores en modo cazador
    def mostrar_top_5_caza():
        global top_jugadores_caza
        
        mensaje = "TOP 5 - MODO CAZADOR\n\n"
        if top_jugadores_caza:
            for i, jugador in enumerate(top_jugadores_caza, 1):
                mensaje += f"{i}. {jugador[0]} - Puntuación: {jugador[1]}\n"
        else:
            mensaje += "No hay jugadores en este top aún"
        
        messagebox.showinfo("Top 5 - Modo Cazador", mensaje)

    #E:jugador(objeto)-objeto Jugador a modificar
    #S:Cambia modo_actual global y modo del jugador
    #R:Ninguna
    #Funcionalidad:Alternar modo de juego entre "escapa" y "cazador"
    def cambiar_modo(jugador):
        global modo_actual
        if modo_actual == "escapa":
            modo_actual = "cazador"
            jugador.modo = "cazador"
        else:
            modo_actual = "escapa"
            jugador.modo = "escapa"
        messagebox.showinfo("Modo Cambiado", f"Modo actual: {modo_actual.capitalize()}")
    
    #E:nueva_dificultad(string)-dificultad a establecer
    #S:Cambia dificultad_actual global
    #R:nueva_dificultad debe ser "facil", "intermedio" o "dificil"
    #Funcionalidad:Establecer nivel de dificultad del juego
    def cambiar_dificultad(nueva_dificultad):
        global dificultad_actual
        dificultad_actual = nueva_dificultad
        messagebox.showinfo("Dificultad Cambiada", f"Dificultad: {dificultad_actual.capitalize()}")

    #E:Ninguna
    #S:Retorna cantidad de enemigos según dificultad
    #R:Ninguna
    #Funcionalidad:Determinar número de enemigos basado en dificultad actual
    def obtener_cantidad_enemigos():
        if dificultad_actual == "facil":
            return 5
        elif dificultad_actual == "intermedio":
            return 7
        else: #dificil
            return 9

    #E:Ninguna
    #S:Retorna intervalo de movimiento de enemigos en milisegundos
    #R:Ninguna
    #Funcionalidad:Determinar velocidad de enemigos basado en dificultad
    def obtener_velocidad_enemigos():
        if dificultad_actual == "facil":
            return 2000
        elif dificultad_actual == "intermedio":
            return 1500
        else: #dificil
            return 1000

    #E:tiempo_transcurrido(float)-tiempo en segundos desde el inicio
    #S:Retorna puntaje calculado como entero
    #R:tiempo_transcurrido debe ser un número positivo
    #Funcionalidad:Calcular puntaje basado en tiempo y dificultad
    def calcular_puntaje(tiempo_transcurrido):
        #Puntaje base máximo por dificultad
        if dificultad_actual == "facil":
            puntaje_maximo = 500
        elif dificultad_actual == "intermedio":
            puntaje_maximo = 750
        else: #dificil
            puntaje_maximo = 1000
        
        #Fórmula: puntaje = puntaje_maximo - (tiempo_en_segundos * 10)
        puntaje_calculado = max(puntaje_maximo - int(tiempo_transcurrido * 10), 0)
        
        return puntaje_calculado

if __name__ == "__main__":
    Gui.registrar_jugador()