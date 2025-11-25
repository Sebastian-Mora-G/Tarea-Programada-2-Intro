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
import Clases.enemigo as enemigo_clase
import random
#Lista global de jugadores
user_jugadores = []
#Variables globales de juego
modo_actual = "escapa"
dificultad_actual = "facil"
puntaje_actual = 0
enemigos = []
tiempo_inicio = 0
juego_activo = True  # Variable para controlar si el juego está activo

top_jugadores_escapa = []
top_jugadores_caza = []

#COMMONS(Archivos)-----------------------------------------------------------------

def salvar_tabla_puntajes(): 
    """
    Salva en 2 archivos distintos para el top 5 de Escapa y el top 5 de caza
    """
    global top_jugadores_escapa, top_jugadores_caza
    top_5_escapa = buscar_top_5(top_jugadores_escapa)
    top_5_caza = buscar_top_5(top_jugadores_caza)

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
    except FileNotFoundError:
        top_jugadores_escapa = "No hay jugadores en el top 5"

def leer_top_5_caza():
    """
    Lee el archivo de Caza
    """
    global top_jugadores_caza
    try: 
        with open("top_5_caza.txt","r") as file:
            top_jugadores_caza = eval(file.read())
    except FileNotFoundError:
        top_jugadores_caza = "No hay jugadores en el top 5"

def buscar_top_5(lista:list): #van de Mayor a Menor
    lista.sort(key=lambda x: x[1], reverse=True)
    if len(lista) < 5:
        return lista
    top_5 = lista[0] + lista[1] + lista[2] + lista[3] + lista[4]
    return top_5
#----------------------------------------------------------------------------------

top_jugadores_escapa = []
top_jugadores_caza = []

#COMMONS(Archivos)-----------------------------------------------------------------

def salvar_tabla_puntajes(): 
    """
    Salva en 2 archivos distintos para el top 5 de Escapa y el top 5 de caza
    """
    global top_jugadores_escapa, top_jugadores_caza
    top_5_escapa = buscar_top_5(top_jugadores_escapa)
    top_5_caza = buscar_top_5(top_jugadores_caza)

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
    except FileNotFoundError:
        top_jugadores_escapa = "No hay jugadores en el top 5"

def leer_top_5_caza():
    """
    Lee el archivo de Caza
    """
    global top_jugadores_caza
    try: 
        with open("top_5_caza.txt","r") as file:
            top_jugadores_caza = eval(file.read())
    except FileNotFoundError:
        top_jugadores_caza = "No hay jugadores en el top 5"

def buscar_top_5(lista:list): #van de Mayor a Menor
    lista.sort(key=lambda x: x[1], reverse=True)
    if len(lista) < 5:
        return lista
    top_5 = lista[0] + lista[1] + lista[2] + lista[3] + lista[4]
    return top_5
#----------------------------------------------------------------------------------

