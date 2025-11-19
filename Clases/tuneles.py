class Tuneles:
    def __init__(self):
        self.tipo = "Tuneles"
    
    def permitir_jugadores(self,tipo_jugador):
        """
        Devuelve True si el jugador es Jugador, False si es Cazador \n
        O sea, devuelve True si puede pasar por este terreno.
        """
        if tipo_jugador == "Jugador":
            return True
        return False