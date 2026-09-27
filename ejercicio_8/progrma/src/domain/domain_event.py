TIPO_TAREA_CREADA = "tarea.creada"
TIPO_TAREA_ASIGNADA = "tarea.asignada"
TIPO_ESTADO_CAMBIADO = "tarea.estado_cambiado"
TIPO_FLUJO_RECONFIGURADO = "proyecto.flujo_reconfigurado"


class DomainEvent:
    """Registro inmutable de un hecho ocurrido en el dominio.

    Viaja en lugar de un string para que un observador pueda reaccionar segun
    'tipo' sin parsear el mensaje, y para que pueda leer el 'origen' (la Task o
    el Project que produjo el hecho) sin adivinarlo por el texto.
    """

    def __init__(self, tipo, mensaje, origen, proyecto):
        self._tipo = tipo
        self._mensaje = mensaje
        self._origen = origen
        self._proyecto = proyecto

    @property
    def tipo(self):
        return self._tipo

    @property
    def mensaje(self):
        return self._mensaje

    @property
    def origen(self):
        return self._origen

    @property
    def proyecto(self):
        return self._proyecto

    def __str__(self):
        return self._mensaje
