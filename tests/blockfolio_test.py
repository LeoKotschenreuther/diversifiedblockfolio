import coinmarketcap
from .context import diversifiedblockfolio as diblo
import pytest


@pytest.fixture
def market():
    return coinmarketcap.Market()


class TestBlockfolio(object):
    def test_init(self, market):
        # a holding in the fiat exchange with a negative amount
        fiat_exchange = {'holdings': [{'symbol': 'BTC', 'amount': -1}]}
        with pytest.raises(ValueError):
            blockfolio = diblo.Blockfolio(fiat_exchange, market)

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
    def test_value(self, monkeypatch, value, fiat_exchange, market):
        def mock_ticker(currency="", **kwargs):
            return [
                {'symbol': 'BTC', 'price_usd': '2499.98'},
                {'symbol': 'ETH', 'price_usd': '239.94'}
            ]

        # no holdings specified in the fiat exchange
        monkeypatch.setattr(market, 'ticker', mock_ticker)
        blockfolio = diblo.Blockfolio(fiat_exchange, market)
        assert blockfolio.value() == value
