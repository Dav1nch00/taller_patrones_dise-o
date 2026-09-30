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
from patterns.observer.jira_sync_observer import JiraSyncObserver
from patterns.observer.slack_notification import SlackNotification
from patterns.strategy.executive_summary_report import ExecutiveSummaryReport
from patterns.strategy.workload_report import WorkloadReport


def main():
    proyecto = Project("P01", "Pasarela de pagos", "software")

    # Adapter + Observer: conectar APIs externas al proyecto.
    slack_api = ExternalSlackAPI(token="xoxb-demo-token")
    email_api = ExternalSmtpEmailAPI(host="mail.legacy.corp", port=587)
    jira_api = ExternalJiraAPI(base_url="https://jira.corp", project_key="PMO")
    proyecto.attach(SlackNotification(SlackAdapter(slack_api, "#pagos")))
    proyecto.attach(EmailNotification(EmailAdapter(email_api), "pmo@corp.com"))
    proyecto.attach(JiraSyncObserver(JiraAdapter(jira_api)))

    responsable = TeamMember("TM01", "Ana Torres", "ana@corp.com", "@ana", "Desarrollo")
    tarea = Task("T01", "Disenar adaptador de pagos", prioridad=1, etiquetas=["pagos"])
    proyecto.add_task(tarea)
    proyecto.asignar_tarea(tarea, responsable)

    # State: avanzar la tarea por el flujo permitido.
    print("\n--- Ciclo de vida ---")
    tarea.start()
    tarea.submit_for_review()
    tarea.approve()

    # Strategy: cambiar el formato del reporte sin modificar Project.
    print("\n--- Reportes ---")
    for estrategia in (ExecutiveSummaryReport(), WorkloadReport()):
        proyecto.set_report_strategy(estrategia)
        print(f"\n{estrategia.nombre}")
        print(proyecto.generate_report())

    print("\n--- Estado final ---")
    print(proyecto)
    print(tarea)


if __name__ == "__main__":
    main()
