#!/bin/bash
token=$(openssl rand -base64 25)
echo "ADMIN_TOKEN=$token" >> ./.env