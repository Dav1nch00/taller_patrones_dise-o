class Flight:
    def __init__(self, numero_vuelo, origen, destino, fecha_salida):
        self._numero_vuelo = numero_vuelo
        self._origen = origen
        self._destino = destino
        self._fecha_salida = fecha_salida

    @property
    def numero_vuelo(self):
        return self._numero_vuelo

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    @property
    def fecha_salida(self):
        return self._fecha_salida

    def __str__(self):
        return f"Flight(numero={self._numero_vuelo}, {self._origen} -> {self._destino})"