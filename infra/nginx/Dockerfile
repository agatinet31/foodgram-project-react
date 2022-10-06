FROM nginx:1.21.3-alpine

RUN apk add --no-cache certbot

COPY nginx/renew /etc/periodic/daily/renew

RUN chmod +x /etc/periodic/daily/renew

RUN mkdir /var/lib/certbot

COPY nginx/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY nginx/nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT [ "../entrypoint.sh" ]