"""///--------------FUNCIONES GUI---------------///"""
class Gui:
    
    #E: Ninguna
    #S: Modifica lista user_jugadores
    #R: Ninguna
    #Funcionalidad: Ventana registro jugador
    def registrar_jugador():
        
        #E: Evento tecla 
        #S: Ejecuta procesar_registro
        #R: Solo responde a tecla Enter
        #Funcionalidad: Detectar Enter
        def enter_presionado(event): 
            procesar_registro()
        
        #E: Ninguna
        #S: Modifica user_jugadores o muestra error
        #R: Nombre no vacío
        #Funcionalidad: Procesar nombre ingresado
        def procesar_registro():
            nombre = entry_nombre.get().strip()
            
            if nombre:
                user_jugadores.append(nombre)
                messagebox.showinfo("Éxito", f"Jugador '{nombre}' registrado")
                ventana.destroy()
                Gui.mostrar_mapa()
            else:
                messagebox.showerror("Error", "Tu nombre no puede ser vacío, escribe uno válido", icon="warning")
        #TOP 5----------------------------------------------------------------------------------------------------
        def mostrar_top_5_escapa():
            mensaje = ""
            leer_top_5_escapa()
            global top_jugadores_escapa
            try:
                for jugador in top_jugadores_escapa:
                    mensaje += f"Jugador {jugador[0]} | Puntuación: {jugador[1]}"
                messagebox.showinfo("Info", mensaje)
            except:
                messagebox.showinfo("Error", "No hay jugadores en este Top")
        def mostrar_top_5_caza():
            mensaje = ""
            leer_top_5_caza()
            global top_jugadores_caza
            try:
                for jugador in top_jugadores_caza:
                    mensaje += f"Jugador {jugador[0]} | Puntuación: {jugador[1]}"
                messagebox.showinfo("Info", mensaje)
            except:
                messagebox.showinfo("Error", "No hay jugadores en este Top")
        #-------------------------------------------------------------------------------------------------------------

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

        boton_puntaje_escapa = tk.Button(ventana,text="Top 5(modo escapa)" ,command=mostrar_top_5_escapa);boton_puntaje_escapa.pack(anchor="center")
        
        boton_puntaje_cazador = tk.Button(ventana,text="Top 5(modo cazador)" ,command=mostrar_top_5_caza);boton_puntaje_cazador.pack(anchor="center")

        boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
        boton_salir.pack()

        ventana.mainloop()

    #E: filas y columnas (opcionales) para dimensiones del mapa
    #S: Retorna matriz que representa el mapa
    #R: filas y columnas deben ser enteros positivos
    #Funcionalidad: Generar mapa aleatorio con diferentes tipos de casillas
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

    #E: Ninguna
    #S: Cambia el modo de juego entre "escapa" y "cazador"
    #R: Ninguna
    #Funcionalidad: Alternar modo de juego
    def cambiar_modo():
        global modo_actual
        if modo_actual == "escapa":
            modo_actual = "cazador"
        else:
            modo_actual = "escapa"
        messagebox.showinfo("Modo Cambiado", f"Modo actual: {modo_actual.capitalize()}")

    #E: nueva_dificultad: string con la dificultad
    #S: Cambia la dificultad actual del juego
    #R: nueva_dificultad debe ser "facil", "intermedio" o "dificil"
    #Funcionalidad: Establecer nivel de dificultad
    def cambiar_dificultad(nueva_dificultad):
        global dificultad_actual
        dificultad_actual = nueva_dificultad
        messagebox.showinfo("Dificultad Cambiada", f"Dificultad: {dificultad_actual.capitalize()}")

    #E: Ninguna
    #S: Retorna cantidad de enemigos según dificultad
    #R: Ninguna
    #Funcionalidad: Determinar número de enemigos basado en dificultad
    def obtener_cantidad_enemigos():
        if dificultad_actual == "facil":
            return 5  # Fácil: 5 enemigos
        elif dificultad_actual == "intermedio":
            return 7  # Intermedio: 7 enemigos
        else: #dificil
            return 9  # Difícil: 9 enemigos

    #E: Ninguna
    #S: Retorna intervalo de movimiento de enemigos en milisegundos según dificultad
    #R: dificultad_actual debe estar definida
    #Funcionalidad: Determinar velocidad de enemigos basado en dificultad
    def obtener_velocidad_enemigos():
        if dificultad_actual == "facil":
            return 2000  # 2 segundos
        elif dificultad_actual == "intermedio":
            return 1500  # 1.5 segundos
        else: #dificil
            return 1000  # 1 segundo

    #E: mapa: matriz del juego, jugador: objeto Jugador, modo: modo actual
    #S: Lista de objetos Enemigo
    #R: mapa debe tener dimensiones válidas
    #Funcionalidad: Crear enemigos en posiciones según el modo
    def crear_enemigos(mapa, jugador, modo):
        enemigos = []
        cantidad = Gui.obtener_cantidad_enemigos()
        filas = len(mapa)
        columnas = len(mapa[0])
        
        if modo == "escapa":
            #Modo Escapa: enemigos en posiciones aleatorias distribuidas
            posiciones_ocupadas = set()
            
            for _ in range(cantidad):
                #Buscar posición aleatoria válida (camino) que no sea la del jugador
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
                    
        else:
            #Modo Cazador: enemigos juntos en el centro
            centro_fila = filas // 2
            centro_columna = columnas // 2
            
            #Crear más posiciones alrededor del centro según la cantidad necesaria
            posiciones_centro = []
            radio = 2  #Radio máximo alrededor del centro
            
            #Generar todas las posiciones dentro del radio
            for i in range(-radio, radio + 1):
                for j in range(-radio, radio + 1):
                    #Excluir la posición del jugador si está en el centro
                    if (centro_fila + i != jugador.fila or centro_columna + j != jugador.columna):
                        posiciones_centro.append((centro_fila + i, centro_columna + j))
            
            #Mezclar las posiciones para variedad
            random.shuffle(posiciones_centro)
            
            #Tomar solo posiciones válidas hasta alcanzar la cantidad necesaria
            enemigos_creados = 0
            for pos in posiciones_centro:
                if enemigos_creados >= cantidad:
                    break
                    
                fila, columna = pos
                if (0 <= fila < filas and 0 <= columna < columnas and 
                    mapa[fila][columna] == 1):
                    enemigos.append(enemigo_clase.Enemigo(fila, columna))
                    enemigos_creados += 1
            
            #Si aún no tenemos suficientes enemigos, buscar posiciones aleatorias cerca del centro
            if enemigos_creados < cantidad:
                for _ in range(cantidad - enemigos_creados):
                    intentos = 0
                    while intentos < 20:
                        #Buscar posiciones cerca del centro (radio más amplio)
                        fila = centro_fila + random.randint(-3, 3)
                        columna = centro_columna + random.randint(-3, 3)
                        posicion = (fila, columna)
                        
                        if (0 <= fila < filas and 0 <= columna < columnas and 
                            mapa[fila][columna] == 1 and
                            (fila != jugador.fila or columna != jugador.columna) and
                            posicion not in [(e.fila, e.columna) for e in enemigos]):
                            
                            enemigos.append(enemigo_clase.Enemigo(fila, columna))
                            break
                        intentos += 1
        
        return enemigos

    #E: tiempo_transcurrido: tiempo en segundos desde el inicio
    #S: Retorna puntaje calculado basado en tiempo y dificultad
    #R: tiempo_transcurrido debe ser un número positivo
    #Funcionalidad: Calcular puntaje basado en tiempo (menos tiempo = más puntos)
    def calcular_puntaje(tiempo_transcurrido):
        #Puntaje base máximo por dificultad
        if dificultad_actual == "facil":
            puntaje_maximo = 500
        elif dificultad_actual == "intermedio":
            puntaje_maximo = 750
        else: #dificil
            puntaje_maximo = 1000
        
        #Fórmula: puntaje = puntaje_maximo - (tiempo_en_segundos * 10)
        #Esto significa que por cada segundo que pase, pierdes 10 puntos
        puntaje_calculado = max(puntaje_maximo - int(tiempo_transcurrido * 10), 0)
        
        return puntaje_calculado

    #E: Ninguna
    #S: Crea y muestra ventana con mapa interactivo
    #R: Ninguna
    #Funcionalidad: Mostrar mapa del juego con jugador movible y enemigos
    def mostrar_mapa():
        global enemigos, tiempo_inicio, puntaje_actual, juego_activo
        
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
        jugador = jugador_clase.Jugador(0, 0)
        enemigos = Gui.crear_enemigos(mapa, jugador, modo_actual)
        tiempo_inicio = time.time()
        cell_size = 35
        juego_activo = True
        
        #Matriz para almacenar los canvas de cada celda
        celdas_canvas = [[None for _ in range(len(mapa[0]))] for _ in range(len(mapa))]
        
        #E: Ninguna
        #S: Actualiza el botón de modo con el texto correcto
        #R: Ninguna
        #Funcionalidad: Refrescar texto del botón de modo
        def actualizar_boton_modo():
            boton_modo.config(text=f"Modo: {modo_actual.capitalize()}")
        
        #E: Ninguna
        #S: Reinicia el juego con nueva configuración de enemigos
        #R: Ninguna
        #Funcionalidad: Recrear enemigos según modo y dificultad actual
        def reiniciar_enemigos():
            global enemigos
            enemigos = Gui.crear_enemigos(mapa, jugador, modo_actual)
            dibujar_enemigos()
        
        #Botones de control
        boton_modo = tk.Button(opciones_frame, text=f"Modo: {modo_actual.capitalize()}", 
                            command=lambda: [Gui.cambiar_modo(), actualizar_boton_modo(), reiniciar_enemigos()], 
                            width=15)
        boton_modo.pack(pady=10)
        
        #Frame para dificultad
        dificultad_frame = tk.Frame(opciones_frame, bg="lightgray")
        dificultad_frame.pack(pady=10)
        
        label_dificultad = tk.Label(dificultad_frame, text="Dificultad:", bg="lightgray")
        label_dificultad.pack()
        
        boton_facil = tk.Button(dificultad_frame, text="Fácil", 
                            command=lambda: [Gui.cambiar_dificultad("facil"), reiniciar_enemigos()], 
                            width=10)
        boton_facil.pack(pady=2)
        
        boton_intermedio = tk.Button(dificultad_frame, text="Intermedio", 
                                    command=lambda: [Gui.cambiar_dificultad("intermedio"), reiniciar_enemigos()], 
                                    width=10)
        boton_intermedio.pack(pady=2)
        
        boton_dificil = tk.Button(dificultad_frame, text="Difícil", 
                                command=lambda: [Gui.cambiar_dificultad("dificil"), reiniciar_enemigos()], 
                                width=10)
        boton_dificil.pack(pady=2)
        
        #Label para puntaje (solo mostrará puntaje si ganas)
        label_puntaje = tk.Label(opciones_frame, text="Puntaje: 0", 
                                bg="lightgray", font=("Arial", 12, "bold"))
        label_puntaje.pack(pady=20)
        
        #Label para tiempo transcurrido
        label_tiempo = tk.Label(opciones_frame, text="Tiempo: 0s", 
                            bg="lightgray", font=("Arial", 10))
        label_tiempo.pack(pady=10)
        
        #E: Ninguna
        #S: Dibuja el mapa en la interfaz gráfica
        #R: Ninguna
        #Funcionalidad: Renderizar todas las celdas del mapa según su tipo
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
                        canvas.create_line(0, cell_size/3, cell_size, cell_size/3, width=2)
                        canvas.create_line(0, 2*cell_size/3, cell_size, 2*cell_size/3, width=2)
                        canvas.create_line(cell_size/3, 0, cell_size/3, cell_size, width=2)
                        canvas.create_line(2*cell_size/3, 0, 2*cell_size/3, cell_size, width=2)
                    elif cell_type == 1:  #Camino
                        canvas.configure(bg='white')
                    elif cell_type == 2:  #Túnel
                        canvas.configure(bg='white')
                        canvas.create_oval(5, 5, cell_size-5, cell_size-5, fill='black', outline='black')
                    elif cell_type == 3:  #Lianas
                        canvas.configure(bg='green')
            
            dibujar_jugador()
            dibujar_enemigos()
        
        #E: Ninguna
        #S: Actualiza la posición visual del jugador en el mapa
        #R: Ninguna
        #Funcionalidad: Dibujar al jugador en su posición actual
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
            canvas_jugador.create_text(cell_size/2, cell_size/2, text=jugador.simbolo, 
                                    fill=jugador.color, font=("Arial", 12, "bold"))
        
        #E: Ninguna
        #S: Dibuja todos los enemigos en el mapa
        #R: Ninguna
        #Funcionalidad: Renderizar enemigos en sus posiciones actuales
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
        
        #E: Ninguna
        #S: Actualiza el label de tiempo en la interfaz
        #R: Ninguna
        #Funcionalidad: Mostrar tiempo transcurrido actualizado
        def actualizar_tiempo():
            if juego_activo:
                tiempo_transcurrido = int(time.time() - tiempo_inicio)
                label_tiempo.config(text=f"Tiempo: {tiempo_transcurrido}s")
                #Programar próxima actualización
                mapa_ventana.after(1000, actualizar_tiempo)
        
        #E: Ninguna
        #S: Finaliza el juego y cierra la ventana
        #R: Ninguna
        #Funcionalidad: Terminar partida de manera controlada
        def finalizar_juego(mensaje):
            global juego_activo
            juego_activo = False
            messagebox.showinfo("Fin del Juego", mensaje)
            mapa_ventana.destroy()
        
        #E: Ninguna
        #S: Verifica condiciones de victoria/derrota y muestra mensajes
        #R: Ninguna
        #Funcionalidad: Controlar estado del juego
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
            
            #Verificar si enemigos llegaron a la meta en modo cazador
            if modo_actual == "cazador":
                for enemigo in enemigos:
                    if enemigo.fila == len(mapa)-1 and enemigo.columna == len(mapa[0])-1:
                        #Reubicar enemigo en posición aleatoria
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
                puntaje_final = Gui.calcular_puntaje(tiempo_transcurrido)
                finalizar_juego(f"¡Escapaste!\nTiempo: {int(tiempo_transcurrido)} segundos\nPuntaje final: {puntaje_final}")
        
        #E: Ninguna
        #S: Mueve todos los enemigos según el modo actual y los redibuja
        #R: Ninguna
        #Funcionalidad: Actualizar posición de enemigos automáticamente
        def mover_enemigos_automatico():
            if not juego_activo:
                return
                
            for enemigo in enemigos:
                if modo_actual == "cazador":
                    #En modo cazador, enemigos van hacia la meta (esquina inferior derecha)
                    enemigo.mover_hacia_meta(len(mapa)-1, len(mapa[0])-1, len(mapa), len(mapa[0]))
                else:
                    #En modo escapa, enemigos persiguen/huyen según comportamiento normal
                    enemigo.mover(jugador.fila, jugador.columna, modo_actual, len(mapa), len(mapa[0]))
            
            dibujar_enemigos()
            verificar_estado_juego()
            
            #Programar próximo movimiento solo si el juego sigue activo
            if juego_activo:
                velocidad = Gui.obtener_velocidad_enemigos()
                mapa_ventana.after(velocidad, mover_enemigos_automatico)
        
        #E: Evento de teclado
        #S: Mueve al jugador y actualiza la visualización
        #R: Tecla debe ser una flecha direccional
        #Funcionalidad: Manejar movimiento del jugador con teclado
        def tecla_presionada(event):
            if not juego_activo:
                return
                
            if event.keysym == "Up":
                jugador.mover("up", len(mapa), len(mapa[0]))  #Usar método mover de la clase Jugador
                dibujar_jugador() 
                jugador.mover("up", len(mapa), len(mapa[0]))
            elif event.keysym == "Down":
                jugador.mover("down", len(mapa), len(mapa[0]))
            elif event.keysym == "Left":
                jugador.mover("left", len(mapa), len(mapa[0]))
            elif event.keysym == "Right":
                jugador.mover("right", len(mapa), len(mapa[0]))
            
            dibujar_jugador()
            verificar_estado_juego()
        
        #Dibujar mapa inicial
        dibujar_mapa()
        
        #Iniciar movimiento automático de enemigos
        velocidad = Gui.obtener_velocidad_enemigos()
        mapa_ventana.after(velocidad, mover_enemigos_automatico)
        
        #Iniciar actualización de tiempo
        actualizar_tiempo()
        
        #Configurar bindings de teclado
        mapa_ventana.bind("<KeyPress>", tecla_presionada)
        mapa_ventana.focus_set()  #Asegurar que la ventana reciba eventos de teclado
        mapa_ventana.focus_set()
        
        mapa_ventana.mainloop()

if __name__ == "__main__":
    Gui.registrar_jugador()