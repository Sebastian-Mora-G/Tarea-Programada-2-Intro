class Jugador:
    def __init__(self, nombre_usuario, fila, columna): 
        self.nombre_usuario = nombre_usuario
        self.puntaje = 0 #Se debe modificar al ganar
        self.modo = "escapa" #Default
        self.fila = fila
        self.columna = columna
        self.simbolo = "★"
        self.color = "yellow"
    
    def mover(self, direccion, mapa, filas_max, columnas_max):
        """Mueve al jugador en la dirección especificada, validando límites del mapa"""
        if direccion == "up":
            if not Jugador.verificar_terreno(mapa[0][self.fila-1] ,self.modo):
                return
            self.fila = max(0, self.fila - 1)
            
        elif direccion == "down":
            if not Jugador.verificar_terreno(mapa[filas_max - 1][self.fila + 1] ,self.modo):
                return
            self.fila = min(filas_max - 1, self.fila + 1)
            
        elif direccion == "left":
            if not Jugador.verificar_terreno(mapa[0][self.columna - 1] ,self.modo):
                return
            self.columna = max(0, self.columna - 1)
            
        elif direccion == "right":
            if not Jugador.verificar_terreno(mapa[columnas_max - 1][self.columna + 1] ,self.modo):
                return
            self.columna = min(columnas_max - 1, self.columna + 1)

    def verificar_terreno(terreno, modo):
        """
        E: terreno dnd se va a mover y el modo en el que se encuentra \n
        S: bool, dependiendo si puede o no pasar \n
        R: - \n
        Verifica el terreno dnd se quiere mover el jugador y si puede moverse por ahí \n
        """
        if modo == "escapa":
            if terreno  == 1 or terreno == 2:
                return True
            return False
        else:
            if terreno == 1 or terreno == 3:
                return True
            return False