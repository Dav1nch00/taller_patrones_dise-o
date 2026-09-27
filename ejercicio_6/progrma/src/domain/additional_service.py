class AdditionalService:
    def __init__(self, nombre, costo):
        self._nombre = nombre
        self._costo = float(costo)

    @property
    def nombre(self):
        return self._nombre

    @property
    def costo(self):
        return self._costo

    def __str__(self):
        return f"AdditionalService(nombre={self._nombre}, costo={self._costo})"