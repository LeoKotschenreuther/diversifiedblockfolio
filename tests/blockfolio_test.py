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


@pytest.fixture(params=[0, -0.12, -5])
def bad_deposit(request):
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

    def test_deposit_bad_input(self, asset_allocation, market, bad_deposit):
        blockfolio = diblo.Blockfolio(diblo.Exchange(), asset_allocation,
                                      market)
        with pytest.raises(ValueError):
            blockfolio.deposit(bad_deposit)

    @pytest.mark.parametrize(
        'fiat_exchange, asset_allocation, amount, holdings', [
            # no preexisting holdings, equal weight allocation
            (
                diblo.Exchange(),
                [{'symbol': 'BTC'}, {'symbol': 'ETH'}, {'symbol': 'LTC'}],
                300,
                [{'symbol': 'BTC', 'amount': .1, 'price': 1000, 'value': 100},
                 {'symbol': 'ETH', 'amount': 1, 'price': 100, 'value': 100},
                 {'symbol': 'LTC', 'amount': 10, 'price': 10, 'value': 100}]
            ),
            # no preexisting holdings, non equal weight allocation
            (
                diblo.Exchange(),
                [
                    {'symbol': 'BTC', 'target_weight': 5},
                    {'symbol': 'ETH', 'target_weight': 3},
                    {'symbol': 'LTC', 'target_weight': 2}
                ],
                500,
                [{'symbol': 'BTC', 'amount': .25, 'price': 1000, 'value': 250},
                 {'symbol': 'ETH', 'amount': 1.5, 'price': 100, 'value': 150},
                 {'symbol': 'LTC', 'amount': 10, 'price': 10, 'value': 100}]
            ),
            # preexisting holdings, equal weight allocation,
            # all assets get bought
            (
                diblo.Exchange({'holdings': [
                    {'symbol': 'BTC', 'amount': .2},
                    {'symbol': 'ETH', 'amount': 2.4982},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]}),
                [{'symbol': 'BTC'}, {'symbol': 'ETH'}, {'symbol': 'LTC'}],
                300.01,
                [
                    {'symbol': 'BTC', 'amount': .28471, 'price': 1000,
                     'value': 284.71},
                    {'symbol': 'ETH', 'amount': 2.8471, 'price': 100,
                     'value': 284.71},
                    {'symbol': 'LTC', 'amount': 28.471, 'price': 10,
                     'value': 284.71}
                ]
            ),
            # preexisting holdings, non equal weight allocation,
            # all assets get bought
            (
                diblo.Exchange({'holdings': [
                    {'symbol': 'BTC', 'amount': .4},
                    {'symbol': 'ETH', 'amount': 3.4982},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]}),
                [
                    {'symbol': 'BTC', 'target_weight': 5},
                    {'symbol': 'ETH', 'target_weight': 3},
                    {'symbol': 'LTC', 'target_weight': 2}
                ],
                500.08,
                [
                    {'symbol': 'BTC', 'amount': .6771, 'price': 1000,
                     'value': 677.1},
                    {'symbol': 'ETH', 'amount': 4.0626, 'price': 100,
                     'value': 406.26},
                    {'symbol': 'LTC', 'amount': 27.084, 'price': 10,
                     'value': 270.84}
                ]
            ),
            # preexisting holdings, equal weight allocation,
            # not all assets get bought
            (
                diblo.Exchange({'holdings': [
                    {'symbol': 'BTC', 'amount': .8},
                    {'symbol': 'ETH', 'amount': 2.4982},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]}),
                [{'symbol': 'BTC'}, {'symbol': 'ETH'}, {'symbol': 'LTC'}],
                300.04,
                [
                    {'symbol': 'BTC', 'amount': .8, 'price': 1000,
                     'value': 800},
                    {'symbol': 'ETH', 'amount': 3.2708, 'price': 100,
                     'value': 327.08},
                    {'symbol': 'LTC', 'amount': 32.708, 'price': 10,
                     'value': 327.08}
                ]
            ),
            # preexisting holdings, non equal weight allocation,
            # not all assets get bought
            (
                diblo.Exchange({'holdings': [
                    {'symbol': 'BTC', 'amount': .8},
                    {'symbol': 'ETH', 'amount': 3.4983},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]}),
                [
                    {'symbol': 'BTC', 'target_weight': 5},
                    {'symbol': 'ETH', 'target_weight': 3},
                    {'symbol': 'LTC', 'target_weight': 2}
                ],
                300.07,
                [
                    {'symbol': 'BTC', 'amount': .8, 'price': 1000,
                     'value': 800},
                    {'symbol': 'ETH', 'amount': 4.5252, 'price': 100,
                     'value': 452.52},
                    {'symbol': 'LTC', 'amount': 30.168, 'price': 10,
                     'value': 301.68}
                ]
            )
        ]
    )
    def test_deposit(self, fiat_exchange, asset_allocation, market, amount,
                     holdings, monkeypatch):
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        blockfolio.deposit(amount)
        assert holdings_equal(blockfolio.holdings, holdings)

    def test_init_bad_asset_allocation(self, bad_asset_allocation, market):
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
    def test_holdings(self, fiat_exchange, asset_allocation, market, holdings,
                      monkeypatch):
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
    def test_value(self, fiat_exchange, asset_allocation, market, value,
                   monkeypatch):
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        assert blockfolio.value() == approx(value)
