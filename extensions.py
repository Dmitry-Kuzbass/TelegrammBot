import requests
import json
from config import keys
class ConvertionException(Exception):
    pass
class CriptoConverter:
    @staticmethod
    def get_price(quote, base, amount):
        quote, base = quote.lower(), base.lower()
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        quote_ticker, base_ticker = keys[quote], keys[base]

        r = requests.get(f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={quote_ticker},&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[quote]][keys[base]]
        total_base *= amount
        return total_base