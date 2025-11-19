class Camino:
    def __init__(self):
        self.tipo = "Camino"
        
    def permitir_todos(self): #Esta f tal vez sobre. Pero mejor ponerla por si acaso
        """
        * Todos pueden pasar. Por ende, true
        """
        return True
print(Camino().permitir_todos())