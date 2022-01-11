# Telegraf inputs

Forked from - https://github.com/jouir/mining-dashboards/tree/main/telegraf

## HiveOS API

### Create token

On your [account](https://the.hiveos.farm/account) page, go to *Authentication Tokens*, search for *Personal Tokens* and
create one for `telegraf`:

![image](https://user-images.githubusercontent.com/31908995/148863307-f542ed77-e9dc-484b-8b77-660f075acf41.png)

Enter your 2FA code if needed:

![image](https://user-images.githubusercontent.com/31908995/148863321-8f62fb78-e8c0-448d-abb1-1902da723f5c.png)

Click on *Show*:

![image](https://user-images.githubusercontent.com/31908995/148863337-d922cdc0-b6b1-499a-8d58-c645764913a4.png)

And add this value to the `HIVEOS_TOKEN` environment variable (see *Quickstart* section in the [README](../README.md)).

### Create Telegraf configuration

```
cd hiveos
sudo apt install python3-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
read -s HIVEOS_TOKEN
export HIVEOS_TOKEN
python3 generate.py --verbose
unset HIVEOS_TOKEN
mv hiveos.conf ../
```
