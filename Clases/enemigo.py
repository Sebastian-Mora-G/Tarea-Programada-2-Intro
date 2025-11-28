import random
import heapq

class Enemigo:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.carita = "👹"
        self.color = "red"
        self.ultima_posicion = (fila, columna)
        self.contador_ciclos = 0
        self.camino_actual = []
        self.objetivo_actual = None
    
    #E:mapa,jugador_fila,jugador_columna,modo,filas_mapa,columnas_mapa,otros_enemigos
    #S:nueva posición del enemigo
    #R:Ninguna
    #Funcionalidad:Mover enemigo usando búsqueda de caminos
    def mover(self, mapa, jugador_fila, jugador_columna, modo, filas_mapa, columnas_mapa, otros_enemigos=None):
        objetivo_fila, objetivo_columna = jugador_fila, jugador_columna
        
        if modo == "cazador":
            #En modo cazador, el objetivo es la meta (esquina inferior derecha)
            objetivo_fila, objetivo_columna = filas_mapa-1, columnas_mapa-1
        
        #Si no tenemos camino o el objetivo cambió, calcular nuevo camino
        if (not self.camino_actual or 
            self.objetivo_actual != (objetivo_fila, objetivo_columna) or
            len(self.camino_actual) <= 1):
            
            self.camino_actual = self._encontrar_camino(mapa, self.fila, self.columna, 
                                                      objetivo_fila, objetivo_columna, 
                                                      filas_mapa, columnas_mapa, modo)
            self.objetivo_actual = (objetivo_fila, objetivo_columna)
        
        #Si tenemos un camino, movernos al siguiente paso
        if len(self.camino_actual) > 1:
            siguiente_paso = self.camino_actual[1]
            nueva_fila, nueva_columna = siguiente_paso
            
            #Verificar si la posición está ocupada
            if not self._posicion_ocupada(nueva_fila, nueva_columna, otros_enemigos or []):
                self.fila, self.columna = nueva_fila, nueva_columna
                self.camino_actual.pop(0)
            else:
                #Si está ocupada, recalcular camino
                self.camino_actual = []
        else:
            #Si no hay camino válido, movimiento aleatorio
            self.camino_actual = []
            nueva_fila, nueva_columna = self._movimiento_aleatorio_valido(mapa, filas_mapa, columnas_mapa, modo)
            self.fila, self.columna = nueva_fila, nueva_columna
        
        return self.fila, self.columna
    
    #E:mapa,fila_inicio,columna_inicio,fila_objetivo,columna_objetivo,filas_mapa,columnas_mapa,modo
    #S:lista de posiciones que forman el camino
    #R:Ninguna
    #Funcionalidad:Encontrar camino usando algoritmo A*
    def _encontrar_camino(self, mapa, fila_inicio, columna_inicio, fila_objetivo, columna_objetivo, filas_mapa, columnas_mapa, modo):
        open_set = []
        heapq.heappush(open_set, (0, fila_inicio, columna_inicio))
        
        came_from = {}
        g_score = {(fila_inicio, columna_inicio): 0}
        f_score = {(fila_inicio, columna_inicio): self._heuristic(fila_inicio, columna_inicio, fila_objetivo, columna_objetivo)}
        
        while open_set:
            _, actual_fila, actual_columna = heapq.heappop(open_set)
            
            if actual_fila == fila_objetivo and actual_columna == columna_objetivo:
                return self._reconstruir_camino(came_from, (actual_fila, actual_columna))
            
            for vecino in self._obtener_vecinos_validos(mapa, actual_fila, actual_columna, filas_mapa, columnas_mapa, modo):
                vecino_fila, vecino_columna = vecino
                
                tentative_g_score = g_score[(actual_fila, actual_columna)] + 1
                
                if vecino not in g_score or tentative_g_score < g_score[vecino]:
                    came_from[vecino] = (actual_fila, actual_columna)
                    g_score[vecino] = tentative_g_score
                    f_score[vecino] = tentative_g_score + self._heuristic(vecino_fila, vecino_columna, fila_objetivo, columna_objetivo)
                    heapq.heappush(open_set, (f_score[vecino], vecino_fila, vecino_columna))
        
        return []
    
    #E:fila_actual,columna_actual,fila_objetivo,columna_objetivo
    #S:valor heurístico (distancia Manhattan)
    #R:Ninguna
    #Funcionalidad:Calcular heurística para A*
    def _heuristic(self, fila_actual, columna_actual, fila_objetivo, columna_objetivo):
        return abs(fila_actual - fila_objetivo) + abs(columna_actual - columna_objetivo)
    
    #E:mapa,fila_actual,columna_actual,filas_mapa,columnas_mapa,modo
    #S:lista de vecinos válidos
    #R:Ninguna
    #Funcionalidad:Obtener vecinos a los que se puede mover
    def _obtener_vecinos_validos(self, mapa, fila_actual, columna_actual, filas_mapa, columnas_mapa, modo):
        vecinos = []
        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        
        for dx, dy in direcciones:
            nueva_fila = fila_actual + dx
            nueva_columna = columna_actual + dy
            
            if (0 <= nueva_fila < filas_mapa and 0 <= nueva_columna < columnas_mapa):
                terreno = mapa[nueva_fila][nueva_columna]
                
                if modo == "escapa":
                    if self.verificar_terreno_perseguir(terreno):
                        vecinos.append((nueva_fila, nueva_columna))
                else:
                    if self.verificar_terreno_perseguir(terreno):
                        vecinos.append((nueva_fila, nueva_columna))
        
        return vecinos
    
    #E:came_from,posicion_actual
    #S:camino reconstruido
    #R:Ninguna
    #Funcionalidad:Reconstruir camino desde el objetivo al inicio
    def _reconstruir_camino(self, came_from, actual):
        camino_total = [actual]
        while actual in came_from:
            actual = came_from[actual]
            camino_total.append(actual)
        camino_total.reverse()
        return camino_total
    
    #E:nueva_fila,nueva_columna,otros_enemigos
    #S:booleano indicando si posición está ocupada
    #R:Ninguna
    #Funcionalidad:Verificar si posición está ocupada por otro enemigo
    def _posicion_ocupada(self, nueva_fila, nueva_columna, otros_enemigos):
        for enemigo in otros_enemigos:
            if enemigo != self and enemigo.fila == nueva_fila and enemigo.columna == nueva_columna:
                return True
        return False
    
    #E:mapa,filas_mapa,columnas_mapa,modo
    #S:nueva posición válida aleatoria
    #R:Ninguna
    #Funcionalidad:Movimiento aleatorio cuando no hay camino
    def _movimiento_aleatorio_valido(self, mapa, filas_mapa, columnas_mapa, modo):
        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(direcciones)
        
        for dx, dy in direcciones:
            nf = self.fila + dx
            nc = self.columna + dy
            if (0 <= nf < filas_mapa and 0 <= nc < columnas_mapa):
                terreno = mapa[nf][nc]
                if modo == "escapa" and self.verificar_terreno_perseguir(terreno):
                    return nf, nc
                elif modo == "cazador" and self.verificar_terreno_perseguir(terreno):
                    return nf, nc
        
        return self.fila, self.columna
    
    #E:terreno
    #S:booleano indicando si puede pasar
    #R:Ninguna
    #Funcionalidad:Verificar terreno válido para persecución
    def verificar_terreno_perseguir(self, terreno):
        if terreno == 1 or terreno == 3:
            return True
        return False
    
    #E:terreno
    #S:booleano indicando si puede pasar
    #R:Ninguna
    #Funcionalidad:Verificar terreno válido para huida
    def verificar_terreno_huir(self, terreno):
        if terreno == 1 or terreno == 2:
            return True
        return False