class Trampas:
    #E:Ninguna
    #S:Inicializa sistema de trampas con listas vacías
    #R:Ninguna
    #Funcionalidad:Constructor que prepara el sistema de trampas
    def __init__(self):
        self.trampas_activas = []  #Lista de (fila, columna, tiempo_colocacion)
        self.max_trampas = 3
        self.cooldown = 5  #segundos por trampa individual
        self.trampas_eliminadas = []  #Para controlar reaparición
    
    #E:fila(int), columna(int), tiempo_actual(float)
    #S:booleano indicando si se pudo colocar trampa
    #R:Posición debe ser válida y no exceder máximo de trampas
    #Funcionalidad:Colocar una nueva trampa en posición específica
    def colocar_trampa(self, fila, columna, tiempo_actual):
        #Verificar si hay slots disponibles (trampas que ya cumplieron cooldown)
        trampas_disponibles = self.obtener_trampas_disponibles(tiempo_actual)
        
        if trampas_disponibles <= 0:
            return False  #No hay trampas disponibles
        
        #Verificar que no haya trampa en esa posición
        for f, c, t in self.trampas_activas:
            if f == fila and c == columna:
                return False
        
        #Si hay menos de 3 trampas activas, agregar nueva
        if len(self.trampas_activas) < self.max_trampas:
            self.trampas_activas.append((fila, columna, tiempo_actual))
            return True
        else:
            #Reemplazar la trampa más antigua que ya cumplió cooldown
            for i, (f, c, t) in enumerate(self.trampas_activas):
                if tiempo_actual - t >= self.cooldown:
                    self.trampas_activas[i] = (fila, columna, tiempo_actual)
                    return True
        
        return False
    
    #E:fila(int), columna(int)
    #S:booleano indicando si hay trampa en posición
    #R:Ninguna
    #Funcionalidad:Verificar si hay trampa en posición específica
    def hay_trampa(self, fila, columna):
        for f, c, t in self.trampas_activas:
            if f == fila and c == columna:
                return True
        return False
    
    #E:fila(int), columna(int), tiempo_actual(float)
    #S:booleano indicando si se eliminó trampa
    #R:Ninguna
    #Funcionalidad:Eliminar trampa específica y registrar eliminación
    def eliminar_trampa(self, fila, columna, tiempo_actual):
        for i, (f, c, t) in enumerate(self.trampas_activas):
            if f == fila and c == columna:
                self.trampas_activas.pop(i)
                self.trampas_eliminadas.append((fila, columna, tiempo_actual))
                return True
        return False
    
    #E:tiempo_actual(float)
    #S:número de trampas disponibles para usar
    #R:Ninguna
    #Funcionalidad:Obtener cantidad de trampas que pueden colocarse
    def obtener_trampas_disponibles(self, tiempo_actual):
        if len(self.trampas_activas) < self.max_trampas:
            return self.max_trampas - len(self.trampas_activas)
        
        #Contar cuántas trampas han cumplido cooldown
        disponibles = 0
        for f, c, t in self.trampas_activas:
            if tiempo_actual - t >= self.cooldown:
                disponibles += 1
        
        return disponibles
    
    #E:tiempo_actual(float)
    #S:lista de posiciones de enemigos para reaparecer
    #R:Ninguna
    #Funcionalidad:Obtener enemigos eliminados que deben reaparecer
    def obtener_enemigos_para_reaparecer(self, tiempo_actual):
        reaparecer = []
        nuevos_eliminados = []
        
        for fila, columna, tiempo in self.trampas_eliminadas:
            if tiempo_actual - tiempo >= 10:  #10 segundos para reaparecer
                reaparecer.append((fila, columna))
            else:
                nuevos_eliminados.append((fila, columna, tiempo))
        
        self.trampas_eliminadas = nuevos_eliminados
        return reaparecer
    
    #E:Ninguna
    #S:Reinicia todas las trampas a estado inicial
    #R:Ninguna
    #Funcionalidad:Limpiar todas las trampas al cambiar de modo
    def reiniciar_trampas(self):
        self.trampas_activas = []
        self.trampas_eliminadas = []