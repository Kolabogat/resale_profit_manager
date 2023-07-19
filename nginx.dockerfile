FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY mysite.conf /etc/nginx/conf.d/mysite.conf