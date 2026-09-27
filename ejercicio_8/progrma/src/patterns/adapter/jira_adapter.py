from patterns.adapter.external_jira_api import ExternalJiraAPI, JiraApiError
from patterns.adapter.external_task_tracker import ExternalTaskTracker


class JiraAdapter(ExternalTaskTracker):
    """Traduce una Task del dominio a los cuatro campos planos de Jira.

    No importa Task: lee por duck typing para que el adaptador no dependa del
    dominio. Los ocho atributos de la tarea se aplanan en la descripcion, que es
    el unico campo de texto libre que la API acepta.
    """

    def __init__(self, api, project_key=None):
        self._api = api
        self._project_key = project_key or api.default_project_key()
        self._issues = {}

    @property
    def project_key(self):
        return self._project_key

    def publish_task(self, task) -> dict:
        """Crea el issue la primera vez y lo actualiza en los siguientes eventos.

        El remember de la clave es del adaptador, no del observador: el tracker
        es quien sabe si la tarea ya existe del lado de Jira.
        """
        try:
            if task.id in self._issues:
                clave = self._issues[task.id]
                respuesta = self._api.update_issue(
                    clave, {"description": self._armar_descripcion(task)}
                )
                accion = "actualizado"
            else:
                respuesta = self._api.create_issue(
                    self._project_key, "Task", task.titulo, self._armar_descripcion(task)
                )
                self._issues[task.id] = respuesta["key"]
                accion = "creado"
        except JiraApiError as error:
            raise RuntimeError(f"Jira rechazo el issue: {error}") from error
        return {
            "transport": "jira",
            "clave": respuesta["key"],
            "referencia": respuesta["self"],
            "accion": accion,
            "respuesta_externa": respuesta,
        }

    def _armar_descripcion(self, task):
        quien = task.responsable.nombre if task.responsable else "sin asignar"
        etiquetas = ", ".join(task.etiquetas) or "sin etiquetas"
        dependencias = ", ".join(task.dependencias) or "sin dependencias"
        fecha = task.fecha_limite or "sin fecha limite"
        return "\n".join(
            [
                f"Id interno: {task.id}",
                f"Estado en la plataforma: {task.estado}",
                f"Prioridad: {task.prioridad}",
                f"Responsable: {quien}",
                f"Fecha limite: {fecha}",
                f"Etiquetas: {etiquetas}",
                f"Dependencias: {dependencias}",
                "",
                str(task.descripcion),
            ]
        )
