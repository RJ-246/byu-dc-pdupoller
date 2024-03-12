#!/bin/bash
token = openssl rand -base64 25

echo $token

echo "ADMIN_TOKEN=$token"