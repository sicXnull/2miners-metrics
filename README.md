# 2miners-metrics

There are probably better ways to do this, but this worked for me, especially since the info 2Miners provides isn't the best. That said, this setup is still kind of hacked together, please send over pull requests if you use this and modify it in a positive way 

-Consists of the following
- A Prometheus Exporter for <https://2miners.com/>
- Price Converter (Eth value to BTC/USD)
- HiveOS Wattage to USD Conversion
- Exporter for above conversions
- Telegraf/InfluxDB HiveOS 

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

- Run it while listening on port 9877:

```sh
docker run -d -p 9877:9877 -p 9977:9977 -p 8800:80 --name 2miners-exporter --restart=always 2miners-metrics:latest
```
```

- 2Miners Exporter Port - 9877
- Conversion Exporter Port - 9977
- Json Host - 9878
