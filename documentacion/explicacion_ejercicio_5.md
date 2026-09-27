# Explicación del Motor de Procesamiento de Pagos (Ejercicio 5)

Recorrido por cada paso del desarrollo, cómo funciona cada patrón y cómo fluye un pago completo.

---

## Paso 1 — `PaymentConfig` (patrón Singleton)

**Archivo:** `Programa/src/config/payment_config.py`

**Problema que resuelve:** si cada módulo tuviera su propia copia de la configuración (moneda, tasas, umbrales), una tasa actualizada en un módulo no se vería en otro → inconsistencias en operaciones de dinero.

**Solución:** garantizar que solo exista **una** instancia viva de `PaymentConfig` y que todos pidan esa misma instancia.

```python
def __new__(cls):                 # se ejecuta al hacer PaymentConfig()
    if cls._instance is None:
        cls._instance = super().__new__(cls)   # crea la única instancia
        cls._instance._ready = False
    return cls._instance                       # si ya existía, devuelve la misma
```

El truco del Singleton en Python es `__new__`: no importa cuántas veces hagas `PaymentConfig()`, siempre obtienes la misma instancia. Y el método `get_instance()` es la "puerta" de acceso que además garantiza que quede inicializada:

```python
a = PaymentConfig.get_instance()
b = PaymentConfig.get_instance()
a is b   # -> True, es el mismo objeto
```

Guarda 3 datos base:
- `_default_currency = "USD"` — la moneda canónica de todo el motor.
- `_exchange_rates` — tasas fijas (USD=1, EUR=0.92, COP=4120, MXN=18.5).
- `_security_thresholds` — cuánto es "sospechoso" por país, **en USD** (CO=1500, US=10000, EU=9000, MX=4000).

Servicios:
- `exchange_rate(source, target)` — calcula la tasa cruzada, ej.: `USD→COP` es `4120/1 = 4120`.
- `threshold(country)` — devuelve el umbral de antifraude del país.

---

## Paso 2 — `domain/` (los datos que viajan por el motor)

**Archivos:** `payment_request.py` y `payment_result.py`

Dataclasses para los dos "vehículos" de información:

- `PaymentRequest(amount, country, method_type, client_type)` — lo que llega a la validación: cuánto, dónde, con qué método y qué tipo de cliente.
- `PaymentResult(success, message, transaction_id, amount, currency, commission, created_at)` — lo que devuelve el sistema: si el pago pasó, id de la transacción, monto final en USD y la comisión cobrada.

---

## Paso 3 — `strategy/` (algoritmos intercambiables en plena ejecución)

**Archivos:** `commission.py` y `conversion.py`

El patrón Strategy consiste en: definir una **interfaz común** y varias clases que la implementan con distinto comportamiento. El código que usa la estrategia **no sabe cuál es**, solo sabe que tiene los métodos de la interfaz.

**Comisiones** (`CommissionStrategy` + 3 estrategias):

```
CommissionStrategy  (interfaz: calculate(base) -> float)
├── StandardCommission        2.0%  → 1000 USD → 20 USD
├── PremiumCommission         0.5%  → 1000 USD → 5 USD
└── InternationalCommission   3.5%  → 1000 USD → 35 USD
```

**Conversión** (`CurrencyConversionStrategy` + `FixedRateConversion`): `convert(amount, source, target)` multiplica el monto por la tasa cruzada del Singleton (`PaymentConfig.exchange_rate`). Es "fixed rate" porque usa las tasas base fijas de la configuración.

---

## Paso 4 — `factory/` (crear métodos de pago sin `if`s)

**Archivos:** `payment_methods.py` y `payment_factory.py`

**Problema:** si para crear cada método escribieras `if method == "sepa": return BankTransferSEPA()`, cada método nuevo obligaría a tocar ese `if` central (se viola el principio de abierto/cerrado).

**Solución (Factory Method):** cada tipo de pago es una clase que implementa la interfaz `PaymentMethod` (con `name` y `supports(country)`), y un solo `PaymentFactory` las crea según un diccionario `_registry`.

```
PaymentMethod          (interfaz)
├── CreditCardPayment  name="credit_card"      (todo el mundo)
├── BankTransferSEPA   name="sepa"             (EU, DE, FR, ES, IT)
├── BankTransferACH    name="ach"              (US, MX)
├── CryptoPayment      name="crypto"           (todo el mundo)
└── DigitalWallet      name="digital_wallet"   (todo el mundo)
```

