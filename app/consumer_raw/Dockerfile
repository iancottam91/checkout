FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY consumer_raw.py .

CMD ["python", "consumer_raw.py"]
