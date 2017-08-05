KEY_AMOUNT = 'amount'
KEY_CMC_PRICE_FIAT = 'price_usd'
KEY_HOLDINGS = 'holdings'
KEY_PRICE = 'price'
KEY_SYMBOL = 'symbol'
KEY_VALUE = 'value'
TICKER_LIMIT = 100


class Blockfolio:

    def __init__(self, fiat_exchange, asset_allocation, market):
        self._fiat_exchange = fiat_exchange
        if not asset_allocation:
            raise ValueError("The asset allocation needs at least one asset")
        for allocation in asset_allocation:
            symbol = allocation.get(KEY_SYMBOL, '')
            if not symbol:
                raise ValueError("An allocation needs a symbol")
        self._asset_allocation = asset_allocation
        self._market = market

    def _ticker_price(self, symbol, ticker):
        return next(float(item.get(KEY_CMC_PRICE_FIAT, 0)) for item in ticker
                    if item.get(KEY_SYMBOL) == symbol)

    def _holding_amount(self, symbol, exchange):
        return next((holding.get(KEY_AMOUNT, 0) for holding
                     in exchange.holdings
                     if holding[KEY_SYMBOL] == symbol),
                    0)

    # def deposit(self, amount):
    #     return

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

    def value(self):
        holdings = self._fiat_exchange.holdings
        if len(holdings) == 0:
            return 0
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        return sum(holding.get(KEY_AMOUNT, 0) *
                   self._ticker_price(holding.get(KEY_SYMBOL), ticker)
                   for holding in holdings)
