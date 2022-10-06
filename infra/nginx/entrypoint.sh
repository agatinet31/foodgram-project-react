#!/bin/sh

certbot certonly -n -d example.com,www.example.com \
  --standalone --preferred-challenges http --email example@gmail.com --agree-tos --expand

/usr/sbin/crond -f -d 8 &

/usr/sbin/nginx -g "daemon off;"
