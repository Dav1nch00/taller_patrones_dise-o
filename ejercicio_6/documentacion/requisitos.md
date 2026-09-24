# Ejercicio 6: Sistema de Reservas para Aerolínea - Requisitos

## Objetivo

Diseñar un sistema que gestione reservas complejas con cambios dinámicos de estado y cálculo flexible de precios.

## Contexto

El sistema debe manejar:

- Reservas
- Asientos
- Pagos
- Cancelaciones

## Requerimientos funcionales

1. **Construcción de reservas complejas (Builder)**
   - Ensamblar una reserva paso a paso con: pasajero, vuelo, precio base, servicios adicionales y preferencias específicas.
   - Evitar constructores telescópicos.
   - Garantizar que el objeto `Reservation` sea consistente antes de ser utilizado.

2. **Cálculo dinámico de tarifas (Strategy)**
   - Calcular el precio según el tipo de clase: económica, premium, primera clase.
   - Considerar temporada del año y anticipación de la compra.
   - Seleccionar la estrategia de precio en tiempo de ejecución sin modificar la lógica central de la reserva.

3. **Ciclo de vida de la reserva (State)**
   - Modelar los estados: pendiente, confirmada, cancelada, check-in realizado, abordada.
   - Reglas de negocio:
     - Solo se pueden modificar reservas en estado pendiente.
     - Las reservas canceladas no generan cargos adicionales.
   - Cambiar el comportamiento de la reserva cuando su estado interno cambia.

4. **Notificaciones (Observer)**
   - Notificar a pasajeros y agentes de viaje ante cambios de estado: confirmación, cancelación, cambios de horario.
   - Canales: Email, SMS, App (móvil).
   - Desacoplar la lógica de la reserva de los mecanismos de notificación.

5. **Upgrades**
   - Permitir upgrades de reservas (cambio de clase / tarifa) dentro de las reglas de estado.

## Requerimientos no funcionales

- **Extensibilidad**: incorporar nuevos tipos de tarifas, estados adicionales (overbooking, lista de espera) y canales de notificación emergentes sin afectar la estabilidad del núcleo.
- **Mantenibilidad**: arquitectura cohesiva, objetos controlados por el builder, respuesta dinámica a cambios de contexto.
- **Escalabilidad**: soportar crecimiento de funcionalidad sin modificar el núcleo del sistema.
- **Disponibilidad y confiabilidad**: propios de sistemas de reservas aerocomerciales.

## Patrones involucrados

| Patrón | Responsabilidad |
| ------ | --------------- |
| Builder | Construcción de reservas complejas (`ReservationBuilder`) |
| Strategy | Cálculo de precio de tarifas (`EconomyPricing`, `PremiumPricing`) |
| State | Ciclo de vida de la reserva (`PendingState`, `ConfirmedState`, `CancelledState`) |
| Observer | Notificación de cambios de estado (`EmailNotifier`, `SMSNotifier`, `AppNotifier`) |

## Preguntas de reflexión

- ¿Qué problemas genera usar múltiples condicionales para estados?
- ¿Cómo facilita Builder la creación de reservas complejas?
- ¿Qué ocurre si cambian las reglas de precio?
- ¿Cómo desacoplar notificaciones?
- ¿Qué patrón mejora cohesión en cambios de estado?