`PaymentFactory.create("sepa", "CO")` no solo crea el objeto, **valida que el método exista y sea compatible con el país** (SEPA en Colombia → `ValueError`). Agregar un método nuevo = crear la clase y registrarla en el diccionario; nada más.

---

## Paso 5 — `chain/` (validación antifraude en cadena)

**Archivos:** `handler.py` y `validators.py`

**Patrón Chain of Responsibility:** cada validador decide si **rechaza** o si **pasa el caso al siguiente**. Forman una cadena, no un montón de `if`s anidados.

```python
chain = AmountValidator()
chain.set_next(HighRiskCountryValidator()).set_next(BehaviorPatternValidator())
```

`set_next()` devuelve el siguiente eslabón, por eso se puede encadenar de corrido. Lógica de `handle()`:

```python
def handle(self, request):
    if self._validate(request):          # este eslabón pasa?
        return self._next.handle(request) if self._next else True   # → siguiente
    return False                          # → rechazado aquí y se corta
```

Los 3 eslabones:
1. `AmountValidator` — monto > umbral del país (del Singleton) → sospechoso.
2. `HighRiskCountryValidator` — país en lista negra (CU, IR, KP, SY, VE).
3. `BehaviorPatternValidator` — monto operacional máximo 50000 USD.

Si cualquiera falla devuelve `False` y se corta la cadena. Agregar una regla = escribir una clase y agregarla a la cadena.

---

## Paso 6 — `adapter/` (hablar un solo idioma con Stripe, PayPal y MercadoPago)

**Archivos:** `gateway.py`, `stripe_adapter.py`, `paypal_adapter.py`, `mercadopago_adapter.py`

**Problema:** cada pasarela tiene su API distinta e inmodificable (Stripe usa `create_charge` en centavos, PayPal usa `payment` con strings, MercadoPago usa `payment_create` con un dict).

**Solución (Adapter):** cada pasarela tiene su clase `XXXAPI` (simulada = representa el SDK externo que no podemos tocar) y un "adaptador" que la envuelve y la presenta con una interfaz uniforme.

```
PaymentGateway          (interfaz: charge(amount, currency, token))
├── StripeAdapter        -> StripeAPI.create_charge(centavos, ...)
├── PayPalAdapter        -> PayPalAPI.payment(str, ...)
└── MercadoPagoAdapter   -> MercadoPagoAPI.payment_create(dict, ...)
```

El adaptador convierte: pasa el monto a centavos para Stripe (`int(round(amount*100))`), a string para PayPal, a dict para MercadoPago → y todos devuelven el id de la transacción con el mismo formato. Son simulaciones; usan `uuid` para generar ids.

---

## Paso 7 — `observer/` (avisar sin acoplar)

**Archivos:** `observer.py`, `notifier.py`, `notifiers.py`

**Problema:** la lógica de pago no debe saber cómo notificar (email vs SMS vs webhook). Si le metes `if canal == "email"` dentro del procesador, cada canal nuevo obliga a tocar el núcleo.

**Solución (Observer):**
- `PaymentObserver` define la interfaz `update(event, data)`.
- `PaymentNotifier` mantiene una lista de observadores y permite `attach`/`detach`; su `notify()` recorre la lista y le dice a cada uno `update(evento, datos)`.
- `EmailNotifier`, `SmsNotifier`, `WebhookNotifier` implementan qué hacer con ese evento (aquí solo imprimen).

El procesador solo hace `notifier.notify("payment.success", {...})` y no sabe quién escucha. Puedes agregar un canal nuevo sin tocar el motor.

---

## Paso 8 — `template/` (flujo invariable + pasos variables por región)

**Archivos:** `payment_processor.py`, `regional_processors.py`, `payment_processor_factory.py`

Este es el corazón del motor y combina dos patrones.

**Template Method:** defines el **esqueleto del algoritmo** en la clase base (que no se toca) y dejas "huecos" (métodos abstractos) que cada región completa.

