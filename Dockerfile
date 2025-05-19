# Dockerfile

FROM python:3.11-slim

MAINTAINER "Alfonsos Kotsios" 

WORKDIR /app

COPY . .

RUN apt update -y
RUN apt upgrade -y

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt




CMD ["python","-u" ,"main.py"]
