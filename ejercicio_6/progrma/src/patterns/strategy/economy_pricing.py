from patterns.strategy.pricing_strategy import PricingStrategy


class EconomyPricing(PricingStrategy):
    SEASON_FACTORS = {"baja": 0.9, "regular": 1.0, "alta": 1.15}

    def calculate_price(self, subtotal, season="regular", anticipation_days=0):
        factor = self.SEASON_FACTORS.get(season, 1.0)
        price = subtotal * factor
        if anticipation_days >= 30:
            price *= 0.9
        elif anticipation_days >= 15:
            price *= 0.95
        return round(price, 2)