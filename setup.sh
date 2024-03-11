#!/bin/bash

apt-get update
apt-get install systemctl -y
apt-get install cron -y
systemsctl enable cron
systemctl start cron
echo "* * * * * bash /root/" | crontab -
