from coinmarketcap import Market
import yaml
import argparse
from blockfolio import Blockfolio

coinmarketcap = Market()


def load_yaml(filename):
    with open(filename, "r") as f:
        return yaml.load(f)


class OldBlockfolio:

    def __init__(self, blockfolio_dict):
        self.fiat = blockfolio_dict['fiat']
        self.minimum_transaction_value = blockfolio_dict['minimum_transaction_value']
        self.exchanges = blockfolio_dict['exchanges']
        self.assets = blockfolio_dict['assets']

    def aggregate_amounts(self):
        for asset in self.assets:
            asset['amount'] = 0
            if 'locations' in asset.keys():
                asset['amount'] = sum([location['amount'] for location in asset['locations']])

    def calculate_values(self):
        ticker = coinmarketcap.ticker(limit=100, convert=self.fiat['symbol'])
        for asset in self.assets:
            if 'value' in asset.keys():
                continue
            ticker_item = next(item for item in ticker if item['symbol'] == asset['name'])
            asset_price = float(ticker_item['price_' + self.fiat['symbol'].lower()])
            asset['price'] = asset_price
            asset['value'] = asset['amount'] * asset_price

    def calculate_total_value(self):
        self.value = sum([asset['value'] for asset in self.assets]) + self.fiat['amount']

    def calculate_wanted_values_and_changes(self):
        total_weight = sum([asset['weight'] for asset in self.assets])
        for asset in self.assets:
            asset['wanted_value'] = asset['weight'] / total_weight * self.value
            asset['wanted_change'] = asset['wanted_value'] - asset['value']

    def _aggregate_actions(self, actions):
        aggregated_actions = list()
        for asset in self.assets:
            asset_actions = [action for action in actions if action['symbol'] == asset['name']]
            if asset_actions:
                aggregated_actions.append({
                    'symbol': asset['name'],
                    'value': sum([action['value'] for action in asset_actions]),
                    'action': "buy/sell",
                    'quote_symbol': asset['quote_symbol'],
                    'location': asset['exchange']
                })
        return aggregated_actions

    def _plan_buy_sell_actions(self):
        actions = list()
        for asset in self.assets:
            if asset['wanted_change'] != 0:
                actions.append({
                    'symbol': asset['name'],
                    'value': asset['wanted_change'],
                    'action': "buy/sell",
                    'quote_symbol': asset['quote_symbol'],
                    'location': asset['exchange']
                })
                if asset['quote_symbol'] != self.fiat['symbol']:
                    quote_asset = next(item for item in self.assets if item['name'] == asset['quote_symbol'])
                    actions.append({
                        'symbol': quote_asset['name'],
                        'value': asset['wanted_change'],
                        'action': "buy/sell",
                        'quote_symbol': self.fiat['symbol'],
                        'location': quote_asset['exchange']
                    })
        return actions

    def _aggregate_transfers(self, transfers):
        aggregated_transfers = list()
        for exchange in self.exchanges:
            exchange_transfer_values = [transfer['value'] for transfer in transfers if transfer['to'] == exchange]
            if exchange_transfer_values:
                aggregated_transfers.append({
                    'symbol': transfers[0]['symbol'],
                    'value': sum(exchange_transfer_values),
                    'from': transfers[0]['from'],
                    'to': exchange
                })
        return aggregated_transfers

    def plan_rebalance(self):
        actions = self._plan_buy_sell_actions()
        aggregated_actions = self._aggregate_actions(actions)
        fiat_actions = [action for action in aggregated_actions if action['quote_symbol'] == self.fiat['symbol']]
        non_fiat_actions = [action for action in aggregated_actions if action['quote_symbol'] != self.fiat['symbol']]
        transfer_symbols = set([action['quote_symbol'] for action in non_fiat_actions])
        all_transfers = list()
        for action in fiat_actions:
            print(action)
            asset = next(asset for asset in self.assets if asset['name'] == action['symbol'])
            if asset['storage'] != "Wallet" and action['symbol'] not in transfer_symbols:
                continue
            transfers = []
            print("How much " + action['symbol'] + " did you buy?")
            bought_amount = float(input(""))
            future_actions = [item for item in non_fiat_actions if item['quote_symbol'] == action['symbol']]
            for a in future_actions:
                transfers.append({
                    'symbol': action['symbol'],
                    'value': a['value'],
                    'from': asset['exchange'],
                    'to': a['location']
                })
            aggregated_transfers = self._aggregate_transfers(transfers)
            wallet_value = 0
            if asset['locations']:
                wallet_amount = next((location['amount'] for location in asset['locations']
                                        if location['name'] == "Wallet"), 0)
                wallet_value = wallet_amount * asset['price']
            aggregated_transfers.append({
                'symbol': action['symbol'],
                'value': asset['wanted_value'] - wallet_value,
                'from': asset['exchange'],
                'to': "Wallet"
            })
            total_transfer_value = sum(t['value'] for t in aggregated_transfers)
            for transfer in aggregated_transfers:
                transfer['amount'] = transfer['value'] / total_transfer_value * bought_amount
                print(transfer)
            all_transfers = all_transfers + aggregated_transfers
        for transfer in all_transfers:
            if transfer['to'] == 'Wallet':
                continue
            actions = [action for action in non_fiat_actions
                       if action['quote_symbol'] == transfer['symbol'] and action['location'] == transfer['to']]
            total_value = sum([action['value'] for action in actions])
            for action in actions:
                action['amount'] = transfer['amount'] * action['value'] / total_value
                print(action)

    def deposit(self, fiat_amount):
        self.aggregate_amounts()
        self.calculate_values()
        self.calculate_total_value()
        self.calculate_wanted_values_and_changes()
        self.plan_rebalance()

    def withdraw(self, fiat_amount):
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deposits and Withdrawals for a Blockfolio')
    parser.add_argument('action', choices=['deposit', 'withdraw'])
    parser.add_argument('amount', type=float)

    args = parser.parse_args()
    input_data = load_yaml("data/blockfolio.yaml")
    blockfolio = Blockfolio(input_data)
    if args.action == 'deposit':
        blockfolio.deposit(args.amount)
    elif args.action == 'withdraw':
        blockfolio.withdraw(args.amount)
