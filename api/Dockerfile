FROM python:3.7-slim

# create a user with a home dir. home dir is needed by pip cache.
RUN useradd -r -m apprunner

USER apprunner
ENV HOME=/home/apprunner
ENV PATH=$HOME/.local/bin:$PATH
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --user -r requirements.txt


COPY . /app/
RUN pip install --user .

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "nivo_api.app:app"]
