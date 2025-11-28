class Enemigo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.carita = "👹"
        self.color = "red"
        self.caminos_bloqueados = [] #Ptos x,y dnd solo tiene una salida posible
    
    #Funcionalidad: Decidir movimiento del enemigo según modo de juego
    def mover(self,mapa ,jugador_fila, jugador_columna, modo, filas_mapa, columnas_mapa, otros_enemigos=None):
        if modo == "escapa":
            #Perseguir al jugador
            nueva_fila, nueva_columna = self._perseguir(mapa, jugador_fila, jugador_columna, filas_mapa, columnas_mapa)
        else:
            #Huir del jugador
            nueva_fila, nueva_columna = self._huir(mapa, jugador_fila, jugador_columna, filas_mapa, columnas_mapa)
        
        #Verificar si la nueva posición está ocupada por otro enemigo
        if otros_enemigos:
            posicion_ocupada = False
            for enemigo in otros_enemigos:
                if enemigo != self and enemigo.fila == nueva_fila and enemigo.columna == nueva_columna:
                    posicion_ocupada = True
                    break
            
            #Si la posición está ocupada, mantener la posición actual
            if posicion_ocupada:
                return self.fila, self.columna
        
        #Actualizar posición si no está ocupada
        self.fila = nueva_fila
        self.columna = nueva_columna
        return self.fila, self.columna
    
    #Funcionalidad: Movimiento dirigido hacia la meta en modo cazador
    def mover_hacia_meta(self, mapa, jugador_fila, jugador_columna, meta_fila, meta_columna, filas_mapa, columnas_mapa, otros_enemigos=None):
        nueva_fila = self.fila
        nueva_columna = self.columna
        resultado = False
        nuevo_valor = 0
        
        #Decidir dirección prioritaria
        resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, True)
        if resultado:
            nueva_fila = nuevo_valor
        else: 
            resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, True)
            if resultado:
                nueva_columna = nuevo_valor
            else:
                resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, False)
                if resultado:
                    nueva_fila = nuevo_valor
                else:
                    resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, False)
                    if resultado:
                        nueva_columna = nuevo_valor
                    self.caminos_bloqueados.append((self.fila, self.columna))
        
    
        #Verificar si la nueva posición está ocupada por otro enemigo
        if otros_enemigos:
            posicion_ocupada = False
            for enemigo in otros_enemigos:
                if enemigo != self and enemigo.fila == nueva_fila and enemigo.columna == nueva_columna:
                    posicion_ocupada = True
                    break
            
            #Si la posición está ocupada, mantener la posición actual
            if posicion_ocupada:
                return self.fila, self.columna
        
        #Actualizar posición si no está ocupada
        self.fila = nueva_fila
        self.columna = nueva_columna
        return self.fila, self.columna
    
    #Funcionalidad: Movimiento de persecución hacia el jugador
    def _perseguir(self,mapa, jugador_fila, jugador_columna, filas_mapa, columnas_mapa):
        #Moverse hacia el jugador (algoritmo simple)
        nueva_fila = self.fila
        nueva_columna = self.columna
        resultado = False
        nuevo_valor = 0
        
        #Decidir dirección prioritaria
        resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, False)
        if resultado:
            nueva_fila = nuevo_valor
        else: 
            resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, False)
            if resultado:
                nueva_columna = nuevo_valor
            else:
                resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, True)
                if resultado:
                    nueva_fila = nuevo_valor
                else:
                    resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, True)
                    if resultado:
                        nueva_columna = nuevo_valor
        
        return nueva_fila, nueva_columna

    def perseguir_vertical(self, mapa, jugador_fila,filas_mapa, noprioritario):
        suma = True
        nueva_fila = self.fila
        #Moverse verticalmente
        if jugador_fila < self.fila and self.fila > 0:
            suma = False
        elif jugador_fila > self.fila and self.fila < filas_mapa - 1:
            suma = True
        
        if noprioritario:
            suma = not suma 
        
        if suma:
            nueva_fila += 1
        else:
            nueva_fila -= 1   
        try:
            posicion = mapa[nueva_fila][self.columna]
            if (nueva_fila, self.columna) in self.caminos_bloqueados:
                return False, nueva_fila
            res = self.verificar_terreno_perseguir(posicion) 
            return res , nueva_fila
        except IndexError:
            return False, nueva_fila
    
    def perseguir_horizontal(self, mapa,  jugador_columna ,columnas_mapa, noprioritario):
        suma = True
        nueva_columna = self.columna
        #Moverse horizontalmente
        if jugador_columna < self.columna and self.columna > 0:
            suma = False
        elif jugador_columna > self.columna and self.columna < columnas_mapa - 1:
            suma = True
        if noprioritario:
            suma = not suma 
        
        if suma:
            nueva_columna += 1
        else:
            nueva_columna -= 1  
        try:
            posi = mapa[self.fila][nueva_columna]
            if (self.fila, nueva_columna) in self.caminos_bloqueados:
                return False, nueva_columna
            res = self.verificar_terreno_perseguir(posi)
            return res, nueva_columna
        except IndexError:
            return False, nueva_columna
    
    #Funcionalidad: Movimiento de huida del jugador
    def _huir(self, mapa, jugador_fila, jugador_columna, filas_mapa, columnas_mapa):
        nueva_fila = self.fila
        nueva_columna = self.columna
        resultado = False
        nuevo_valor = 0
        
        #Decidir dirección prioritaria
        resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, True)
        if resultado:
            nueva_fila = nuevo_valor
        else: 
            resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, True)
            if resultado:
                nueva_columna = nuevo_valor
            else:
                resultado, nuevo_valor = self.perseguir_vertical(mapa, jugador_fila, filas_mapa, False)
                if resultado:
                    nueva_fila = nuevo_valor
                else:
                    resultado, nuevo_valor = self.perseguir_horizontal(mapa, jugador_columna, columnas_mapa, False)
                    if resultado:
                        nueva_columna = nuevo_valor
        
        return nueva_fila, nueva_columna
    
    def verificar_terreno_perseguir(self, terreno):
        """
        E: terreno dnd se va a mover y el modo en el que se encuentra \n
        S: bool, dependiendo si puede o no pasar \n
        R: - \n
        Verifica el terreno dnd se quiere mover el enemigo y si puede moverse por ahí \n
        """
        if terreno == 1 or terreno == 3:
            return True
        return False
    
    def verificar_terreno_huir(self, terreno):
        """
        E: terreno dnd se va a mover y el modo en el que se encuentra \n
        S: bool, dependiendo si puede o no pasar \n
        R: - \n
        Verifica el terreno dnd se quiere mover el enemigo y si puede moverse por ahí \n
        """
        if terreno == 1 or terreno == 2:
            return True
        return False
""""
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
        
        """