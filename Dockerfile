FROM python:3.8

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt .

RUN apt-get update

RUN pip install -r requirements.txt

COPY . .
RUN pip3 install -e /app

RUN mkdir /app/data

EXPOSE 5000

CMD ["python", "bin/run.py"]
