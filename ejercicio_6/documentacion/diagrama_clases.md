# Ejercicio 6: Sistema de Reservas para Aerolínea - Diagrama de Clases

## Diagrama (Mermaid)

```mermaid
classDiagram
    direction LR

    class Passenger {
        +String id
        +String nombre
        +String email
        +String telefono
        +getNombre() String
    }

    class Flight {
        +String numeroVuelo
        +String origen
        +String destino
        +DateTime fechaSalida
        +getNumeroVuelo() String
    }

    class AdditionalService {
        +String nombre
        +double costo
        +getCosto() double
    }

    class Reservation {
        -Passenger passenger
        -Flight flight
        -double basePrice
        -List~AdditionalService~ services
        -Map~String, String~ preferences
        -ReservationState state
        -PricingStrategy pricingStrategy
        -List~NotificationObserver~ observers
        +attach(NotificationObserver) void
        +detach(NotificationObserver) void
        +notifyObservers(String event) void
        +changeState(ReservationState) void
        +calculatePrice() double
        +modify() void
        +confirm() void
        +cancel() void
        +checkIn() void
        +board() void
        +upgrade(PricingStrategy) void
    }

    class ReservationBuilder {
        -Passenger passenger
        -Flight flight
        -double basePrice
        -List~AdditionalService~ services
        -Map~String, String~ preferences
        +setPassenger(Passenger) ReservationBuilder
        +setFlight(Flight) ReservationBuilder
        +setBasePrice(double) ReservationBuilder
        +addService(AdditionalService) ReservationBuilder
        +setPreference(String, String) ReservationBuilder
        +setPricingStrategy(PricingStrategy) ReservationBuilder
        +build() Reservation
    }

    class PricingStrategy {
        <<interface>>
        +calculatePrice(basePrice double, season String, anticipation int) double
    }

    class EconomyPricing {
        +calculatePrice(double, String, int) double
    }

    class PremiumPricing {
        +calculatePrice(double, String, int) double
    }

    class ReservationState {
        <<interface>>
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class PendingState {
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class ConfirmedState {
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class CancelledState {
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class CheckInState {
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class BoardedState {
        +modify(Reservation) void
        +confirm(Reservation) void
        +cancel(Reservation) void
        +checkIn(Reservation) void
        +board(Reservation) void
    }

    class NotificationObserver {
        <<interface>>
        +update(String event, Reservation reservation) void
    }

    class EmailNotifier {
        +update(String, Reservation) void
    }

    class SMSNotifier {
        +update(String, Reservation) void
    }

    class AppNotifier {
        +update(String, Reservation) void
    }

    ReservationBuilder ..> Reservation : crea (build)
    Reservation o-- Passenger : pasajero
    Reservation o-- Flight : vuelo
    Reservation o-- AdditionalService : servicios
    Reservation o-- ReservationState : estado actual
    Reservation o-- PricingStrategy : estrategia
    Reservation o-- NotificationObserver : observadores
    PricingStrategy <|.. EconomyPricing
    PricingStrategy <|.. PremiumPricing
    ReservationState <|.. PendingState
    ReservationState <|.. ConfirmedState
    ReservationState <|.. CancelledState
    ReservationState <|.. CheckInState
    ReservationState <|.. BoardedState
    NotificationObserver <|.. EmailNotifier
    NotificationObserver <|.. SMSNotifier
    NotificationObserver <|.. AppNotifier
```

## Descripción de los patrones en el diagrama

- **Builder**: `ReservationBuilder` permite ensamblar `Reservation` paso a paso mediante métodos fluidos (`setPassenger`, `setFlight`, `addService`, `setPreference`, `build`), evitando constructores telescópicos.
- **Strategy**: `Reservation` delega el cálculo del precio en una `PricingStrategy` intercambiable (`EconomyPricing`, `PremiumPricing`), seleccionable en tiempo de ejecución.
- **State**: `Reservation` delega su comportamiento en un `ReservationState` (`PendingState`, `ConfirmedState`, `CancelledState`, `CheckInState`, `BoardedState`). Cada estado define qué transiciones son válidas.
- **Observer**: `Reservation` mantiene una lista de `NotificationObserver` (`EmailNotifier`, `SMSNotifier`, `AppNotifier`) y los notifica ante eventos (confirmación, cancelación, cambios de horario).