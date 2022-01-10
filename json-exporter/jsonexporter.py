"""JSONSTATS exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Info, Summary, Enum
import requests
import logging

addy = os.environ.get('IP-ADDRESS')

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=80, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds
        # Prometheus metrics to collect
        self.jsonstats_price_BTC = Gauge("jsonstats_price_BTC", "price_BTC")
        self.jsonstats_price_ETH = Gauge("jsonstats_price_ETH", "price_ETH")
        self.jsonstats_unpaid_balance_ETH = Gauge("jsonstats_unpaid_balance_ETH", "unpaid_balance_ETH")
        self.jsonstats_unpaid_balance_USD = Gauge("jsonstats_unpaid_balance_USD", "unpaid_balance_USD")
        self.jsonstats_unpaid_last_24_hr_ETH = Gauge("jsonstats_unpaid_last_24_hr_ETH", "unpaid_last_24_hr_ETH")
        self.jsonstats_unpaid_last_24_hr_USD = Gauge("jsonstats_unpaid_last_24_hr_USD", "unpaid_last_24_hr_USD")
        self.jsonstats_wallet_balance_BTC = Gauge("jsonstats_wallet_balance_BTC", "wallet_balance_BTC")
        self.jsonstats_wallet_balance_USD = Gauge("jsonstats_wallet_balance_USD", "wallet_balance_USD")
        self.jsonstats_power_cost_USD = Gauge("jsonstats_power_cost_USD", "power_cost_USD")
        self.jsonstats_mining_profitability = Gauge("jsonstats_mining_profitability", "mining_profitability")
        self.jsonstats_mining_profitability_percent = Gauge("jsonstats_mining_profitability_percent", "mining_profitability_percent")


    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        resp = requests.get(url=f"http://{addy}:9878/result.json")
        status_data = resp.json()

        # Update Prometheus metrics with application metrics
        self.jsonstats_price_BTC.set(status_data["price_BTC"])
        self.jsonstats_price_ETH.set(status_data["price_ETH"])
        self.jsonstats_unpaid_balance_ETH.set(status_data["unpaid_balance_ETH"])
        self.jsonstats_unpaid_balance_USD.set(status_data["unpaid_balance_USD"])
        self.jsonstats_unpaid_last_24_hr_ETH.set(status_data["unpaid_last_24_hr_ETH"])
        self.jsonstats_unpaid_last_24_hr_USD.set(status_data["unpaid_last_24_hr_USD"])
        self.jsonstats_wallet_balance_BTC.set(status_data["wallet_balance_BTC"])
        self.jsonstats_wallet_balance_USD.set(status_data["wallet_balance_USD"])
        self.jsonstats_power_cost_USD.set(status_data["power_cost_USD"])
        self.jsonstats_mining_profitability.set(status_data["mining_profitability"])
        self.jsonstats_mining_profitability_percent.set(status_data["mining_profitability_percent"])


def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    app_port = int(os.getenv("APP_PORT", "80"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9977"))

    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()