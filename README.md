# 2miners-metrics


-Consists of the following
- A Prometheus Exporter for <https://2miners.com/>
- Price Converter (Eth value to BTC/USD)
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
EXPLORER_URL=https://blockchain.info/balance?active=
HIVE_URL=https://api2.hiveos.farm
MINING_URL=https://<coin>.2miners.com/api/accounts
CURRENCY=USD
BASE_COIN=BTC
MINING_COIN=
MINING_DECIMALS=
```

- Run it while listening on port 9877,9977,8800 (8800 is optional, if you wish to see price converter json):

```sh
docker run -d --env-file ./.env -p 9877:9877 -v /opt/2miners-metrics/:/home --name 2miners-metrics --restart=always 2miners-metrics:latest
```
```

- 2Miners Exporter Port - 9877
- Conversion Exporter Port - 9977
- Json Host - 8800
