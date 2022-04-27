FROM nginx

RUN ["rm", "/etc/nginx/conf.d/default.conf"]
RUN ["ln", "-s", "/app/nginx/mysite_nginx.conf", "/etc/nginx/conf.d/"]
CMD ["nginx", "-g", "daemon off;"]