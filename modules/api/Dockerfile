FROM rne1223/udaconnect-base:v1.0.0

WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

EXPOSE 5000

# RUN pip install ptvsd
# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000
CMD ["flask", "run", "--host", "0.0.0.0"]