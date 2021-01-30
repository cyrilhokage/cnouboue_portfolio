# Dockerfile
FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV enviroment='PRODUCTION'

# copy source and install dependencies
RUN mkdir -p /opt/app/cnouboue_portfolio

COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY . /opt/app/cnouboue_portfolio/

# Set the working directory to /opt/app/cnouboue_portfolio
WORKDIR /opt/app/cnouboue_portfolio

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --cache-dir /opt/app/cnouboue_portfolio/pip_cache
RUN chown -R www-data:www-data /opt/app/cnouboue_portfolio

# start server
EXPOSE 8020 80 443
STOPSIGNAL SIGTERM
CMD ["/opt/app/cnouboue_portfolio/start-server.sh"]