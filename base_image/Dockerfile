# Base image for app to speed up image builds
FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY main_requirements.txt main_requirements.txt
RUN pip install -r main_requirements.txt