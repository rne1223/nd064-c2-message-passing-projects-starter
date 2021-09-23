FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Installing debugger
RUN pip install ptvsd

# EXPOSE 5000
# ENV FLASK_APP=wsgi.py

COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]

CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000