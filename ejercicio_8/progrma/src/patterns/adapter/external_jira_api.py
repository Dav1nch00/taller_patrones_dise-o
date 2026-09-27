class JiraApiError(Exception):
    pass


class ExternalJiraAPI:
    """API de un tercero. No se modifica: se envuelve con un adaptador.

    Simula heterogeneidad real: no acepta una entidad de negocio sino cuatro
    campos planos, exige el project_key aunque la API ya tenga uno por defecto,
    y lanza excepcion cuando el resumen excede el limite del campo.
    """

    LIMITE_RESUMEN = 255

    def __init__(self, base_url, project_key="PMO", api_token=None):
        self._base_url = base_url
        self._project_key = project_key
        self._api_token = api_token
        self._secuencia = 0
        self._issues = {}

    def default_project_key(self):
        return self._project_key

    def create_issue(self, project_key, issue_type, summary, description):
        if len(summary) > self.LIMITE_RESUMEN:
            raise JiraApiError(
                f"El resumen supera los {self.LIMITE_RESUMEN} caracteres del campo summary."
            )
        if not description.strip():
            raise JiraApiError("La descripcion no puede ir vacia.")
        self._secuencia += 1
        issue_id = str(9000 + self._secuencia)
        clave = f"{project_key}-{100 + self._secuencia}"
        self._issues[clave] = issue_id
        return {
            "id": issue_id,
            "key": clave,
            "self": f"{self._base_url}/rest/api/3/issue/{issue_id}",
            "fields": {"summary": summary, "issuetype": {"name": issue_type}},
        }

    def update_issue(self, issue_key, fields):
        if issue_key not in self._issues:
            raise JiraApiError(f"El issue {issue_key} no existe en este proyecto.")
        issue_id = self._issues[issue_key]
        return {
            "id": issue_id,
            "key": issue_key,
            "self": f"{self._base_url}/rest/api/3/issue/{issue_id}",
            "updated": True,
            "fields": fields,
        }
