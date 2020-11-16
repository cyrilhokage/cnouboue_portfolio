# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


# create root directory for our project in the container
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/cnouboue_portfolio
RUN mkdir -p /opt/app/pip_cache

# Copy the current directory contents into the container at 
COPY . /opt/app/cnouboue_portfolio/
COPY .pip_cache /opt/app/pip_cache/

# Set the working directory to /opt/app
WORKDIR /opt/app/cnouboue_portfolio

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app/cnouboue_portfolio

EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/opt/app/cnouboue_portfolio/start-server.sh"]