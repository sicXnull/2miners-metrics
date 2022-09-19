import json, requests
import time
import os

wallet_address = os.environ.get('WALLET-ADDY')
hive_farm_id = os.environ.get('FARM-ID')
electric = float(os.environ.get('ELECTRIC-COST'))
hive_key = os.environ.get('HIVE-KEY')
cc_key = os.environ.get('CC-KEY')
explorer_url = os.environ.get('EXPLORER_URL')
mining_url = os.environ.get('MINING_URL')
hive_url = os.environ.get('HIVE_URL')
currency = os.environ.get('CURRENCY')
ticker = os.environ.get('MINING_COIN')
wallet_type = os.environ.get('BASE_COIN')
decimal = os.environ.get('MINING_DECIMALS')

class PriceStats:
    def __init__(self):
        self.currency = currency
        self.ticker = ticker
        self.wallet_type = wallet_type
        self.hive_headers = {"Authorization": f"Bearer {hive_key}"}
        self.decimal = int(f'1{"0"*decimal}')

        self.endpoints = {
            'price': f'',
            '2miners': f'{mining_url}/{wallet_address}',
            'balance': f'{explorer_url}{wallet_address}',
            'hive': f'{hive_url}/api/v2/farms/{hive_farm_id}/stats'
        }
        self.results = {}

    def extractData(self):

        for key in self.endpoints.keys():

            if key == "price":
                price_wallet = requests.get(self.priceURL(self.wallet_type, self.currency)).json()
                price_mining = requests.get(self.priceURL(self.ticker, self.currency)).json()
                self.results[f"{key}_{self.wallet_type}"] = price_wallet[self.currency]
                self.results[f"{key}_{self.ticker}"] = price_mining[self.currency]

            elif key == "2miners":
                resp = requests.get(self.endpoints[key]).json()
                self.results.update({f"unpaid_balance_{self.ticker}": round(resp['stats']['balance'] / self.decimal, 5)})
                self.results.update({f"unpaid_balance_{self.currency}": round(self.results[f"unpaid_balance_{self.ticker}"] * self.results[f"price_{self.ticker}"], 2)})
                self.results.update({f"unpaid_last_24_hr_{self.ticker}": round(resp['sumrewards'][2]['reward'] / self.decimal, 5)})
                self.results.update({f"unpaid_last_24_hr_{self.currency}": round(self.results[f"unpaid_last_24_hr_{self.ticker}"] * self.results[f"price_{self.ticker}"], 2)})

            elif key == "balance":
                resp = requests.get(self.endpoints[key]).json()
                self.results.update({f'wallet_{key}_{self.wallet_type}': round(resp[wallet_address]['final_balance'] / self.decimal, 5)})
                self.results.update({f'wallet_{key}_{self.currency}': round(self.results[f'wallet_{key}_{self.wallet_type}'] * self.results[f'price_{self.wallet_type}'], 2)})

            elif key == "hive":
                resp = requests.get(self.endpoints[key], headers=self.hive_headers).json()
                watts = resp['stats']['power_draw']
                self.results[f'power_cost_{self.currency}'] = round(self.powerConversion(watts), 2)
                self.results['mining_profitability'] = round(self.results[f'unpaid_last_24_hr_{self.currency}'] - self.results[f'power_cost_{self.currency}'], 2)
                self.results['mining_profitability_percent'] = round((self.results['mining_profitability'] / self.results[f'unpaid_last_24_hr_{self.currency}']) * 100, 2)

        with open('metrics.txt', 'w') as file:
            file.write(self.metrics_data)

        with open("result.json", 'w') as file:
            json.dump(self.results, file, indent=2)
        print(self.results)

    @property
    def metrics_data(self):
        lines = ""
        for key in self.results.keys():
            lines = f"{lines}{key} {self.results[key]}\n"
        return lines

    def powerConversion(self, wattage):
        # converts a given wattage to daily cost
        kwh = wattage * 24 / 1000  # 24 hrs
        cents = 100
        return kwh * electric / cents

    def priceURL(self, coin, currency):
        return f'https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms={currency}&api_key={cc_key}'


if __name__ == '__main__':
    execute = PriceStats()
    running = True
    while running:
        execute.extractData()
        time.sleep(300)
