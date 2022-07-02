FROM python:3.10

RUN apt-get update

RUN apt-get install -y --no-install-recommends

WORKDIR /The-Lottery-App

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /The-Lottery-App

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
