FROM rne1223/udaconnect-base:v1.0.1

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .

CMD python3 ./app/main.py 