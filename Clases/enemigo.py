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
        self.historial_posiciones = []  #Para detectar ciclos
        self.contador_atascado = 0
    
    #E:mapa,jugador_fila,jugador_columna,modo,filas_mapa,columnas_mapa,otros_enemigos
    #S:nueva posición del enemigo
    #R:Ninguna
    #Funcionalidad:Mover enemigo usando búsqueda de caminos inteligente
    def mover(self, mapa, jugador_fila, jugador_columna, modo, filas_mapa, columnas_mapa, otros_enemigos=None):
        #Determinar objetivo según modo
        if modo == "cazador":
            #En modo cazador, elegir entre dos metas forma inteligente
            objetivo_fila, objetivo_columna = self._elegir_meta_inteligente(filas_mapa, columnas_mapa)
        else:
            #En modo escapa, perseguir jugador
            objetivo_fila, objetivo_columna = jugador_fila, jugador_columna
        
        #Detectar si está atascado en ciclo
        if self._detectar_ciclo():
            self.contador_atascado += 1
            #Si está muy atascado, usar movimiento alternativo
            if self.contador_atascado > 3:
                return self._movimiento_emergencia(mapa, objetivo_fila, objetivo_columna, filas_mapa, columnas_mapa, otros_enemigos or [])
        else:
            self.contador_atascado = 0
        
        #Si no tenemos camino o objetivo cambió, calcular nuevo camino
        if (not self.camino_actual or 
            self.objetivo_actual != (objetivo_fila, objetivo_columna) or
            len(self.camino_actual) <= 1):
            
            self.camino_actual = self._encontrar_camino(mapa, self.fila, self.columna, 
                                                      objetivo_fila, objetivo_columna, 
                                                      filas_mapa, columnas_mapa, modo)
            self.objetivo_actual = (objetivo_fila, objetivo_columna)
        
        #Si tenemos camino, movernos al siguiente paso
        if len(self.camino_actual) > 1:
            siguiente_paso = self.camino_actual[1]
            nueva_fila, nueva_columna = siguiente_paso
            
            #Verificar si posición está ocupada
            if not self._posicion_ocupada(nueva_fila, nueva_columna, otros_enemigos or []):
                self.fila, self.columna = nueva_fila, nueva_columna
                self.camino_actual.pop(0)
                self._actualizar_historial()
            else:
                #Si está ocupada, recalcular camino
                self.camino_actual = []
        else:
            #Si no hay camino válido, movimiento aleatorio inteligente
            self.camino_actual = []
            self._movimiento_aleatorio_inteligente(mapa, objetivo_fila, objetivo_columna, filas_mapa, columnas_mapa, otros_enemigos or [])
            self._actualizar_historial()
        
        return self.fila, self.columna
    
    #E:filas_mapa,columnas_mapa
    #S:meta elegida (fila,columna)
    #R:Ninguna
    #Funcionalidad:Elegir meta más cercana forma inteligente
    def _elegir_meta_inteligente(self, filas_mapa, columnas_mapa):
        meta_izquierda = (filas_mapa-1, 0)
        meta_derecha = (filas_mapa-1, columnas_mapa-1)
        
        #Calcular distancia a cada meta
        dist_izquierda = abs(self.fila - meta_izquierda[0]) + abs(self.columna - meta_izquierda[1])
        dist_derecha = abs(self.fila - meta_derecha[0]) + abs(self.columna - meta_derecha[1])
        
        #Elegir meta más cercana
        if dist_izquierda < dist_derecha:
            return meta_izquierda
        elif dist_derecha < dist_izquierda:
            return meta_derecha
        else:
            #Si equidistan, elegir aleatoriamente
            return random.choice([meta_izquierda, meta_derecha])
    
    #E:Ninguna
    #S:booleano indicando si está en ciclo
    #R:Ninguna
    #Funcionalidad:Detectar si enemigo está atrapado en ciclo
    def _detectar_ciclo(self):
        if len(self.historial_posiciones) < 6:
            return False
        
        #Verificar si hay pocas posiciones únicas en historial reciente
        ultimas_posiciones = self.historial_posiciones[-6:]
        posiciones_unicas = len(set(ultimas_posiciones))
        
        #Si hay 3 o menos posiciones únicas en 6 movimientos, probable ciclo
        return posiciones_unicas <= 3
    
    #E:Ninguna
    #S:Actualiza historial de posiciones
    #R:Ninguna
    #Funcionalidad:Mantener registro de posiciones recientes
    def _actualizar_historial(self):
        self.historial_posiciones.append((self.fila, self.columna))
        if len(self.historial_posiciones) > 8:
            self.historial_posiciones.pop(0)
    
    #E:mapa,objetivo_fila,objetivo_columna,filas_mapa,columnas_mapa,otros_enemigos
    #S:Modifica posición del enemigo
    #R:Ninguna
    #Funcionalidad:Movimiento emergencia cuando está atascado
    def _movimiento_emergencia(self, mapa, objetivo_fila, objetivo_columna, filas_mapa, columnas_mapa, otros_enemigos):
        #Primero intentar movimientos que acerquen al objetivo
        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        
        #Ordenar direcciones por proximidad al objetivo
        direcciones_ordenadas = []
        for dx, dy in direcciones:
            nf = self.fila + dx
            nc = self.columna + dy
            
            if (0 <= nf < filas_mapa and 0 <= nc < columnas_mapa and
                self._es_movimiento_valido(mapa, nf, nc)):
                
                distancia = abs(nf - objetivo_fila) + abs(nc - objetivo_columna)
                direcciones_ordenadas.append((distancia, nf, nc, dx, dy))
        
        #Probar direcciones ordenadas por proximidad
        if direcciones_ordenadas:
            direcciones_ordenadas.sort(key=lambda x: x[0])
            for distancia, nf, nc, dx, dy in direcciones_ordenadas:
                if not self._posicion_ocupada(nf, nc, otros_enemigos):
                    self.fila, self.columna = nf, nc
                    self.historial_posiciones = []
                    self.contador_atascado = 0
                    return
        
        #Si no pudo moverse sin colisiones, forzar movimiento
        for dx, dy in direcciones:
            nf = self.fila + dx
            nc = self.columna + dy
            
            if (0 <= nf < filas_mapa and 0 <= nc < columnas_mapa and
                self._es_movimiento_valido(mapa, nf, nc)):
                
                self.fila, self.columna = nf, nc
                self.historial_posiciones = []
                self.contador_atascado = 0
                return
    
    #E:mapa,objetivo_fila,objetivo_columna,filas_mapa,columnas_mapa,otros_enemigos
    #S:Modifica posición del enemigo
    #R:Ninguna
    #Funcionalidad:Movimiento aleatorio que prioriza acercarse al objetivo
    def _movimiento_aleatorio_inteligente(self, mapa, objetivo_fila, objetivo_columna, filas_mapa, columnas_mapa, otros_enemigos):
        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        
        #Ordenar direcciones por qué tan cerca quedamos del objetivo
        direcciones_ordenadas = []
        for dx, dy in direcciones:
            nf = self.fila + dx
            nc = self.columna + dy
            
            if (0 <= nf < filas_mapa and 0 <= nc < columnas_mapa and
                self._es_movimiento_valido(mapa, nf, nc) and
                not self._posicion_ocupada(nf, nc, otros_enemigos)):
                
                distancia = abs(nf - objetivo_fila) + abs(nc - objetivo_columna)
                direcciones_ordenadas.append((distancia, nf, nc))
        
        #Elegir dirección que más acerca al objetivo
        if direcciones_ordenadas:
            direcciones_ordenadas.sort(key=lambda x: x[0])
            self.fila, self.columna = direcciones_ordenadas[0][1], direcciones_ordenadas[0][2]
        else:
            #Si no hay movimientos válidos, intentar cualquier movimiento
            for dx, dy in direcciones:
                nf = self.fila + dx
                nc = self.columna + dy
                if (0 <= nf < filas_mapa and 0 <= nc < columnas_mapa and
                    self._es_movimiento_valido(mapa, nf, nc)):
                    self.fila, self.columna = nf, nc
                    break
    
    #E:mapa,fila,columna
    #S:booleano indicando si movimiento es válido
    #R:Ninguna
    #Funcionalidad:Verificar si movimiento es válido
    def _es_movimiento_valido(self, mapa, fila, columna):
        if not (0 <= fila < len(mapa) and 0 <= columna < len(mapa[0])):
            return False
        terreno = mapa[fila][columna]
        return terreno == 1 or terreno == 3  #Camino o Lianas
    
    #E:mapa,fila_inicio,columna_inicio,fila_objetivo,columna_objetivo,filas_mapa,columnas_mapa,modo
    #S:lista de posiciones que forman camino
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
                if self._es_movimiento_valido(mapa, nueva_fila, nueva_columna):
                    vecinos.append((nueva_fila, nueva_columna))
        
        return vecinos
    
    #E:came_from,posicion_actual
    #S:camino reconstruido
    #R:Ninguna
    #Funcionalidad:Reconstruir camino desde objetivo al inicio
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