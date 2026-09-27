from abc import ABC, abstractmethod


class ReportStrategy(ABC):
    """Algoritmo intercambiable de generacion de reportes.

    La interfaz es deliberadamente minima: recibe el proyecto completo y decide
    que datos leer y como presentarlos. No hay metodo plantilla en la base, cada
    algoritmo arma su propio texto, para no meter un patron mas en el alcance.
    """

    nombre = "Reporte"

    @abstractmethod
    def generate(self, project) -> str:
        pass
