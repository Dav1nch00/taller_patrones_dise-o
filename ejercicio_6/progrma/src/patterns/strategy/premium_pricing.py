from patterns.strategy.pricing_strategy import PricingStrategy


class PremiumPricing(PricingStrategy):
    PREMIUM_FACTOR = 1.5
    SEASON_FACTORS = {"baja": 0.95, "regular": 1.0, "alta": 1.1}

    def calculate_price(self, subtotal, season="regular", anticipation_days=0):
        factor = self.SEASON_FACTORS.get(season, 1.0)
        price = subtotal * self.PREMIUM_FACTOR * factor
        if anticipation_days >= 30:
            price *= 0.95
        return round(price, 2)