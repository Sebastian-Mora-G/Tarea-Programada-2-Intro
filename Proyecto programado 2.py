"""
    ! Fecha de entrega: 28-11-2025
    TODO: cuando terminemos, hay que hacer el repositorio público en GitHub para la evaluacion 
    """
import tkinter as tk
from tkinter import messagebox #Iconos posibles: 'error', 'info', 'question', 'warning'
import time
import Clases.camino as camino
import Clases.lianas as lianas
#CLASES DE LOS CAMINOS ==========================================================================


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
        def enter_presionado(event): #El event se pone obligatorio o todo se cae. Nota Sebas: quité el event, y no se me cayó
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
                #ventana.quit()                                              #Si dejamos esto, destruye toda la ventana. Mejor comentarlo
                #ventana.destroy()
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

        boton_registrar = tk.Button(ventana, text="Comenzar Juego", command=procesar_registro)
        boton_registrar.pack(pady=10)

        boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy);boton_salir.pack()

        ventana.mainloop()

if __name__ == "__main__":
    Gui.registrar_jugador()
#registrar_jugador()