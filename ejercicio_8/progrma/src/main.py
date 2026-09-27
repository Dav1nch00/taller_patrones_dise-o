from domain.project import Project
from domain.task import Task
from domain.team_member import TeamMember
from patterns.adapter.email_adapter import EmailAdapter
from patterns.adapter.external_jira_api import ExternalJiraAPI
from patterns.adapter.external_slack_api import ExternalSlackAPI
from patterns.adapter.external_smtp_email_api import ExternalSmtpEmailAPI
from patterns.adapter.jira_adapter import JiraAdapter
from patterns.adapter.slack_adapter import SlackAdapter
from patterns.observer.email_notification import EmailNotification
from patterns.observer.event_observer import EventObserver
from patterns.observer.jira_sync_observer import JiraSyncObserver
from patterns.observer.slack_notification import SlackNotification
from patterns.state.task_state import InvalidStateTransitionError, TaskNotMutableError
from patterns.state.workflow import ESTADOS_CONOCIDOS, Workflow
from patterns.strategy.deadline_risk_report import DeadlineRiskReport
from patterns.strategy.detailed_tasks_report import DetailedTasksReport
from patterns.strategy.executive_summary_report import ExecutiveSummaryReport
from patterns.strategy.report_strategy import ReportStrategy
from patterns.strategy.workload_report import WorkloadReport

FLUJO_QA_ESTRICTO = {
    "ToDo": {"start": "InProgress"},
    "InProgress": {"submit_for_review": "InReview"},
    "InReview": {"approve": "Done", "reject": "InProgress"},
    "Blocked": {"unblock": "InProgress"},
    "Done": {},
}


class ConsoleAuditObserver(EventObserver):
    """Cuarto canal, escrito en este archivo y no en patterns/observer/.

    Existe para demostrar que agregar un canal es agregar una clase que
    implementa EventObserver. No se modifico Project, ni Task, ni los tres
    canales que ya existian.
    """

    canal = "auditoria"

    def update(self, event) -> dict:
        print(f"  [AUDITORIA] {event.tipo:<26} {event.mensaje}")
        return {"transport": self.canal, "registrado": True}


def montar_proyecto():
    """Cableado: APIs externas -> adaptadores -> observadores -> proyecto."""
    slack_api = ExternalSlackAPI(token="xoxb-demo-token")
    smtp_api = ExternalSmtpEmailAPI(host="mail.legacy.corp", port=587)
    jira_api = ExternalJiraAPI(base_url="https://jira.corp", project_key="PMO")

    proyecto = Project("P01", "Pasarela de pagos", "software", "Rediseño del motor de pagos.")
    proyecto.attach(EmailNotification(EmailAdapter(smtp_api), "pmo@corp.com"))
    proyecto.attach(SlackNotification(SlackAdapter(slack_api, "#pagos")))
    proyecto.attach(JiraSyncObserver(JiraAdapter(jira_api)))
    return proyecto, slack_api, smtp_api, jira_api


def cargar_tareas(proyecto):
    ana = TeamMember("TM01", "Ana Torres", "ana.torres@corp.com", "@ana", "Frontend")
    luis = TeamMember("TM02", "Luis Perez", "luis.perez@corp.com", "@luis", "Backend")
    sofia = TeamMember("TM03", "Sofia Gomez", "sofia.gomez@corp.com", "@sofia", "QA")

    proyecto.add_task(Task("T01", "Diseno del adaptador de pasarela", "Fijar la interfaz unica de cobro.",
                           prioridad=1, fecha_limite="2026-09-18", etiquetas=["pagos", "arquitectura"]))
    proyecto.add_task(Task("T02", "Migracion de historicos", "Portar 3 anos de movimientos al esquema nuevo.",
                           prioridad=2, fecha_limite="2026-10-02", etiquetas=["datos"], dependencias=["T01"]))
    proyecto.add_task(Task("T03", "Reconciliacion de cierres diarios", "Cuadre contable por dia.",
                           prioridad=2, fecha_limite="2026-09-28", etiquetas=["contabilidad"]))
    proyecto.add_task(Task("T04", "Panel de conciliacion", "Vista paraTesoreria.",
                           prioridad=3, etiquetas=["frontend"]))
    proyecto.add_task(Task("T05", "Auditoria de seguridad PCI", "Revisar manejo de datos de tarjeta.",
                           prioridad=1, fecha_limite="2026-09-24", etiquetas=["seguridad", "pagos"]))

    proyecto.asignar_tarea(proyecto.buscar_tarea("T01"), ana)
    proyecto.asignar_tarea(proyecto.buscar_tarea("T02"), luis)
    proyecto.asignar_tarea(proyecto.buscar_tarea("T03"), luis)
    proyecto.asignar_tarea(proyecto.buscar_tarea("T04"), ana)
    proyecto.asignar_tarea(proyecto.buscar_tarea("T05"), sofia)
    return ana, luis, sofia


