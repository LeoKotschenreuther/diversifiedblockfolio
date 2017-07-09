TICKER_LIMIT = 100


class Blockfolio:

    def __init__(self, fiat_exchange, market):
        for holding in fiat_exchange.get('holdings', []):
            amount = holding.get('amount', 0)
            if amount < 0:
                raise ValueError("A holding can't have a negative amount")
        self._fiat_exchange = fiat_exchange
        self._market = market

    def value(self):
        holdings = self._fiat_exchange.get('holdings', [])
        if len(holdings) == 0:
            return 0
        value = 0
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        for holding in holdings:
            price = next(float(item.get('price_usd', 0)) for item in ticker
                         if item.get('symbol') == holding.get('symbol'))
            value += holding.get('amount', 0) * price
        return round(value, 2)
