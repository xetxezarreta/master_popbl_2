# pull official base image
FROM python:slim-buster

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
RUN mkdir /code
WORKDIR /code

# install requirements
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
