
FROM nginx:latest

#EXPOSE 80

ADD nginx.conf /etc/nginx/nginx.conf
# Nginx will listen on this port

# Remove the default config file that
# /etc/nginx/nginx.conf includes
#RUN rm /etc/nginx/conf.d/default.conf
# We copy the requirements file in order to install
# Python dependencies
#ADD nginx.conf /etc/nginx/nginx.conf