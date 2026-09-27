from src.patterns.facade.payment_facade import PaymentFacade


def mostrar(resultado):
    estado = "OK" if resultado.success else "RECHAZADO"
    print(f"-> [{estado}] {resultado.message} | id={resultado.transaction_id} | "
          f"{round(resultado.amount, 2)} {resultado.currency} | comision={round(resultado.commission, 2)}")


def main():
    facade = PaymentFacade()

    print("=== 1. Tarjeta de credito en Colombia ===")
    mostrar(facade.pay("credit_card", 120000, "CO", "standard"))

    print("=== 2. SEPA en Alemania (cliente premium) ===")
    mostrar(facade.pay("sepa", 250, "DE", "premium"))

    print("=== 3. ACH en Estados Unidos ===")
    mostrar(facade.pay("ach", 75, "US", "standard"))

    print("=== 4. Billetera digital en Mexico ===")
    mostrar(facade.pay("digital_wallet", 2000, "MX", "premium"))

    print("=== 5. Rechazado por antifraude (monto sospechoso) ===")
    mostrar(facade.pay("credit_card", 90000, "US", "standard"))

    print("=== 6. Metodo no disponible en Colombia ===")
    try:
        facade.pay("sepa", 100, "CO", "standard")
    except ValueError as e:
        print("->", e)


if __name__ == "__main__":
    main()