import builtins
import pytest

from .context import diversifiedblockfolio as diblo
from .test_utils import holdings_equal


@pytest.fixture(params=[('ETH', 'EUR', 1), ('ETH', 'USD', 100)])
def bad_buy(request):
    return request.param


@pytest.fixture(params=[
    {'holdings': [{}]},
    {'holdings': [{'symbol': ''}]},
    {'holdings': [{'symbol': 'BTC', 'amount': -1}]}
])
def bad_exchange_data(request):
    return request.param


@pytest.fixture(params=[('STRAT', 'USD', 1), ('ETH', 'USD', 1)])
def bad_sell(request):
    return request.param


@pytest.fixture
def exchange_data():
    return {'holdings': [
        {'symbol': 'BTC', 'amount': .0448},
        {'symbol': 'ETH', 'amount': 0.624},
        {'symbol': 'LTC', 'amount': 2.351},
        {'symbol': 'USD', 'amount': 65.02}
    ]}


def mock_buy_input(*args, **kwargs):
    return ".327"


def mock_sell_input(*args, **kwargs):
    return "45.23"


class TestExchange(object):
    def test_init(self, bad_exchange_data):
        with pytest.raises(ValueError):
            diblo.Exchange(bad_exchange_data)

    def test_buy_bad_input(self, exchange_data, bad_buy):
        exchange = diblo.Exchange(exchange_data)
        with pytest.raises(ValueError):
            exchange.buy(*bad_buy)

    @pytest.mark.parametrize(
        'symbol, quote_symbol, quote_amount, expected_holdings', [
            ('ETH', 'USD', 65.02, [
                {'symbol': 'BTC', 'amount': .0448},
                {'symbol': 'ETH', 'amount': .951},
                {'symbol': 'LTC', 'amount': 2.351},
                {'symbol': 'USD', 'amount': 0}
            ]),
            ('ETH', 'USD', 30.02, [
                {'symbol': 'BTC', 'amount': .0448},
                {'symbol': 'ETH', 'amount': .951},
                {'symbol': 'LTC', 'amount': 2.351},
                {'symbol': 'USD', 'amount': 35}
            ])
        ]
    )
    def test_buy(self, monkeypatch, exchange_data, symbol, quote_symbol,
                 quote_amount, expected_holdings):
        monkeypatch.setattr(builtins, 'input', mock_buy_input)
        exchange = diblo.Exchange(exchange_data)
        exchange.buy(symbol, quote_symbol, quote_amount)
        assert holdings_equal(exchange.holdings, expected_holdings)

    def test_sell_bad_input(self, exchange_data, bad_sell):
        exchange = diblo.Exchange(exchange_data)
        with pytest.raises(ValueError):
            exchange.sell(*bad_sell)

    @pytest.mark.parametrize(
        'symbol, quote_symbol, symbol_amount, expected_holdings', [
            ('ETH', 'USD', .624, [
                {'symbol': 'BTC', 'amount': .0448},
                {'symbol': 'ETH', 'amount': 0},
                {'symbol': 'LTC', 'amount': 2.351},
                {'symbol': 'USD', 'amount': 110.25}
            ]),
            ('ETH', 'USD', .312, [
                {'symbol': 'BTC', 'amount': .0448},
                {'symbol': 'ETH', 'amount': .312},
                {'symbol': 'LTC', 'amount': 2.351},
                {'symbol': 'USD', 'amount': 110.25}
            ])
        ]
    )
    def test_sell(self, monkeypatch, exchange_data, symbol, quote_symbol,
                  symbol_amount, expected_holdings):
        monkeypatch.setattr(builtins, 'input', mock_sell_input)
        exchange = diblo.Exchange(exchange_data)
        exchange.sell(symbol, quote_symbol, symbol_amount)
        assert holdings_equal(exchange.holdings, expected_holdings)
