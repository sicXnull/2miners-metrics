#!/bin/bash
exec python3 /assets/main.py &
sleep 5
exec python3 /assets/2miners.py &
sleep 5
exec python3 /assets/jsonexporter.py
