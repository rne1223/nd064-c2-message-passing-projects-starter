# Base image for app to speed up image builds
FROM python:3.9

WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY base_requirements.txt base_requirements.txt
RUN pip install -r base_requirements.txt
