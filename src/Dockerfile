#FROM gcr.io/turing-230020/turing_challenge_db_image:0.1
FROM 93462a368b04
MAINTAINER Malisa Ncube <malisa.n@turing.com>

RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    supervisor \
    wget \
    apt-transport-https \
    lsb-release \
    ca-certificates \
    less

RUN apt-get update && apt-get install -y python3-pip python3-dev libmysqlclient-dev && apt-get clean

# Project Files and Settings
ARG PROJECT=turing_backend
ARG PROJECT_DIR=/var/www/${PROJECT}

RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
ADD requirements.txt $PROJECT_DIR
RUN pip3 install -r requirements.txt

ADD . $PROJECT_DIR

# Server
EXPOSE 8000
COPY turing-entrypoint.sh /turing-entrypoint.sh


ENTRYPOINT ["/turing-entrypoint.sh"]


