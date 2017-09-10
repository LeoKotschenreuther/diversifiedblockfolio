import math

TICKER_LIMIT = 100


class Blockfolio:

    def __init__(self, fiat_exchange, asset_allocation, market):
        self._fiat_exchange = fiat_exchange
        if not asset_allocation:
            raise ValueError("The asset allocation needs at least one asset")
        for allocation in asset_allocation:
            symbol = allocation.get('symbol', '')
            if not symbol:
                raise ValueError("An allocation needs a symbol")
        self._asset_allocation = asset_allocation
        self._market = market

    def _ticker_price(self, symbol, ticker):
        return next(float(item.get('price_usd', 0)) for item in ticker
                    if item.get('symbol') == symbol)

    def _holding_amount(self, symbol, exchange):
        return next((holding.get('amount', 0) for holding in exchange.holdings
                     if holding['symbol'] == symbol), 0)

    def _holding_drift(self, holding):
        if holding['target_weight'] == 0:
            return math.inf
        return ((holding['weight'] - holding['target_weight']) /
                holding['target_weight'])

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("The deposit amount must be greater than zero.")
        holdings = self.holdings
        total_value = self.value() + amount
        print('total_value:', total_value)
        target_value = total_value / len(self._asset_allocation)
        print('target_value:', target_value)
        print('amount:', amount)
        holdings.sort(key=lambda holding: holding['value'])
        print(holdings)
        i = 0
        while amount >= 0.01:
            buy_value = target_value - holdings[i]['value']
            print('buy_value1:', buy_value)
            if (i + 1) < len(holdings):
                buy_value = min(buy_value, holdings[i + 1]['value'] -
                                holdings[i]['value'])
            print('buy_value2:', buy_value)
            total_buy = buy_value * (i + 1)
            print('total_buy1:', total_buy)
            if total_buy > amount:
                buy_value = buy_value * amount / total_buy
                total_buy = amount
                print('total_buy2:', total_buy)
            for holding in holdings[:i + 1]:
                holding['buy_value'] = holding.get('buy_value', 0) + buy_value
            amount -= total_buy
            i += 1
            print(i, amount)

        for holding in holdings:
            if 'buy_value' in holding:
                self._fiat_exchange.buy(holding['symbol'], 'USD',
                                        holding['buy_value'])

    @property
    def holdings(self):
        ticker = self._market.ticker(limit=TICKER_LIMIT)
        holdings = []
        for asset in self._asset_allocation:
            amount = self._holding_amount(asset['symbol'], self._fiat_exchange)
            holding = {
                'symbol': asset['symbol'],
                'amount': amount,
                'price': self._ticker_price(asset['symbol'], ticker)
            }
            holding['value'] = holding['amount'] * holding['price']
            holdings.append(holding)
        return holdings

    def value(self):
        holdings = self.holdings
        return sum(holding.get('value', 0) for holding in holdings)
