"""
    ! Fecha de entrega: 28-11-2025
    """
import tkinter as tk
from tkinter import messagebox

#CLASES DE LOS CAMINOS ==========================================================================
class Camino:
    def __init__(self):
        self.tipo = "Camino"
        
    def permitir_todos(self): #Esta f tal vez sobre. Pero mejor ponerla por si acaso
        """
        * Todos pueden pasar. Por ende, true
        """
        return True
    
class Lianas:
    def init__(self):
        self.tipo = "Lianas"
        
    def permitir_cazadores(self,tipo_jugador): 
        """
        Devuelve True si el jugador es Cazador, False si es jugador \n
        O sea, devuelve True si puede pasar por este terreno. 
        """
        if tipo_jugador == "Cazador":
            return True
        return False

class Tuneles:
    def __init__(self):
        self.tipo = "Tuneles"
    
    def permitir_jugadores(self,tipo_jugador):
        """
        Devuelve True si el jugador es Jugador, False si es Cazador \n
        O sea, devuelve True si puede pasar por este terreno.
        """
        if tipo_jugador == "Jugador":
            return True
        return False
class Muros:
    def __init__(self):
        self.tipo = "Muros"
        
    def permitir_nadie(self): #Esta f tal vez sobre. Pero mejor ponerla por si acaso
        """
        * Nadie puede pasar. Por ende, false
        """
        return False

#Lista global de jugadores
user_jugadores = []

"""///--------------FUNCIONES GUI---------------///"""
class Gui:
    #E: Ninguna
    #S: Modifica lista user_jugadores
    #R: Nombre no vacío
    #Funcionalidad: Ventana registro jugador
    def registrar_jugador():
        
        """#E: Evento tecla \n
        #S: Ejecuta procesar_registro\n
        #R: Solo responde a tecla Enter\n
        #Funcionalidad: Detectar Enter"""
        def enter_presionado(event): #El event se pone obligatorio o todo se cae
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
                #ventana.quit()                                              #Si dejamos esto, destruye toda la ventana. Mejor comentarlo
                #ventana.destroy()
            else:
                messagebox.showerror("Error", "Tu nombre no puede ser vacío, escribe uno válido")

        ventana = tk.Tk()
        ventana.title("Registro Jugador")
        ventana.geometry("300x300")

        label_instruccion = tk.Label(ventana, text="Escribe tu nombre:")
        label_instruccion.pack(pady=10)

        entry_nombre = tk.Entry(ventana, width=30)
        entry_nombre.pack(pady=10)
        entry_nombre.focus()

        boton_registrar = tk.Button(ventana, text="Comenzar Juego", command=procesar_registro)
        boton_registrar.pack(pady=10)

        boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy);boton_salir.pack()


        ventana.mainloop()

if __name__ == "__main__":
    Gui.registrar_jugador()
#registrar_jugador()