def demo_1_ciclo_de_vida(proyecto):
    print("\n" + "=" * 78)
    print("DEMO 1  State + Observer: ciclo de vida de una tarea, evento por evento")
    print("=" * 78)
    tarea = proyecto.buscar_tarea("T01")
    print(f"\nTarea creada en {tarea.estado}\n")

    tarea.start()
    tarea.submit_for_review()
    tarea.approve()

    tarea2 = proyecto.buscar_tarea("T02")
    tarea2.start()
    tarea2.block("frozen window del proveedor de pagos")
    tarea2.unblock()
    tarea2.submit_for_review()
    tarea2.reject()
    tarea2.submit_for_review()
    tarea2.approve()

    print(f"\n{proyecto}")
    print(f"Progreso: {proyecto.progreso()}%")


def demo_2_reglas_de_negocio(proyecto):
    print("\n" + "=" * 78)
    print("DEMO 2  State: las reglas se niegan solas, sin condicionales en el dominio")
    print("=" * 78)

    print("\n[a] Bloquear una tarea que aun no empezo (regla: solo en progreso)")
    try:
        proyecto.buscar_tarea("T04").block("todavia no empezo")
    except InvalidStateTransitionError as e:
        print(f"    RECHAZADA -> {e}")

    print("\n[b] Aprobar sin pasar por revision (regla: solo en revision)")
    try:
        proyecto.buscar_tarea("T04").approve()
    except InvalidStateTransitionError as e:
        print(f"    RECHAZADA -> {e}")

    print("\n[c] Modificar una tarea completada (regla: completada es inmutable)")
    completada = proyecto.buscar_tarea("T01")
    try:
        completada.editar(prioridad=3)
    except TaskNotMutableError as e:
        print(f"    RECHAZADA -> {e}")
    try:
        completada.asignar(proyecto.buscar_tarea("T01").responsable)
    except TaskNotMutableError as e:
        print(f"    RECHAZADA -> {e}")

    print("\n[d] Reabrir una tarea completada (estado terminal)")
    try:
        completada.unblock()
    except InvalidStateTransitionError as e:
        print(f"    RECHAZADA -> {e}")


def demo_3_flujo_configurable(proyecto):
    print("\n" + "=" * 78)
    print("DEMO 3  State: el flujo es configuracion, no codigo")
    print("=" * 78)

    print("\n[a] Flujo vigente:")
    print("    " + proyecto.workflow.como_texto().replace("\n", "\n    "))

    print("\n[b] El proyecto pasa a un flujo QA estricto (sin bloqueo de tareas):")
    proyecto.configurar_flujo(Workflow("qa_estricto", dict(FLUJO_QA_ESTRICTO)))
    tarea = proyecto.buscar_tarea("T03")
    tarea.start()
    try:
        tarea.block("en QA estricto no se permite bloquear")
    except InvalidStateTransitionError as e:
        print(f"    RECHAZADA -> {e}")

    print("\n[c] La misma tarea, ahora en el flujo por defecto, si se bloquea:")
    proyecto.configurar_flujo(Workflow("estandar"))
    tarea.block("vuelve a ser permitido")
    print(f"    {tarea.estado} -> {tarea.motivo_bloqueo}")
    tarea.unblock()

    print("\n[d] Ninguna clase de TaskState se modifico en ningun momento.")


