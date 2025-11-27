class Jugador:
    def __init__(self, nombre_usuario, fila, columna): 
        self.nombre_usuario = nombre_usuario
        self.puntaje = 0 #Se debe modificar al ganar
        self.modo = "escapa" #Default
        self.fila = fila
        self.columna = columna
        self.simbolo = "★"
        self.color = "blue"
    
    def mover(self, direccion, mapa, filas_max, columnas_max):
        fila_siguiente = 0
        columna_siguiente = 0
        """Mueve al jugador en la dirección especificada, validando límites del mapa"""
        if direccion == "up":
            fila_siguiente = max(0, self.fila - 1)
            columna_siguiente = self.columna
            if not Jugador.verificar_terreno(mapa[fila_siguiente][columna_siguiente] ,self.modo):
                return
            self.fila = fila_siguiente
            
        elif direccion == "down":
            fila_siguiente = min(filas_max - 1, self.fila + 1)
            columna_siguiente = self.columna
            if not Jugador.verificar_terreno(mapa[fila_siguiente][columna_siguiente] ,self.modo):
                return
            self.fila = fila_siguiente 
            
        elif direccion == "left":
            fila_siguiente = self.fila
            columna_siguiente = max(0, self.columna - 1)
            if not Jugador.verificar_terreno(mapa[fila_siguiente][columna_siguiente] ,self.modo):
                return
            self.columna = columna_siguiente
            
        elif direccion == "right":
            fila_siguiente = self.fila
            columna_siguiente = min(columnas_max - 1, self.columna + 1)
            if not Jugador.verificar_terreno(mapa[fila_siguiente][columna_siguiente] ,self.modo):
                return
            self.columna = columna_siguiente

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