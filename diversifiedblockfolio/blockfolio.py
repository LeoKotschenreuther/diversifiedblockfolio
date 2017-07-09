COINMARKETCAP_PRICE_FIAT = 'price_usd'
TICKER_LIMIT = 100


class Blockfolio:

    def __init__(self, fiat_exchange, asset_allocation, market):
        for holding in fiat_exchange.get('holdings', []):
            amount = holding.get('amount', 0)
            symbol = holding.get('symbol', '')
            if amount < 0 or not symbol:
                raise ValueError("A holding can't have a negative amount")
        self._fiat_exchange = fiat_exchange
        self._market = market

    def _ticker_price(self, symbol, ticker):
        return next(float(item.get('price_usd', 0)) for item in ticker
                    if item.get('symbol') == symbol)

    def value(self):
        holdings = self._fiat_exchange.get('holdings', [])
        if len(holdings) == 0:
            return 0
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        value = sum(holding.get('amount', 0) *
                    self._ticker_price(holding.get('symbol'), ticker)
                    for holding in holdings)
        return round(value, 2)

    def holdings(self):
        # make it a property
        # return for each held asset:
        # - symbol
        # - total amount
        # - last price
        # - total value
        # - preferred weight
        # - preferred change in value
        return 0
