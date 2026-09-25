from src.patterns.template.payment_processor import PaymentProcessor
from src.patterns.template.regional_processors import ColombiaProcessor, EuropeProcessor, MexicoProcessor, USProcessor


class PaymentProcessorFactory:

    _registry = {
        "CO": ColombiaProcessor,
        "US": USProcessor,
        "MX": MexicoProcessor,
        "EU": EuropeProcessor,
        "DE": EuropeProcessor,
        "FR": EuropeProcessor,
        "ES": EuropeProcessor,
    }

    def create(self, country: str) -> PaymentProcessor:
        processor_cls = self._registry.get(country.upper())
        if processor_cls is None:
            raise ValueError(f"Pais no soportado: {country}")
        return processor_cls()