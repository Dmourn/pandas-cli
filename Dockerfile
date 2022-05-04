FROM debian:unstable-slim

RUN apt update && apt upgrade -y 
RUN apt install -y python3 python3-pip python3-dev python3-venv && mkdir /test

WORKDIR /test

COPY ./data data
COPY ./requirements.txt requirements.txt
COPY ./dev-requirements.txt dev-requirements.txt
COPY  ./pandas_cli pandas_cli 
COPY ./setup.py setup.py
COPY ./test test
COPY ./noxfile.py noxfile.py

RUN bash -c "python3 -m venv /test/.env && source .env/bin/activate && pip install -U pip && pip install nox"

ENTRYPOINT ["bash", "-c", "source .env/bin/activate && nox "]

