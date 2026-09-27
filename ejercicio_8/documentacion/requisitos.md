# Ejercicio 8: Plataforma de Gestión de Proyectos - Requisitos

## Objetivo

Diseñar una plataforma con flujo dinámico de estados y generación flexible de reportes.

## Contexto

Una empresa tecnológica necesita:

- Gestión de tareas.
- Estados de proyecto.
- Notificaciones.
- Reportes.

## Alcance de patrones

Este ejercicio se desarrolla **únicamente con los cuatro patrones de la sección "Patrones involucrados" del enunciado**:

| Patrón | Responsabilidad |
| ------ | --------------- |
| State | Estado del proyecto (ciclo de vida de la tarea dentro del proyecto) |
| Observer | Notificaciones |
| Strategy | Reportes |
| Adapter | Integraciones externas |

Los patrones Singleton, Factory Method, Builder, Repository y Facade que aparecen
en el párrafo descriptivo del enunciado **no se implementan**, porque no están
listados en la sección de patrones involucrados. El alcance respetado es el que
gobierna el diseño.

## Requerimientos funcionales

1. **Flujo de estados configurable (State)**
   - Modelar el ciclo de vida de una tarea: `ToDo`, `InProgress`, `InReview`, `Blocked`, `Done`.
   - Cada estado es una clase que define qué acciones tienen sentido sobre la tarea.
   - Las transiciones válidas no están codificadas en los estados, sino en una tabla
     configurable (`Workflow`) asociada al proyecto. Cambiar el flujo del proyecto
     es cambiar esa tabla, sin modificar ninguna clase de estado.
   - Reglas de negocio del enunciado:
     - Solo las tareas en progreso pueden ser bloqueadas.
     - Las tareas completadas no pueden modificarse ni reasignarse.
     - Solo las tareas en revisión pueden aprobarse.

2. **Notificaciones desacopladas (Observer)**
   - Los eventos de la plataforma (tarea creada, tarea asignada, cambio de estado)
     deben notificarse automáticamente a múltiples canales.
   - Canales: correo electrónico, Slack y sincronización con una herramienta externa
     de seguimiento de tareas.
   - La lógica de negocio no debe conocer ni invocar directamente a ningún canal.

3. **Generación flexible de reportes (Strategy)**
   - Cada algoritmo de reporte es una estrategia intercambiable, seleccionable en
     tiempo de ejecución sin modificar el proyecto ni el servicio que lo consume.
     - Reporte resumen ejecutivo: totales, distribución por estado, avance.
     - Reporte detallado de tareas: una línea por tarea con responsable, prioridad,
       fecha límite, etiquetas y dependencias.
     - Reporte de carga de trabajo: tareas y estados por responsable.
     - Reporte de riesgo por fecha límite: tareas vencidas, en riesgo y sin fecha.

4. **Integración con herramientas externas (Adapter)**
   - Slack y correo se integran mediante adaptadores que envuelven APIs externas
     no modificables y las exponen bajo una interfaz uniforme.
   - La herramienta externa de seguimiento de tareas se integra mediante un segundo
     adaptador, con su propia interfaz, porque no es un canal de notificación sino
     un destino de datos.
   - El dominio y los observadores solo conocen las interfaces, nunca las APIs.

## Requerimientos no funcionales

- **Extensibilidad**: agregar un canal de notificación, un algoritmo de reporte o
  un proveedor externo no debe modificar el dominio ni los patrones ya escritos.
- **Desacoplamiento**: las clases de estado no conocen entre sí; los observadores no
  conocen al sujeto; el dominio no conoce las APIs externas.
- **Mantenibilidad**: el flujo de estados es dato (una tabla), no código, de modo
  que auditarlo no exige leer las subclases de `TaskState`.
- **Escalabilidad**: la plataforma admite nuevos tipos de proyecto con flujos
  distintos sin bifurcar la lógica de estados.

## Decisiones de diseño

El enunciado es ambiguo en dos puntos; se adoptan estas resoluciones:

1. **El State se aplica a la tarea, no al proyecto.** La narrativa dice de forma
   explícita que "las tareas atraviesan diferentes estados durante su ciclo de vida"
   y ejemplo las reglas con "solo las tareas en progreso pueden ser bloqueadas".
   El rótulo "estado del proyecto" de la tabla se interpreta como el flujo de
   estados que el proyecto impone a sus tareas, no como una máquina de estados del
   propio proyecto. El proyecto **posee** el `Workflow`, cada tarea **aplica** el
   `TaskState`.

2. **El sujeto del Observer es el `Project`.** Es el único que mantiene lista de
   observadores y expone `attach`/`detach`/`publicar`. Una tarea no tiene lista
   propia: publica en el proyecto al que pertenece. Así existe una sola
   suscripción en toda la plataforma en vez de una por tarea, que habría que
   sincronizar cada vez que se adjunta un canal.

   Los hechos viajan como un `DomainEvent` (`tipo`, `mensaje`, `origen`,
   `proyecto`) y no como texto. El `tipo` permite reaccionar sin parsear el
   mensaje, y el `origen` da la entidad real que produjo el hecho, que es lo que
   necesita el observador que sincroniza con la herramienta externa.

3. **No hay clase de servicio.** El cableado de observadores, adaptadores y
   estrategias se realiza en el punto de entrada. En el ejercicio anterior ese papel
   lo cumplía una clase de servicio que era, de hecho, un Facade; aquí se evita
   deliberadamente para no introducir un patrón fuera del alcance acordado.

## Estructura de paquetes

```
progrma/src/
├── domain/            Entidades del dominio (Project, Task, TeamMember, DomainEvent)
├── patterns/
│   ├── state/         TaskState, sus 5 estados y Workflow
│   ├── observer/      EventObserver y sus canales
│   ├── strategy/      ReportStrategy y sus algoritmos
│   └── adapter/       Interfaces uniformes y APIs externas envueltas
└── main.py            Cableado y demostraciones
```

Los tres directorios de `patterns/` son independientes entre sí: `adapter/` no
conoce el dominio, y los observadores no conocen a los reporters. Por eso un
error en el Adapter no puede manifestarse como un fallo del State.

## Errores de dominio

| Error | Se lanza cuando |
| ----- | --------------- |
| `InvalidStateTransitionError` | La acción no aplica al estado actual, o el `Workflow` no la permite |
| `TaskNotMutableError` | Se intenta editar o reasignar una tarea completada |
| `WorkflowConfigurationError` | La tabla de transiciones declara un estado o destino inexistente, o una transición implementada no coincide con la declarada |

## Preguntas de reflexión

- ¿Por qué usar State en lugar de múltiples condicionales?
- ¿Cómo hacer reportes extensibles?
- ¿Qué ventaja tiene Adapter?
- ¿Cómo afecta el diseño a la escalabilidad?
- ¿Qué patrón facilita mantenimiento futuro?
