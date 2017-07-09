KEY_AMOUNT = 'amount'
KEY_CMC_PRICE_FIAT = 'price_usd'
KEY_HOLDINGS = 'holdings'
KEY_PRICE = 'price'
KEY_SYMBOL = 'symbol'
KEY_TARGETWEIGHT = 'target_weight'
KEY_VALUE = 'value'
TICKER_LIMIT = 100


class Blockfolio:

    def __init__(self, fiat_exchange, asset_allocation, market):
        for holding in fiat_exchange.get(KEY_HOLDINGS, []):
            symbol = holding.get(KEY_SYMBOL, '')
            if not symbol:
                raise ValueError("A holding needs a symbol")
            amount = holding.get(KEY_AMOUNT, 0)
            if amount < 0:
                raise ValueError("A holding needs an amount >= 0")
        self._fiat_exchange = fiat_exchange
        if not asset_allocation:
            raise ValueError("The asset allocation needs at least one asset")
        for allocation in asset_allocation:
            symbol = allocation.get(KEY_SYMBOL, '')
            if not symbol:
                raise ValueError("An allocation needs a symbol")
            target_weight = allocation.get(KEY_TARGETWEIGHT, 0)
            if target_weight <= 0:
                raise ValueError("An allocation needs a target weight > 0")
        self._asset_allocation = asset_allocation
        self._market = market

    def _ticker_price(self, symbol, ticker):
        return next(float(item.get(KEY_CMC_PRICE_FIAT, 0)) for item in ticker
                    if item.get(KEY_SYMBOL) == symbol)

    def _holding_amount(self, symbol, exchange):
        return next((holding.get(KEY_AMOUNT, 0) for holding
                     in exchange.get(KEY_HOLDINGS, [])
                     if holding[KEY_SYMBOL] == symbol),
                    0)

    def value(self):
        holdings = self._fiat_exchange.get(KEY_HOLDINGS, [])
        if len(holdings) == 0:
            return 0
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        return sum(holding.get(KEY_AMOUNT, 0) *
                   self._ticker_price(holding.get(KEY_SYMBOL), ticker)
                   for holding in holdings)

    @property
    def holdings(self):
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        holdings = []
        for asset in self._asset_allocation:
            amount = self._holding_amount(asset[KEY_SYMBOL],
                                          self._fiat_exchange)
            holding = {
                KEY_SYMBOL: asset[KEY_SYMBOL],
                KEY_AMOUNT: amount,
                KEY_PRICE: self._ticker_price(asset[KEY_SYMBOL], ticker),
            }
            holding[KEY_VALUE] = holding[KEY_AMOUNT] * holding[KEY_PRICE]
            holdings.append(holding)
        return holdings
