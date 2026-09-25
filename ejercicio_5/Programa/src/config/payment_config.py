class PaymentConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ready = False
        return cls._instance

    def _initialize(self):
        if self._ready:
            return
        self._default_currency = "USD"
        self._exchange_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "COP": 4120.0,
            "MXN": 18.5,
        }
        self._security_thresholds = {
            "US": 10000.0,
            "CO": 1500.0,
            "EU": 9000.0,
            "MX": 4000.0,
        }
        self._ready = True

    @classmethod
    def get_instance(cls):
        instance = cls()
        instance._initialize()
        return instance

    @property
    def default_currency(self):
        return self._default_currency

    def exchange_rate(self, source, target):
        if source not in self._exchange_rates or target not in self._exchange_rates:
            raise ValueError(f"Moneda no soportada: {source} -> {target}")
        return self._exchange_rates[target] / self._exchange_rates[source]

    def threshold(self, country):
        return self._security_thresholds.get(country.upper(), 10000.0)