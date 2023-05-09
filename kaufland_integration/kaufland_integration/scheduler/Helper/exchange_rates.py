import requests


class ExchangeRates:
    def get_currancy_rate(self,currency:str):
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}/?format=json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['rates'][0]['mid']
        else:
            return 0