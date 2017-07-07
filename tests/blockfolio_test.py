from .context import diversifiedblockfolio as dibl
import pytest


class TestBlockfolio(object):
    def test_init(self):
        # don't specify a fiat currency at all, expect a ValueError
        with pytest.raises(ValueError):
            b = dibl.Blockfolio({})

        # specify a fiat currency which is supported
        fiat_currency = "USD"
        b = dibl.Blockfolio({'fiat_symbol': fiat_currency})
        assert b.fiat_symbol == fiat_currency
