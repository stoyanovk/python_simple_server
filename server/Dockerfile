FROM python:3.11.3-bullseye

RUN pip3 install "pip>=20"

WORKDIR /work/server

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-deps
