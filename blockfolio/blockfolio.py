class Blockfolio:
    ERROR_TEXT_NO_FIAT_SYMBOL = ""
    ERROR_TEXT_NO_FIAT_EXCHANGE = ""
    ERROR_TEXT_NO_ASSET_ALLOCATION = ""

    def __init__(self, attribute_dict):
        self.fiat_symbol = ""
        self.fiat_exchange = dict()
        self.non_fiat_exchanges = list()
        self.wallets = list()
        self.asset_allocation = list()
        return

    def deposit(self, amount):
        return

    def withdraw(self, amount):
        return

    def rebalance(self, amount=0):
        return
