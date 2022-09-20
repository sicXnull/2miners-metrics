"""JSONSTATS exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Info, Summary, Enum
import requests
import logging

addy = os.environ.get('IP-ADDRESS')
base_coin = os.environ.get("BASE_COIN")
mining_coin = os.environ.get("MINING_COIN")
currency = os.environ.get("CURRENCY")

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=80, polling_interval_seconds=5):

        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds
        # Prometheus metrics to collect
        self.metrics = {
            f"jsonstats_price_{base_coin}": Gauge(f"jsonstats_price_{base_coin}", f"price_{base_coin}"),
            f"jsonstats_price_{mining_coin}": Gauge(f"jsonstats_price_{mining_coin}", f"price_{mining_coin}"),
            f"jsonstats_unpaid_balance_{mining_coin}": Gauge(f"jsonstats_unpaid_balance_{mining_coin}", f"unpaid_balance_{mining_coin}"),
            f"jsonstats_unpaid_balance_{currency}": Gauge(f"jsonstats_unpaid_balance_{currency}", f"unpaid_balance_{currency}"),
            f"jsonstats_unpaid_last_24_hr_{mining_coin}": Gauge(f"jsonstats_unpaid_last_24_hr_{mining_coin}", f"unpaid_last_24_hr_{mining_coin}"),
            f"jsonstats_unpaid_last_24_hr_{currency}": Gauge(f"jsonstats_unpaid_last_24_hr_{currency}", f"unpaid_last_24_hr_{currency}"),
            f"jsonstats_wallet_balance_{base_coin}": Gauge(f"jsonstats_wallet_balance_{base_coin}", f"wallet_balance_{base_coin}"),
            f"jsonstats_wallet_balance_{currency}": Gauge(f"jsonstats_wallet_balance_{currency}", f"wallet_balance_{currency}"),
            f"jsonstats_power_cost_{currency}": Gauge(f"jsonstats_power_cost_{currency}", f"power_cost_{currency}"),
            "jsonstats_mining_profitability": Gauge("jsonstats_mining_profitability", "mining_profitability"),
            "jsonstats_mining_profitability_percent": Gauge("jsonstats_mining_profitability_percent","mining_profitability_percent")

        }

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
        resp = requests.get(url=f"http://{addy}/result.json")
        status_data = resp.json()

        # Update Prometheus metrics with application metrics
        self.metrics[f"jsonstats_price_{base_coin}"].set(status_data[f"price_{base_coin}"])
        self.metrics[f"jsonstats_price_{mining_coin}"].set(status_data[f"price_{mining_coin}"])
        self.metrics[f"jsonstats_unpaid_balance_{mining_coin}"].set(status_data[f"unpaid_balance_{mining_coin}"])
        self.metrics[f"jsonstats_unpaid_balance_{currency}"].set(status_data[f"unpaid_balance_{currency}"])
        self.metrics[f"jsonstats_unpaid_last_24_hr_{mining_coin}"].set(status_data[f"unpaid_last_24_hr_{mining_coin}"])
        self.metrics[f"jsonstats_unpaid_last_24_hr_{currency}"].set(status_data[f"unpaid_last_24_hr_{currency}"])
        self.metrics[f"jsonstats_wallet_balance_{base_coin}"].set(status_data[f"wallet_balance_{base_coin}"])
        self.metrics[f"jsonstats_wallet_balance_{currency}"].set(status_data[f"wallet_balance_{currency}"])
        self.metrics[f"jsonstats_power_cost_{currency}"].set(status_data[f"power_cost_{currency}"])
        self.metrics[f"jsonstats_mining_profitability"].set(status_data["mining_profitability"])
        self.metrics[f"jsonstats_mining_profitability_percent"].set(status_data["mining_profitability_percent"])


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
