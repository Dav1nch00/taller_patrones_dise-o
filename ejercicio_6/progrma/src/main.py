from domain.additional_service import AdditionalService
from domain.flight import Flight
from domain.passenger import Passenger
from patterns.state.reservation_state import InvalidStateTransitionError
from patterns.strategy.economy_pricing import EconomyPricing
from patterns.strategy.premium_pricing import PremiumPricing
from services.reservation_service import ReservationService


def demo_reserva_ana():
    service = ReservationService()

    pasajero = Passenger("P001", "Ana Torres", "ana.torres@mail.com", "3001234567")
    vuelo = Flight("AV-815", "BOG", "MAD", "2026-10-01 22:30")
    servicios = [
        AdditionalService("Equipaje documentado", 60.0),
        AdditionalService("Selección de asiento", 25.0),
    ]
    preferencias = {"asiento": "ventana", "comida": "vegetariana"}

    reserva = service.crear_reserva(
        pasajero,
        vuelo,
        base_price=420.0,
        services=servicios,
        preferences=preferencias,
        pricing_strategy=EconomyPricing(),
    )

    print("=== Reserva creada ===")
    print(reserva)
    print("Preferencias:", reserva.preferences)
    print("Precio base + servicios:", round(reserva.base_price + sum(s.costo for s in reserva.services), 2))

    print("\n=== Precio dinámico (Strategy) ===")
    print("Alta temporada hoy:      $", service.calcular_precio(reserva, "alta", 0))
    print("Alta temporada 40 días:  $", service.calcular_precio(reserva, "alta", 40))
    print("Baja temporada 40 días:  $", service.calcular_precio(reserva, "baja", 40))

    print("\n=== Upgrade a Premium (Strategy en tiempo de ejecución) ===")
    service.upgrade(reserva, PremiumPricing())
    print("Nuevo precio alta temporada: $", service.calcular_precio(reserva, "alta", 0))

    print("\n=== Ciclo de vida (State + Observer) ===")
    print(service.modificar(reserva))
    service.confirmar(reserva)
    service.check_in(reserva)
    service.abordar(reserva)

    print("\n=== Transición inválida (controlada) ===")
    try:
        service.cancelar(reserva)
    except InvalidStateTransitionError as e:
        print("ERROR:", e)

    print("\n=== Estado final ===")
    print(reserva)


def demo_reserva_cancelada():
    service = ReservationService()

    pasajero = Passenger("P002", "Luis Pérez", "luis.perez@mail.com", "3209876543")
    vuelo = Flight("AV-220", "MDE", "CDMX", "2026-11-05 08:15")

    reserva = service.crear_reserva(
        pasajero,
        vuelo,
        base_price=310.0,
        pricing_strategy=EconomyPricing(),
    )

    print("=== Reserva cancelada ===")
    print(reserva)
    service.cancelar(reserva)
    print(reserva)
    try:
        service.modificar(reserva)
    except InvalidStateTransitionError as e:
        print("ERROR:", e)


if __name__ == "__main__":
    demo_reserva_ana()
    print()
    demo_reserva_cancelada()