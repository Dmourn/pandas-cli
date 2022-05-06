FROM debian:unstable-slim

RUN apt update && apt upgrade -y 
RUN apt install -y less python3 python3-pip python3-dev python3-venv && mkdir /test

WORKDIR /test

COPY ./data data
COPY ./requirements.txt requirements.txt
COPY ./dev-requirements.txt dev-requirements.txt

RUN bash -c "python3 -m venv /test/.env && source .env/bin/activate && pip install -U pip && pip install -r dev-requirements.txt"

COPY ./setup.py setup.py
COPY  ./pandas_cli pandas_cli 
COPY ./test test
COPY ./noxfile.py noxfile.py

RUN ["bash", "-c", "source .env/bin/activate && nox "]
RUN ["bash", "-c", "source .env/bin/activate && pip install ./"]
# ENTRYPOINT ["bash", "-c", "source .env/bin/activate && bash -i "]
ENTRYPOINT ["bash", "-c", "source .env/bin/activate && pandas-cli && bash -i || bash -i "]

