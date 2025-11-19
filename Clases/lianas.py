class Lianas:
    def init__(self):
        self.tipo = "Lianas"
        
    def permitir_cazadores(self,tipo_jugador): 
        """
        Devuelve True si el jugador es Cazador, False si es jugador \n
        O sea, devuelve True si puede pasar por este terreno. 
        """
        if tipo_jugador == "Cazador":
            return True
        return False