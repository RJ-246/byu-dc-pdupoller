#!/bin/bash
token=$(openssl rand -base64 40)
echo "ADMIN_TOKEN=$token" >> ./.env