import coinmarketcap
from .context import diversifiedblockfolio as diblo
import pytest
from pytest import approx


@pytest.fixture(params=[
    [],
    [{}],
    [{'symbol': ''}],
    [{'symbol': 'BTC'}],
    [{'symbol': 'BTC', 'target_weight': -1}],
    [{'symbol': 'BTC', 'target_weight': 0}]

])
def bad_asset_allocation(request):
    return request.param


@pytest.fixture(params=[
    {'holdings': [{}]},
    {'holdings': [{'symbol': ''}]},
    {'holdings': [{'symbol': 'BTC', 'amount': -1}]}
])
def bad_fiat_exchange(request):
    return request.param


@pytest.fixture
def asset_allocation():
    return [
        {'symbol': 'BTC', 'target_weight': 1},
        {'symbol': 'ETH', 'target_weight': 1},
        {'symbol': 'LTC', 'target_weight': 1}
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

    def test_init_bad_fiat_exchange(self, bad_fiat_exchange, asset_allocation,
                                    market):
        with pytest.raises(ValueError):
            diblo.Blockfolio(bad_fiat_exchange, asset_allocation, market)

    def test_init_bad_asset_allocation(self, market, bad_asset_allocation):
        with pytest.raises(ValueError):
            diblo.Blockfolio({}, bad_asset_allocation, market)

    @pytest.mark.parametrize(
        'value, fiat_exchange', [
            (0, {}),
            (0, {'holdings': []}),
            (0, {'holdings': [{'symbol': 'BTC', 'amount': 0}]}),
            (1249.99, {'holdings': [{'symbol': 'BTC', 'amount': .5}]}),
            (1849.84, {'holdings': [
                {'symbol': 'BTC', 'amount': 0.5},
                {'symbol': 'ETH', 'amount': 2.5}
            ]})
        ]
    )
    def test_value(self, monkeypatch, value, fiat_exchange, asset_allocation,
                   market):
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        assert blockfolio.value() == approx(value)

    @pytest.mark.parametrize(
        'holdings, fiat_exchange', [
            (
                [{'symbol': 'BTC', 'amount': 0, 'price': 2499.98, 'value': 0},
                 {'symbol': 'ETH', 'amount': 0, 'price': 239.94, 'value': 0},
                 {'symbol': 'LTC', 'amount': 0, 'price': 49.57, 'value': 0}],
                {}
            ),
            (
                [{'symbol': 'BTC', 'amount': 0, 'price': 2499.98, 'value': 0},
                 {'symbol': 'ETH', 'amount': 3.4982, 'price': 239.94,
                    'value': 839.358108},
                 {'symbol': 'LTC', 'amount': 0, 'price': 49.57, 'value': 0}],
                {'holdings': [{'symbol': 'ETH', 'amount': 3.4982}]}
            ),
            (
                [{'symbol': 'BTC', 'amount': .4, 'price': 2499.98,
                    'value': 999.992},
                 {'symbol': 'ETH', 'amount': 3.4982, 'price': 239.94,
                    'value': 839.358108},
                 {'symbol': 'LTC', 'amount': 10.43, 'price': 49.57,
                    'value': 517.0151}],
                {'holdings': [
                    {'symbol': 'BTC', 'amount': .4},
                    {'symbol': 'ETH', 'amount': 3.4982},
                    {'symbol': 'LTC', 'amount': 10.43}
                ]}
            ),
        ]
    )
    def test_holdings(self, monkeypatch, holdings, fiat_exchange,
                      asset_allocation, market):
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, asset_allocation, market)
        blockfolio_holdings = blockfolio.holdings
        for index, blockfolio_holding in enumerate(blockfolio_holdings):
            holding = holdings[index]
            assert blockfolio_holding.keys() == holding.keys()
            for key in blockfolio_holding.keys():
                if type(blockfolio_holding[key]) == float:
                    assert blockfolio_holding[key] == approx(holding[key])
                else:
                    assert blockfolio_holding[key] == holding[key]
