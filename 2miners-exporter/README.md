# 2miners-exporter

A prometheus exporter for <https://2miners.com/>


# Developing

- Build the image:

```sh
docker build -t 2miners-exporter:latest .
```

- Run it while listening on port 9877:

```sh
docker run -d -p 9877:9877 --name 2miners-exporter --restart=always -e RIG-NAME='Reported Rig Name' -e MINING-ADDRESS='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' 2miners-exporter:latest
```

- Run it interactively:

```sh
docker run --rm -it --entrypoint=/bin/sh -p 9877:9877 -e MINING-ADDRESS='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' -v ${PWD}:/opt/2miners-exporter 2miners-exporter:latest
```

- Then to launch:

```sh
python3 2miners.py
```
