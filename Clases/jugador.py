class Jugador:
    def __init__(self, fila, columna): #Nota: y si le agregamos a jugador un atributo "username" o algo así? Además del puntaje, con el fin de q sea más fácil tratarlo con archivos
        self.fila = fila
        self.columna = columna
        self.simbolo = "★"
        self.color = "yellow"
    
    def mover(self, direccion, filas_max, columnas_max):
        """Mueve al jugador en la dirección especificada, validando límites del mapa"""
        if direccion == "up":
            self.fila = max(0, self.fila - 1)
        elif direccion == "down":
            self.fila = min(filas_max - 1, self.fila + 1)
        elif direccion == "left":
            self.columna = max(0, self.columna - 1)
        elif direccion == "right":
            self.columna = min(columnas_max - 1, self.columna + 1)