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


@pytest.fixture
def exchange_data():
    return {'holdings': [
        {'symbol': 'BTC', 'amount': .0448},
        {'symbol': 'ETH', 'amount': 0.624},
        {'symbol': 'LTC', 'amount': 2.351},
        {'symbol': 'USD', 'amount': 65.02}
    ]}


def mock_input(*args, **kwargs):
    return ".327"


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
        monkeypatch.setattr(builtins, 'input', mock_input)
        exchange = diblo.Exchange(exchange_data)
        exchange.buy(symbol, quote_symbol, quote_amount)
        assert holdings_equal(exchange.holdings, expected_holdings)
