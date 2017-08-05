from coinmarketcap import Market
import yaml
import argparse
import diversifiedblockfolio as diblo


def load_yaml(filename):
    with open(filename, "r") as f:
        return yaml.load(f)


def print_holdings(holdings):
    for holding in holdings:
        print(holding)


def print_value(value):
    print("{} USD".format(value))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Automated Blockchain Investments')
    parser.add_argument('action', choices=['holdings', 'value'])
    parser.add_argument('-d', '--datafile', default='data/blockfolio.yaml')

    args = parser.parse_args()
    input_data = load_yaml(args.datafile)
    fiat_exchange = diblo.Exchange(input_data['fiat_exchange'])
    market = Market()
    blockfolio = diblo.Blockfolio(fiat_exchange,
                                  input_data['asset_allocation'], market)

    if args.action == 'holdings':
        print_holdings(blockfolio.holdings)
    elif args.action == 'value':
        print_value(blockfolio.value())
