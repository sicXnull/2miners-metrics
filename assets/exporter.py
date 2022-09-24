import time, json, requests, os
from prometheus_client import start_http_server, Gauge, Info, Summary, Enum
import requests
from logger import logger

ip_addy = os.environ.get('IP_ADDRESS')
base_coin = os.environ.get('BASE_COIN')
mining_coin = os.environ.get('MINING_COIN')
currency = os.environ.get("CURRENCY")
addy = os.environ.get('MINING_ADDRESS')
name = os.environ.get('RIG_NAME')
hive_url = os.environ.get('HIVE_URL')
wallet_address = os.environ.get('WALLET_ADDY')
hive_farm_id = os.environ.get('FARM_ID')
electric = float(os.environ.get('ELECTRIC_COST'))
hive_key = os.environ.get('HIVE_KEY')
cc_key = os.environ.get('CC_KEY')
explorer_url = os.environ.get('EXPLORER_URL')
mining_url = os.environ.get('MINING_URL')
decimal = int(os.environ.get('MINING_DECIMALS'))
polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "300"))
app_port = int(os.getenv("APP_PORT", "80"))
exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

class PromExporter:
	
	def __init__(self):
		"""
		Prometheus Exporter Object
		
		executeProcess() - Main Process Loop
		fetchData() - Aggregates all Data
		getGauges() - Initializes the Prometheus Collectors
		setGauges() - Sets the Gauges with the Aggregate Data
		writeFile() - Writes response Data to json file for apache to serve
		"""
		logger.info(f"Init PromExporter")
		
		self.currency = currency
		self.ticker = mining_coin
		self.wallet_type = base_coin
		self.hive_headers = {"Authorization": f"Bearer {hive_key}"}
		self.decimal = int(f'1{"0" * decimal}')
		self.getGauges()
		
		self.endpoints = {
			'price': f'',
			'2miners': f'{mining_coin.lower()}.2miners.com/api/accounts/{addy}',
			'balance': f'{explorer_url}{wallet_address}',
			'hive': f'{hive_url}/api/v2/farms/{hive_farm_id}/stats'
		}
		
		self.data = {
			'price': {},
			'2miners': {},
			'balance': {},
			'hive': {}
		}
		
	
	def executeProcess(self):
		
		# Metrics Loop
		logger.info(f"Beginning Running Loop")
		while True:
			self.fetchData()
			self.setGauges()
			self.writeFile()
			logger.info(f"Sleeping for  : {polling_interval_seconds}(s)")
			time.sleep(polling_interval_seconds)
		
	
	def fetchData(self):
		logger.info(f"Begin Data Extraction..")
		for key in self.endpoints.keys():
			
			if key == "price":
				logger.info(f"Hitting cryptoCompare for Price Data")
				
				self.data[key][f"{key}_{self.wallet_type}"] = requests.get(
					self.priceURL(self.wallet_type, self.currency)).json()
				
				self.data[key][f"{key}_{self.ticker}"] = requests.get(self.priceURL(self.ticker, self.currency)).json()
				
			
			elif key == "balance":
				logger.info(f"Hitting Explorer for Wallet Balance Data")
				
				self.data[key] = requests.get(f"https://{self.endpoints[key]}").json()
				
				self.data[key].update({f'wallet_{key}_{self.wallet_type}': round(
					self.data[key][wallet_address]['final_balance'] / self.decimal, 5)})
	
				self.data[key].update({f'wallet_{key}_{self.currency}': round(
					self.data[key][f'wallet_{key}_{self.wallet_type}'] *
					self.data['price'][f'price_{self.wallet_type}'][currency], 2)})
			
			elif key == "hive":
				logger.info(f"Hitting Hive for Farm Stats")
				
				resp = requests.get(f"https://{self.endpoints[key]}", headers=self.hive_headers).json()
				self.data[key] = resp
				
				self.data[key][f'power_cost_{self.currency}'] = round(
					self.powerConversion(self.data[key]['stats']['power_draw']), 2)
				
				self.data[key]['mining_profitability'] = round(
					self.data['2miners'][f'unpaid_last_24_hr_{self.currency}'] - self.data[key][
						f'power_cost_{self.currency}'], 2)
				
				self.data[key]['mining_profitability_percent'] = \
					round((self.data[key]['mining_profitability'] / self.data['2miners'][f'unpaid_last_24_hr_{self.currency}']) * 100,2)
			
			elif key == "2miners":
				logger.info(f"Hitting 2Miners for Account Stats Data")
				
				self.data[key] = requests.get(f"https://{self.endpoints[key]}").json()
				
				self.data[key].update(
					{f"unpaid_balance_{self.ticker}": round(self.data[key]['stats']['balance'] / self.decimal, 5)})
				
				self.data[key].update({f"unpaid_balance_{self.currency}": round(
					self.data[key][f"unpaid_balance_{self.ticker}"] * self.data['price'][f"price_{self.ticker}"][
						currency], 2)})
				
				self.data[key].update({f"unpaid_last_24_hr_{self.ticker}": round(
					self.data[key]['sumrewards'][2]['reward'] / self.decimal, 5)})
				
				self.data[key].update({f"unpaid_last_24_hr_{self.currency}": round(
					self.data[key][f"unpaid_last_24_hr_{self.ticker}"] * self.data['price'][f"price_{self.ticker}"][
						currency], 2)})
		
		logger.info(f"Data Extraction Complete")
	
	def getGauges(self):
		self.gauges = {
			f"jsonstats_price_{base_coin}": Gauge(f"jsonstats_price_{base_coin}", f"price_{base_coin}"),
			
			f"jsonstats_price_{mining_coin}": Gauge(f"jsonstats_price_{mining_coin}", f"price_{mining_coin}"),
			
			f"jsonstats_unpaid_balance_{mining_coin}": Gauge(f"jsonstats_unpaid_balance_{mining_coin}",
														f"unpaid_balance_{mining_coin}"),
			
			f"jsonstats_unpaid_balance_{currency}": Gauge(f"jsonstats_unpaid_balance_{currency}",
														f"unpaid_balance_{currency}"),
			
			f"jsonstats_unpaid_last_24_hr_{mining_coin}": Gauge(f"jsonstats_unpaid_last_24_hr_{mining_coin}",
																f"unpaid_last_24_hr_{mining_coin}"),
			
			f"jsonstats_unpaid_last_24_hr_{currency}": Gauge(f"jsonstats_unpaid_last_24_hr_{currency}",
																f"unpaid_last_24_hr_{currency}"),
			
			f"jsonstats_wallet_balance_{base_coin}": Gauge(f"jsonstats_wallet_balance_{base_coin}",
																f"wallet_balance_{base_coin}"),
			
			f"jsonstats_wallet_balance_{currency}": Gauge(f"jsonstats_wallet_balance_{currency}",
																f"wallet_balance_{currency}"),
			
			f"jsonstats_power_cost_{currency}": Gauge(f"jsonstats_power_cost_{currency}", f"power_cost_{currency}"),
			
			"jsonstats_mining_profitability": Gauge("jsonstats_mining_profitability", "mining_profitability"),
			
			"jsonstats_mining_profitability_percent": Gauge("jsonstats_mining_profitability_percent",
															"mining_profitability_percent"),
			
			"miner_dayreward_number": Gauge("miner_dayreward_number", "24hnumreward"),
			
			"miner_dayreward": Gauge("miner_dayreward", "24hreward"),
			
			"miner_currentHashrate": Gauge("miner_hashrate_current", "currentHashrate"),
			
			"miner_reportedHashrate": Gauge("miner_hashrate_reported", "reportedHashrate"),
			
			"miner_current_luck": Gauge('miner_current_luck', 'currentLuck'),
			
			"miner_averageHashrate": Gauge('miner_averageHashrate', 'averageHashrate'),
			
			"miner_payments_total": Gauge('miner_payments_total', 'paymentsTotal'),
			
			"miner_round_shares": Gauge('miner_round_shares', 'roundShares'),
			
			"miner_shares_stale": Gauge('miner_shares_stale', 'sharesStale'),
			
			"miner_shares_valid": Gauge('miner_shares_valid', 'sharesValid'),
			
			"miner_current_balance": Gauge('miner_current_balance', 'stats_balance')
			
		}
	
	def setGauges(self):
		logger.info(f"Setting Gauge Data")
		self.gauges[f"jsonstats_price_{base_coin}"].set(self.data['price'][f"price_{base_coin}"][currency])
		
		self.gauges[f"jsonstats_price_{mining_coin}"].set(self.data['price'][f"price_{mining_coin}"][currency])
		
		self.gauges[f"jsonstats_wallet_balance_{base_coin}"].set(self.data['balance'][f"wallet_balance_{base_coin}"])
		
		self.gauges[f"jsonstats_wallet_balance_{currency}"].set(self.data['balance'][f"wallet_balance_{currency}"])
		
		self.gauges[f"jsonstats_power_cost_{currency}"].set(self.data['hive'][f"power_cost_{currency}"])
		
		self.gauges[f"jsonstats_mining_profitability"].set(self.data['hive']["mining_profitability"])
		
		self.gauges[f"jsonstats_mining_profitability_percent"].set(self.data['hive']["mining_profitability_percent"])
		
		self.gauges[f"jsonstats_unpaid_balance_{mining_coin}"].set(
			self.data['2miners'][f"unpaid_balance_{mining_coin}"])
		
		self.gauges[f"jsonstats_unpaid_balance_{currency}"].set(self.data['2miners'][f"unpaid_balance_{currency}"])
		
		self.gauges[f"jsonstats_unpaid_last_24_hr_{mining_coin}"].set(
			self.data['2miners'][f"unpaid_last_24_hr_{mining_coin}"])
		
		self.gauges[f"jsonstats_unpaid_last_24_hr_{currency}"].set(
			self.data['2miners'][f"unpaid_last_24_hr_{currency}"])
		
		self.gauges[f"miner_dayreward_number"].set(self.data['2miners']["24hnumreward"])
		
		self.gauges[f"miner_dayreward"].set(self.data['2miners']["24hreward"])
		
		self.gauges[f"miner_currentHashrate"].set(self.data['2miners']["currentHashrate"])
		
		self.gauges[f"miner_reportedHashrate"].set(self.data['2miners']['workers'][f'{name}']['rhr'])
		
		self.gauges[f"miner_current_luck"].set(self.data['2miners']["currentLuck"])
		
		self.gauges[f"miner_averageHashrate"].set(self.data['2miners']["hashrate"])
		
		self.gauges[f"miner_payments_total"].set(self.data['2miners']["paymentsTotal"])
		
		self.gauges[f"miner_round_shares"].set(self.data['2miners']["roundShares"])
		
		self.gauges[f"miner_shares_valid"].set(self.data['2miners']["sharesValid"])
		
		self.gauges[f"miner_shares_stale"].set(self.data['2miners']["sharesStale"])
		
		self.gauges[f"miner_current_balance"].set(self.data['2miners']['stats']['balance'])
	
	def powerConversion(self, wattage):
		# converts a given wattage to daily cost
		kwh = wattage * 24 / 1000  # 24 hrs
		cents = 100
		return kwh * electric / cents
	
	def priceURL(self, coin, currency):
		return f'https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms={currency}&api_key={cc_key}'
	
	def writeFile(self):
		logger.info(f"Writing Metrics Data")
		
		with open("/var/www/html/results.json", 'w') as file:
			json.dump(self.data, file, indent=4)
			
		logger.info("Data Write Complete")


def main():
	# Main entry point
	
	#init Prom Exporter Object
	exporter = PromExporter()
	
	# start up prom http server for gauge data
	start_http_server(exporter_port)
	
	# trigger process
	exporter.executeProcess()

if __name__ == "__main__":
	main()