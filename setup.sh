#!/bin/bash

apt-get update
apt-get install systemctl cron python3 python3-pip -y
systemctl enable cron
systemctl start cron
curl -o /root/modbus.py https://raw.githubusercontent.com/RJ-246/byu-dc-pdupoller/main/modbus.py
curl -o /root/requirements.txt https://raw.githubusercontent.com/RJ-246/byu-dc-pdupoller/main/requirements.txt
pip3 install -r /root/requirements.txt
echo "* * * * * python3 /root/modbus.py" | crontab -
