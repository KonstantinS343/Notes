FROM python:3.11.4

WORKDIR /notes

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /notes/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /notes/requirements.txt

COPY . .

RUN chmod a+x scripts/*.sh