```python
def process_payment(self, method, amount, country, client_type):
    converted = self.conversion().convert(...)        # 1. convierte a USD
    request = PaymentRequest(...)                      #    con monto en USD
    if not self.validation_chain().handle(request):    # 2. antifraude
        ...return rechazado...
    commission = self.commission_strategy(client_type).calculate(converted)  # 3. comisión
    total = converted + commission
    transaction_id = self.gateway().charge(total, "USD", ...)                # 4. cobrar
    ...notify("payment.success", ...)                                       # 5. avisar
    return PaymentResult(...)
```

Ese orden **siempre es el mismo** (flujo invariable). Lo que cambia por región son los hooks:

| Hook | Colombia | US | Europa | México |
|---|---|---|---|---|
| `get_currency()` | COP | USD | EUR | MXN |
| `gateway()` | MercadoPago | Stripe | PayPal | MercadoPago |
| `commission_strategy()` | std/premium | std/premium | **internacional** | std/premium |

Cada región solo sobreescribe lo suyo; `process_payment` nunca se toca. Esto reduce duplicación: la estructura del pago está escrita **una sola vez**.

**Factory Method para procesadores:** `PaymentProcessorFactory.create(country)` devuelve el procesador correcto según el país (`CO`→Colombia, `MX`→México, `US`→US, `EU/DE/FR/ES`→Europa). Así se evita `if país == "CO": ... elif país == "US": ...`.

---

## Paso 9 — `facade/payment_facade.py` (el punto de entrada único)

**Facade** no agrega lógica nueva: **orquesta** lo que ya existe y le da a quien integra un único método:

```python
def pay(self, method_type, amount, country, client_type="standard"):
    method = self._payment_factory.create(method_type, country)      # Factory: método de pago
    processor = self._processor_factory.create(country)              # Factory: procesador por país
    processor.notifier.attach(EmailNotifier())                       # Observer: canales
    processor.notifier.attach(SmsNotifier())
    processor.notifier.attach(WebhookNotifier())
    return processor.process_payment(method, amount, country, client_type)  # Template Method
```

Es el propósito del ejercicio: que un equipo de integración haga **una sola llamada** sin saber nada de validadores, gateways, monedas ni comisiones.

---

## Paso 10 — `main.py` (demo)

Ejecutar `python main.py` desde `Programa/`. Cada caso prueba un camino:

1. Tarjeta en Colombia: `PaymentFactory` crea `CreditCardPayment` → `PaymentProcessorFactory` crea `ColombiaProcessor` → convierte 120000 COP ≈ 29.13 USD → valida (pasa) → comisión 2% = 0.58 → MercadoPago cobra → notifica (email, sms, webhook).
2. SEPA en Alemania premium: PayPal, moneda EUR, comisión internacional 3.5%.
3. ACH en EE.UU.: Stripe, USD, comisión 2%.
4. Billetera en México: MercadoPago, MXN→USD.
5. 90000 USD en EE.UU.: rechazado por `AmountValidator` (90000 > umbral 10000) → notifica `payment.failed`.
6. SEPA en Colombia: `ValueError` del `PaymentFactory` (no soportada ahí).

---

## El flujo completo de un pago, resumido

```
pay("credit_card", 120000, "CO", "standard")
  │
  ├─ 1. PaymentFactory -> CreditCardPayment          (Factory Method)
  ├─ 2. PaymentProcessorFactory -> ColombiaProcessor (Factory Method)
  ├─ 3. attach() email, sms, webhook                  (Observer)
  └─ 4. process_payment()                            (Template Method)
         ├─ conversion() 120000 COP -> 29.13 USD      (Strategy)
         ├─ validation_chain()                        (Chain of Responsibility)
         │     monto<=umbral CO? -> país OK? -> patrón OK?
         ├─ commission_strategy() 2% = 0.58 USD       (Strategy)
         ├─ gateway().charge(29.71 USD) -> mp_xxxx    (Adapter)
         ├─ notifier.notify("payment.success", ...)   (Observer)
         └─ PaymentResult(success=True, ...)
```

**Los 8 patrones del enunciado** quedan distribuidos: Singleton (config global), Factory Method (métodos de pago + procesadores), Strategy (comisiones + conversión), Chain of Responsibility (antifraude), Adapter (pasarelas), Observer (notificaciones), Template Method (flujo de pago) y Facade (orquestador).