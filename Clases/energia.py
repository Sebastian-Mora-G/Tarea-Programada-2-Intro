#Funcionalidad:Representar y gestionar sistema de energia del jugador
class Energia:
    def __init__(self, dificultad="facil"):
        self.energia_actual = 100
        self.energia_maxima = 100
        self.corriendo = False
        self.cooldown_movimiento = 0
        self.cooldown_base = 500  #ms entre movimientos normales
        self.dificultad = dificultad
    
    #E:Ninguna
    #S:Retorna estado de energia actual
    #R:Ninguna
    #Funcionalidad:Obtener porcentaje de energia para mostrar en barra
    def obtener_porcentaje(self):
        return (self.energia_actual / self.energia_maxima) * 100
    
    #E:Ninguna
    #S:Modifica estado de carrera
    #R:Energia debe ser mayor a 0 para activar carrera
    #Funcionalidad:Alternar estado de carrera del jugador
    def toggle_correr(self):
        if self.energia_actual > 0:
            self.corriendo = not self.corriendo
            return True
        else:
            self.corriendo = False
            return False
    
    #E:delta_tiempo(float)-tiempo transcurrido desde ultima actualizacion
    #S:Modifica energia_actual
    #R:delta_tiempo debe ser positivo
    #Funcionalidad:Actualizar energia basado en estado de carrera y tiempo
    def actualizar(self, delta_tiempo):
        if self.corriendo:
            #CONSUMO AL CORRER
            consumo_base = 35  #por segundo
            if self.dificultad == "facil":
                consumo = consumo_base * 0.8  #28 por segundo
            elif self.dificultad == "intermedio":
                consumo = consumo_base  #35 por segundo
            else: #dificil
                consumo = consumo_base * 1.3  #45.5 por segundo
            
            self.energia_actual = max(0, self.energia_actual - consumo * delta_tiempo)
            if self.energia_actual <= 0:
                self.corriendo = False
        else:
            #CONSUMO BAJO AL CAMINAR
            consumo_base = 6  #por segundo al caminar
            if self.dificultad == "facil":
                consumo = consumo_base * 0.5  #3 por segundo
            elif self.dificultad == "intermedio":
                consumo = consumo_base  #6 por segundo
            else: #dificil
                consumo = consumo_base * 1.2  #7.2 por segundo
            
            self.energia_actual = max(0, self.energia_actual - consumo * delta_tiempo)
    
    #E:Ninguna
    #S:Modifica energia_actual
    #R:Ninguna
    #Funcionalidad:Recargar energia basado en dificultad
    def recargar(self):
        recarga_base = 12  #por movimiento de enemigo (AUMENTADO de 6 a 12)
        if self.dificultad == "facil":
            recarga = recarga_base * 1.2  #14.4 (antes 9)
        elif self.dificultad == "intermedio":
            recarga = recarga_base  #12 (antes 6)
        else: #dificil
            recarga = recarga_base * 1.1  #13.2 (antes 4.8)
        
        self.energia_actual = min(self.energia_maxima, self.energia_actual + recarga)
    
    #E:Ninguna
    #S:Retorna cooldown actual en ms
    #R:Ninguna
    #Funcionalidad:Obtener tiempo de espera entre movimientos
    def obtener_cooldown_movimiento(self):
        if self.corriendo:
            return 0  #Sin cooldown al correr
        else:
            return self.cooldown_base
    
    #E:Ninguna
    #S:Retorna booleano indicando si puede moverse
    #R:Ninguna
    #Funcionalidad:Verificar si ha pasado el cooldown necesario para moverse
    def puede_moverse(self, tiempo_actual):
        return tiempo_actual >= self.cooldown_movimiento
    
    #E:tiempo_actual(int)-tiempo actual en ms
    #S:Modifica cooldown_movimiento
    #R:Ninguna
    #Funcionalidad:Establecer tiempo del proximo movimiento permitido
    def set_proximo_movimiento(self, tiempo_actual):
        self.cooldown_movimiento = tiempo_actual + self.obtener_cooldown_movimiento()
    
    #E:nueva_dificultad(string)-nueva dificultad a establecer
    #S:Modifica dificultad interna
    #R:dificultad debe ser "facil", "intermedio" o "dificil"
    #Funcionalidad:Actualizar dificultad para calculos de energia
    def actualizar_dificultad(self, nueva_dificultad):
        self.dificultad = nueva_dificultad