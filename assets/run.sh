#!/bin/bash
exec /etc/init.d/apache2 start &
sleep 5
exec python3 /assets/2miners.py &
sleep 5
exec python3 /assets/main.py &
sleep 300
exec python3 /assets/jsonexporter.py
