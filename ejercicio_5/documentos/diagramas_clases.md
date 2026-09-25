# Documento de Diagramas de Clases - Motor de Procesamiento de Pagos Internacionales

```mermaid
classDiagram
    direction LR

    %% ===================== Singleton =====================
    class PaymentConfig {
        <<singleton>>
        -_instance: PaymentConfig
        -_default_currency: str = "USD"
        -_exchange_rates: dict
        -_security_thresholds: dict
        +get_instance() PaymentConfig
        +exchange_rate(from, to) float
        +threshold(country) float
    }

    %% ===================== Factory Method (métodos de pago) =====================
    class PaymentMethod {
        <<interface>>
        +process(amount: float, currency: str)
    }
    class CreditCardPayment
    class BankTransferSEPA
    class BankTransferACH
    class CryptoPayment
    class DigitalWallet

    class PaymentFactory {
        +create(method_type: str, country: str) PaymentMethod
    }

    %% ===================== Strategy (comisiones + conversión) =====================
    class CommissionStrategy {
        <<interface>>
        +calculate(base_amount: float) float
    }
    class StandardCommission
    class PremiumCommission
    class InternationalCommission

    class CurrencyConversionStrategy {
        <<interface>>
        +convert(amount: float, from: str, to: str) float
    }
    class FixedRateConversion

    %% ===================== Chain of Responsibility (antifraude) =====================
    class PaymentRequest {
        +amount: float
        +country: str
        +method_type: str
        +client_type: str
    }
    class ValidationHandler {
        <<abstract>>
        -_next: ValidationHandler
        +set_next(handler: ValidationHandler) ValidationHandler
        +handle(request: PaymentRequest) bool
        #can_handle(request: PaymentRequest) bool
    }
    class AmountValidator
    class HighRiskCountryValidator
    class BehaviorPatternValidator

    %% ===================== Adapter (pasarelas externas) =====================
    class PaymentGateway {
        <<interface>>
        +charge(amount: float, currency: str, token: str) bool
    }
    class StripeAdapter {
        -_stripe_api: StripeAPI
        +charge(amount, currency, token) bool
    }
    class PayPalAdapter {
        -_paypal_api: PayPalAPI
        +charge(amount, currency, token) bool
    }
    class MercadoPagoAdapter {
        -_mp_api: MercadoPagoAPI
        +charge(amount, currency, token) bool
    }
    class StripeAPI {
        +create_charge(amount_cents: int, currency: str, source: str) str
    }
    class PayPalAPI {
        +payment(amount: str, curr: str, payer: str) str
    }
    class MercadoPagoAPI {
        +payment_create(payload: dict) dict
    }

    %% ===================== Template Method + Factory (procesadores por región) =====================
    class PaymentProcessorFactory {
        +create(country: str) PaymentProcessor
    }
    class PaymentProcessor {
        <<abstract>>
        +process_payment(method: PaymentMethod, amount: float, country: str, client_type: str)
        +notifier PaymentNotifier
        +get_currency()* str
        +conversion()* CurrencyConversionStrategy
        +commission_strategy(client_type) CommissionStrategy*
        +validation_chain()* ValidationHandler
        +gateway()* PaymentGateway
    }
    class ColombiaProcessor {
        +get_currency() str
        +commission_strategy(client_type) CommissionStrategy
        +validation_chain() ValidationHandler
        +gateway() PaymentGateway
    }
    class MexicoProcessor {
        +get_currency() str
        +commission_strategy(client_type) CommissionStrategy
        +validation_chain() ValidationHandler
        +gateway() PaymentGateway
    }
    class USProcessor {
        +get_currency() str
        +commission_strategy(client_type) CommissionStrategy
        +validation_chain() ValidationHandler
        +gateway() PaymentGateway
    }
    class EuropeProcessor {
        +get_currency() str
        +commission_strategy(client_type) CommissionStrategy
        +validation_chain() ValidationHandler
        +gateway() PaymentGateway
    }

    %% ===================== Observer (notificaciones) =====================
    class PaymentNotifier {
        -_observers: List~PaymentObserver~
        +attach(observer: PaymentObserver)
        +detach(observer: PaymentObserver)
        +notify(event: str, data: dict)
    }
    class PaymentObserver {
        <<interface>>
        +update(event: str, data: dict)
    }
    class EmailNotifier
    class SmsNotifier
    class WebhookNotifier

    %% ===================== Facade (punto de entrada único) =====================
    class PaymentFacade {
        +pay(method_type: str, amount: float, country: str, client_type: str = "standard")
    }

    %% ---------- Relaciones ----------
    %% Factory Method: métodos de pago
    PaymentFactory ..> PaymentMethod : crea
    CreditCardPayment ..|> PaymentMethod
    BankTransferSEPA ..|> PaymentMethod
    BankTransferACH ..|> PaymentMethod
    CryptoPayment ..|> PaymentMethod
    DigitalWallet ..|> PaymentMethod

    %% Strategy: comisiones y conversión
    StandardCommission ..|> CommissionStrategy
    PremiumCommission ..|> CommissionStrategy
    InternationalCommission ..|> CommissionStrategy
    FixedRateConversion ..|> CurrencyConversionStrategy

    %% Chain of Responsibility: antifraude
    AmountValidator --|> ValidationHandler
    HighRiskCountryValidator --|> ValidationHandler
    BehaviorPatternValidator --|> ValidationHandler
    ValidationHandler --> PaymentRequest : procesa

    %% Adapter: pasarelas externas
    StripeAdapter ..|> PaymentGateway
    PayPalAdapter ..|> PaymentGateway
    MercadoPagoAdapter ..|> PaymentGateway
    StripeAdapter --> StripeAPI : envuelve
    PayPalAdapter --> PayPalAPI : envuelve
    MercadoPagoAdapter --> MercadoPagoAPI : envuelve

    %% Template Method + Factory: procesadores por región
    ColombiaProcessor --|> PaymentProcessor
    MexicoProcessor --|> PaymentProcessor
    USProcessor --|> PaymentProcessor
    EuropeProcessor --|> PaymentProcessor
    PaymentProcessorFactory --> PaymentProcessor : crea

    %% Observer: notificaciones
    PaymentNotifier o--> PaymentObserver
    EmailNotifier ..|> PaymentObserver
    SmsNotifier ..|> PaymentObserver
    WebhookNotifier ..|> PaymentObserver

    %% Facade: orquesta todo
    PaymentFacade --> PaymentConfig : usa
    PaymentFacade --> PaymentFactory : usa
    PaymentFacade --> PaymentProcessorFactory : usa
    PaymentFacade --> CommissionStrategy : usa
    PaymentFacade --> CurrencyConversionStrategy : usa
    PaymentFacade --> ValidationHandler : usa
    PaymentFacade --> PaymentGateway : usa
    PaymentFacade --> PaymentNotifier : usa