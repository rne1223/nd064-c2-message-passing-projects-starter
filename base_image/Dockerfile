# Base image for app to speed up image builds
FROM python:3.7-slim-buster

WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev build-base
COPY base_requirements.txt base_requirements.txt
RUN pip install -r base_requirements.txt
