FROM redis
MAINTAINER Ron Hay "heyronhay@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev build-essential

# Copy redis config file
COPY redis.conf /etc/redis/redis.conf
# Expose redis port
EXPOSE 6379

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["/bin/bash", "start.sh"]