def demo_4_reportes(proyecto):
    print("\n" + "=" * 78)
    print("DEMO 4  Strategy: el mismo proyecto, cinco algoritmos distintos")
    print("=" * 78)
    estrategias = [
        ExecutiveSummaryReport(),
        WorkloadReport(),
        DeadlineRiskReport(),
        DetailedTasksReport(),
        ReportStrategyPersonalizado(),
    ]
    for estrategia in estrategias:
        print(f"\n{'-' * 78}\nEstrategia activa: {estrategia.nombre}\n{'-' * 78}")
        proyecto.set_report_strategy(estrategia)
        print(proyecto.generate_report())

    print("\n[Los cinco implementan ReportStrategy. El ultimo se escribio despues,")
    print(" fuera de patterns/strategy/, y no toco Project ni a los otros cuatro.]")


class ReportStrategyPersonalizado(ReportStrategy):
    """Quinto reporte, escrito despues y fuera de patterns/strategy/.

    Solo implementa generate. No modifica Project ni los otros cuatro algoritmos:
    eso es lo que hace que agregar un reporte sea barato.
    """

    nombre = "Tablero de estados (personalizado)"

    def generate(self, project) -> str:
        conteo = project.tareas_por_estado()
        total = max(1, len(project.tareas))
        ancho = 32
        barras = [
            f"  {estado:<12}|{'#' * int(ancho * conteo[estado] / total)}"
            for estado in ESTADOS_CONOCIDOS
        ]
        avance = int(ancho * project.progreso() / 100)
        return "\n".join(
            [
                "TABLERO DE ESTADOS (personalizado)",
                "=" * 46,
                f"Proyecto: {project.nombre} ({project.id})",
                f"Completado: [{'#' * avance}{'.' * (ancho - avance)}] {project.progreso()}%",
                "",
                *barras,
            ]
        )


def demo_5_canal_nuevo(proyecto):
    print("\n" + "=" * 78)
    print("DEMO 5  Observer: un canal mas, sin tocar nada de lo existente")
    print("=" * 78)
    auditoria = ConsoleAuditObserver()
    proyecto.attach(auditoria)
    print(f"\nObservadores suscritos: {[o.canal for o in proyecto.observers]}")
    print("\nUn solo cambio de estado:")
    proyecto.buscar_tarea("T05").start()
    print("\nSe separa el canal de auditoria:")
    proyecto.detach(auditoria)
    print(f"Observadores suscritos: {[o.canal for o in proyecto.observers]}")
    print("\nOtro cambio de estado (ya no llega a auditoria):")
    proyecto.buscar_tarea("T05").submit_for_review()


def main():
    print("=" * 78)
    print("EJERCICIO 8  Plataforma de Gestion de Proyectos")
    print("State (flujo configurable) | Observer (notificaciones) | "
          "Strategy (reportes) | Adapter (integraciones)")
    print("=" * 78)

    proyecto, slack_api, smtp_api, jira_api = montar_proyecto()

    print("\n--- Cableado: APIs externas y observadores ---")
    for observador in proyecto.observers:
        print(f"  {observador.canal:<10} {type(observador).__name__}")
    print(f"  APIs externas: {type(slack_api).__name__}, {type(smtp_api).__name__}, {type(jira_api).__name__}")

    print("\n--- Carga de tareas (cada alta y asignacion dispara los 3 canales) ---")
    cargar_tareas(proyecto)

    demo_1_ciclo_de_vida(proyecto)
    demo_2_reglas_de_negocio(proyecto)
    demo_3_flujo_configurable(proyecto)
    demo_4_reportes(proyecto)
    demo_5_canal_nuevo(proyecto)

    print("\n" + "=" * 78)
    print("Estado final")
    print("=" * 78)
    print(proyecto)
    for clave in ("T01", "T02", "T03", "T04", "T05"):
        print(f"  {proyecto.buscar_tarea(clave)}")


if __name__ == "__main__":
    main()
