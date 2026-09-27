from patterns.state.task_state import InvalidStateTransitionError

TRANSICIONES_POR_DEFECTO = {
    "ToDo": {"start": "InProgress"},
    "InProgress": {"submit_for_review": "InReview", "block": "Blocked"},
    "InReview": {"approve": "Done", "reject": "InProgress"},
    "Blocked": {"unblock": "InProgress"},
    "Done": {},
}

ESTADOS_CONOCIDOS = ("ToDo", "InProgress", "InReview", "Blocked", "Done")


class WorkflowConfigurationError(Exception):
    pass


class Workflow:
    """Tabla de transiciones que hace configurable el flujo de estados.

    Las clases de State responden QUE accion existe conceptualmente en cada
    estado; este objeto responde SI la transicion esta permitida y hacia DONDE
    va. Cambiar el proceso de un proyecto es cambiar esta tabla, sin tocar
    ninguna subclase de TaskState.
    """

    def __init__(self, nombre, transiciones=None):
        self._nombre = nombre
        self._transiciones = {
            estado: dict(acciones)
            for estado, acciones in (transiciones or TRANSICIONES_POR_DEFECTO).items()
        }
        self._validar()

    @property
    def nombre(self):
        return self._nombre

    def transiciones_de(self, estado):
        return dict(self._transiciones.get(estado, {}))

    def permite(self, estado, accion):
        return accion in self._transiciones.get(estado, {})

    def destino(self, estado, accion):
        if not self.permite(estado, accion):
            raise InvalidStateTransitionError(
                f"El flujo '{self._nombre}' no permite la accion '{accion}' desde el estado {estado}."
            )
        return self._transiciones[estado][accion]

    def error_de_configuracion(self, estado, accion, esperado, solicitado):
        return WorkflowConfigurationError(
            f"El flujo '{self._nombre}' declara '{estado} --{accion}--> {esperado}', "
            f"pero la transicion implementada apunta a {solicitado}."
        )

    def como_texto(self):
        lineas = [f"Flujo '{self._nombre}'"]
        for estado in ESTADOS_CONOCIDOS:
            detalle = self._texto_de(estado)
            lineas.append(f"  {estado}: {detalle}")
        return "\n".join(lineas)

    def _texto_de(self, estado):
        acciones = self._transiciones.get(estado, {})
        if not acciones:
            return "(estado terminal)"
        return ", ".join(f"{accion} -> {destino}" for accion, destino in acciones.items())

    def _validar(self):
        for estado, acciones in self._transiciones.items():
            if estado not in ESTADOS_CONOCIDOS:
                raise WorkflowConfigurationError(
                    f"Estado desconocido en el flujo '{self._nombre}': {estado}."
                )
            for accion, destino in acciones.items():
                if destino not in ESTADOS_CONOCIDOS:
                    raise WorkflowConfigurationError(
                        f"Destino desconocido en el flujo '{self._nombre}': "
                        f"{estado} --{accion}--> {destino}."
                    )
