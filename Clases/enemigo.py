class Enemigo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.carita = "👹"
        self.color = "red"
    
    #Funcionalidad: Decidir movimiento del enemigo según modo de juego
    def mover(self, jugador_fila, jugador_columna, modo, filas_mapa, columnas_mapa):
        if modo == "escapa":
            #Perseguir al jugador
            return self._perseguir(jugador_fila, jugador_columna, filas_mapa, columnas_mapa)
        else:
            #Huir del jugador
            return self._huir(jugador_fila, jugador_columna, filas_mapa, columnas_mapa)
    
    #Funcio: para el modo escapa, permite que los enemigos vayan a la meta
    def mover_hacia_meta(self, meta_fila, meta_columna, filas_mapa, columnas_mapa):
        nueva_fila = self.fila
        nueva_columna = self.columna
        
        #Decidir dirección hacia la meta
        if abs(meta_fila - self.fila) > abs(meta_columna - self.columna):
            #Moverse verticalmente hacia la meta
            if meta_fila > self.fila and self.fila < filas_mapa - 1:
                nueva_fila += 1
            elif meta_fila < self.fila and self.fila > 0:
                nueva_fila -= 1
        else:
            #Moverse horizontalmente hacia la meta
            if meta_columna > self.columna and self.columna < columnas_mapa - 1:
                nueva_columna += 1
            elif meta_columna < self.columna and self.columna > 0:
                nueva_columna -= 1
        
        #Actualizar posición
        self.fila = nueva_fila
        self.columna = nueva_columna
        return nueva_fila, nueva_columna
    
    #Funcionalidad: Movimiento de persecución hacia el jugador
    def _perseguir(self, jugador_fila, jugador_columna, filas_mapa, columnas_mapa):
        #Moverse hacia el jugador (algoritmo simple)
        nueva_fila = self.fila
        nueva_columna = self.columna
        
        #Decidir dirección prioritaria
        if abs(jugador_fila - self.fila) > abs(jugador_columna - self.columna):
            #Moverse verticalmente
            if jugador_fila < self.fila and self.fila > 0:
                nueva_fila -= 1
            elif jugador_fila > self.fila and self.fila < filas_mapa - 1:
                nueva_fila += 1
        else:
            #Moverse horizontalmente
            if jugador_columna < self.columna and self.columna > 0:
                nueva_columna -= 1
            elif jugador_columna > self.columna and self.columna < columnas_mapa - 1:
                nueva_columna += 1
        
        #Actualizar posición
        self.fila = nueva_fila
        self.columna = nueva_columna
        return nueva_fila, nueva_columna
    
    
    #Funcionalidad: Movimiento de huida del jugador
    def _huir(self, jugador_fila, jugador_columna, filas_mapa, columnas_mapa):
        #Moverse lejos del jugador
        nueva_fila = self.fila
        nueva_columna = self.columna
        
        #Decidir dirección de huida
        if abs(jugador_fila - self.fila) > abs(jugador_columna - self.columna):
            #Huír verticalmente
            if jugador_fila < self.fila and self.fila < filas_mapa - 1:
                nueva_fila += 1
            elif jugador_fila > self.fila and self.fila > 0:
                nueva_fila -= 1
        else:
            #Huír horizontalmente
            if jugador_columna < self.columna and self.columna < columnas_mapa - 1:
                nueva_columna += 1
            elif jugador_columna > self.columna and self.columna > 0:
                nueva_columna -= 1
        
        #Actualizar posición
        self.fila = nueva_fila
        self.columna = nueva_columna
        return nueva_fila, nueva_columna