KEY_AMOUNT = 'amount'
KEY_HOLDINGS = 'holdings'
KEY_SYMBOL = 'symbol'


class Exchange(object):
    def __init__(self, exchange_data):
        holdings = exchange_data.get(KEY_HOLDINGS, [])
        self._holdings = {}
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

    def buy(self, symbol, quote_symbol, quote_amount):
        if (quote_symbol not in self._holdings or
                self._holdings[quote_symbol].get(KEY_AMOUNT) < quote_amount):
            raise ValueError("There is not enough supply of {}"
                             .format(quote_symbol))
        print("Go ahead and use {} {} in order to buy {}."
              .format(quote_amount, quote_symbol, symbol))
        print("How much {} did you get?".format(symbol))
        symbol_amount = float(input())
        self._holdings[quote_symbol][KEY_AMOUNT] -= quote_amount
        if symbol not in self._holdings:
            self._holdings[symbol] = {KEY_SYMBOL: symbol, KEY_AMOUNT: 0}
        self._holdings[symbol][KEY_AMOUNT] += symbol_amount

    @property
    def holdings(self):
        return list(self._holdings.values())
