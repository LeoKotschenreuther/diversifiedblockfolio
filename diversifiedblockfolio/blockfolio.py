KEY_FIAT_SYMBOL = 'fiat_symbol'


class Blockfolio:

    def __init__(self, attribute_dict):
        if KEY_FIAT_SYMBOL not in attribute_dict:
            raise ValueError("Missing key in the passed dict: {}".
                             format(KEY_FIAT_SYMBOL))
            return
        self.fiat_symbol = attribute_dict[KEY_FIAT_SYMBOL]
