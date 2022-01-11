# 2miners-metrics

There is probably better ways to do this, but this worked for me, especially since the info 2Miners provides isn't the best. 

-Consists of the following
- A Prometheus Exporter for <https://2miners.com/>
- Price Converter (Eth value to BTC/USD)
- HiveOS Wattage to USD Conversion
- Exporter for above conversions
- Telegraf/InfluxDB HiveOS 

Metrics used for Grafana Dash which is also linked 

![image](https://user-images.githubusercontent.com/31908995/148860999-abdef56a-e865-41d5-b390-21c7e8c92ee5.png)


## ENV Variables
- 2miners-exporter

```sh
RIG-NAME= <2Miners Rig Name>
MINING-ADDRESS= <BTC/ETH Mining Address>
```
- Price/Power Converter
```sh
WALLET-ADDY=<BTC/ETH Mining Address>
FARM-ID=<Hive-OS Farm ID>
ELECTRIC-COST=<CENTS>
HIVE-KEY=<HiveOS API Key>
```
- Converter-Exporter

```sh
IP-ADDRESS=
```

## Running the app


```sh
cd /opt
git clone https://github.com/sicXnull/2miners-metrics.git
```

```sh
docker-compose up -d
```

- 2Miners Exporter Port - 9877
- Conversion Exporter Port - 9977
- Json Host - 9878
