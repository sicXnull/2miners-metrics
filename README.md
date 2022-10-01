# 2miners-metrics


-A Prometheus Exporter for the following
- https://2miners.com
- HiveOS Exporter
- Price Converter (Coin value to BTC/USD)
- HiveOS Wattage to USD Conversion
- Exporter for above conversions

-Required:
- Cryptocompare API Key (Free will be fine)
- Hive OS API Key

Metrics used for Grafana Dash which is also linked 

![image](https://user-images.githubusercontent.com/31908995/148861960-10505a0b-0de8-44ad-92e2-dde09784ea4c.png)


# Developing

- Build the image:

```sh
docker build -t 2miners-metrics:latest .
```
- Rename .env-example to .env, enter ENV variables:

```
MINING_ADDRESS=<2miners Mining Address>
RIG_NAME=<2miners Mining Name>
IP_ADDRESS=<Machine IP>
WALLET_ADDY=<For Blockchain.info>
FARM_ID=<HiveOS Farm id>
ELECTRIC_COST=<cents 12=0.12>
HIVE_KEY=<HiveOS API Key>
CC_KEY=<CryptoCompare API key>
EXPLORER_URL=blockchain.info/balance?active=
HIVE_URL=api2.hiveos.farm
MINING_URL=<coin>.2miners.com/api/accounts
CURRENCY=USD
BASE_COIN=BTC
MINING_COIN=
MINING_DECIMALS=
APP_PORT=8888
EXPORTER_PORT=9877
```

- Run it while listening on port 9877

```sh
docker run -d --env-file ./.env -p 9877:9877 -p 8888:8888 -v /opt/2miners-metrics/:/home --name 2miners-metrics --restart=always 2miners metrics:latest
```
```
