FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y make python3-pip python3.5

RUN mkdir /game_server

COPY game_server/* /game_server/
COPY requirements/* /game_server/requirements/
COPY Makefile /game_server/

EXPOSE 8888

# relink python3 and pip3 to common python aliases for convenience
RUN ln -sf /usr/bin/python3.5 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip

WORKDIR /game_server
RUN make requirements.game_server

CMD ["make", "help"]
