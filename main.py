import json, requests
import time
import os

wallet_address = os.environ.get('WALLET-ADDY')
hive_farm_id = os.environ.get('FARM-ID')
electric = float(os.environ.get('ELECTRIC-COST'))
hive_key = os.environ.get('HIVE-KEY')

class PriceStats:
    def __init__(self):
        self.currency = 'USD'
        self.ticker = 'ETH'
        self.wallet_type = 'BTC'
        self.hive_headers = {"Authorization": f"Bearer {hive_key}"}

        self.endpoints = {
            'price': f'',
            '2miners': f'https://eth.2miners.com/api/accounts/{wallet_address}',
            'balance': f'https://blockchain.info/balance?active={wallet_address}',
            'hive': f'https://api2.hiveos.farm/api/v2/farms/{hive_farm_id}/stats'
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
                self.results.update({f"unpaid_balance_{self.ticker}": round(resp['stats']['balance'] / 1000000000 if self.ticker == "ETH" else 100000000, 5)})
                self.results.update({f"unpaid_balance_{self.currency}": round(self.results[f"unpaid_balance_{self.ticker}"] * self.results[f"price_{self.ticker}"], 2)})
                self.results.update({f"unpaid_last_24_hr_{self.ticker}": round(resp['sumrewards'][2]['reward'] / 1000000000 if self.ticker == "ETH" else 100000000, 5)})
                self.results.update({f"unpaid_last_24_hr_{self.currency}": round(self.results[f"unpaid_last_24_hr_{self.ticker}"] * self.results[f"price_{self.ticker}"], 2)})

            elif key == "balance":
                resp = requests.get(self.endpoints[key]).json()
                self.results.update({f'wallet_{key}_{self.wallet_type}': round(resp[wallet_address]['final_balance'] / 100000000, 5)})
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
        return f'https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms={currency}'


if __name__ == '__main__':
    execute = PriceStats()
    running = True
    while running:
        execute.extractData()
        time.sleep(60)