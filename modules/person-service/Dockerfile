FROM rne1223/udaconnect-base:v1.0.0

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# Installing debugger
# RUN pip install ptvsd
# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000