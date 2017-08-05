import coinmarketcap
import pytest
from pytest import approx

from .context import diversifiedblockfolio as diblo
from .test_utils import holdings_equal


@pytest.fixture(params=[
    [],
    [{}],
    [{'symbol': ''}],
])
def bad_asset_allocation(request):
    return request.param


@pytest.fixture
def asset_allocation():
    return [
        {'symbol': 'BTC'},
        {'symbol': 'ETH'},
        {'symbol': 'LTC'}
    ]


@pytest.fixture
def market():
    return coinmarketcap.Market()


def mock_ticker(currency="", **kwargs):
    return [
        {'symbol': 'BTC', 'price_usd': '2499.98'},
        {'symbol': 'ETH', 'price_usd': '239.94'},
        {'symbol': 'LTC', 'price_usd': '49.57'}
    ]


class TestBlockfolio(object):

    # def test_deposit(self):
    #     assert False

    def test_init_bad_asset_allocation(self, market, bad_asset_allocation):
        with pytest.raises(ValueError):
            diblo.Blockfolio(diblo.Exchange(), bad_asset_allocation, market)

    @pytest.mark.parametrize(
        'holdings, fiat_exchange', [
            (
                [{'symbol': 'BTC', 'amount': 0, 'price': 2499.98, 'value': 0},
                 {'symbol': 'ETH', 'amount': 0, 'price': 239.94, 'value': 0},
                 {'symbol': 'LTC', 'amount': 0, 'price': 49.57, 'value': 0}],
                diblo.Exchange()
            ),
            (
                [{'symbol': 'BTC', 'amount': 0, 'price': 2499.98, 'value': 0},
                 {'symbol': 'ETH', 'amount': 3.4982, 'price': 239.94,
                    'value': 839.358108},
                 {'symbol': 'LTC', 'amount': 0, 'price': 49.57, 'value': 0}],
                diblo.Exchange({'holdings': [
                    {'symbol': 'ETH', 'amount': 3.4982}
                ]})
            ),
            (
                [{'symbol': 'BTC', 'amount': .4, 'price': 2499.98,
                    'value': 999.992},
                 {'symbol': 'ETH', 'amount': 3.4982, 'price': 239.94,
                    'value': 839.358108},
                 {'symbol': 'LTC', 'amount': 10.43, 'price': 49.57,
                    'value': 517.0151}],
                diblo.Exchange({'holdings': [
                    {'symbol': 'BTC', 'amount': .4},
                    {'symbol': 'ETH', 'amount': 3.4982},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]})
            ),
        ]
    )
    def test_holdings(self, monkeypatch, holdings, fiat_exchange,
                      asset_allocation, market):
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        assert holdings_equal(blockfolio.holdings, holdings)

    @pytest.mark.parametrize(
        'value, fiat_exchange', [
            (0, diblo.Exchange()),
            (0, diblo.Exchange({'holdings': []})),
            (0, diblo.Exchange({'holdings': [
                {'symbol': 'BTC', 'amount': 0}
            ]})),
            (1249.99, diblo.Exchange({'holdings': [
                {'symbol': 'BTC', 'amount': .5}
            ]})),
            (1849.84, diblo.Exchange({'holdings': [
                {'symbol': 'BTC', 'amount': 0.5},
                {'symbol': 'ETH', 'amount': 2.5}
            ]}))
        ]
    )
    def test_value(self, monkeypatch, value, fiat_exchange, asset_allocation,
                   market):
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        assert blockfolio.value() == approx(value)
