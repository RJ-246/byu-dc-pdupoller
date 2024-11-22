#!/bin/bash

apt-get update
apt-get install systemd cron python3 python3-pip python3-venv -y
python3 -m venv /root/venv
systemctl enable cron
systemctl start cron
curl -o /root/modbus.py https://raw.githubusercontent.com/RJ-246/byu-dc-pdupoller/main/modbus.py
curl -o /root/requirements.txt https://raw.githubusercontent.com/RJ-246/byu-dc-pdupoller/main/requirements.txt
/root/venv/bin/pip3 install -r /root/requirements.txt
chmod +x /root/modbus.py
export "INFLUX_TOKEN=$ADMIN_TOKEN"
echo "* * * * * /root/venv/bin/python3 /root/modbus.py" > /root/crontab.txt
crontab /root/crontab.txt