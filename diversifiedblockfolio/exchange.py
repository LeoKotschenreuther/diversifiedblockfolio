KEY_AMOUNT = 'amount'
KEY_HOLDINGS = 'holdings'
KEY_SYMBOL = 'symbol'
SIDE_BUY = 'buy'
SIDE_SELL = 'sell'


class Exchange(object):
    def __init__(self, exchange_data=None):
        self._holdings = {}
        if not exchange_data:
            return
        holdings = exchange_data.get(KEY_HOLDINGS, [])
        for holding in holdings:
            symbol = holding.get(KEY_SYMBOL, '')
            if not symbol:
                raise ValueError("A holding needs a symbol")
            if KEY_AMOUNT not in holding:
                holding[KEY_AMOUNT] = 0
            amount = holding[KEY_AMOUNT]
            if amount < 0:
                raise ValueError("A holding needs an amount >= 0")
            self._holdings[symbol] = holding

    def _enough_available(self, symbol, amount):
        if (symbol not in self._holdings or
                self._holdings[symbol].get(KEY_AMOUNT) < amount):
            return False
        return True

    def _exchange(self, want_symbol, give_symbol, amount, side):
        if not self._enough_available(give_symbol, amount):
            raise ValueError("There is not enough supply of {}."
                             .format(give_symbol))
        if side == SIDE_SELL:
            print("Go ahead and sell {} {} for {}."
                  .format(amount, give_symbol, want_symbol))
        elif side == SIDE_BUY:
            print("Go ahead and buy {} with {} {}."
                  .format(want_symbol, amount, give_symbol))
        print("How much {} did you get?".format(want_symbol))
        want_amount = float(input())
        self._holdings[give_symbol][KEY_AMOUNT] -= amount
        if want_symbol not in self._holdings:
            self._holdings[want_symbol] = {
                KEY_SYMBOL: want_symbol,
                KEY_AMOUNT: 0
            }
        self._holdings[want_symbol][KEY_AMOUNT] += want_amount

    def buy(self, buy_symbol, give_symbol, give_amount):
        self._exchange(buy_symbol, give_symbol, give_amount, SIDE_BUY)

    def sell(self, sell_symbol, want_symbol, sell_amount):
        self._exchange(want_symbol, sell_symbol, sell_amount, SIDE_SELL)

    @property
    def holdings(self):
        return list(self._holdings.values())
