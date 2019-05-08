FROM python:3.7-slim

RUN useradd -r apprunner

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app/
RUN pip install .


CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "nivo_api.app:app"]
