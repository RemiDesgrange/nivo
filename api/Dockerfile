FROM python:3.9-slim

# create a user with a home dir. home dir is needed by pip cache.
RUN useradd -r -m apprunner

USER apprunner
ENV HOME=/home/apprunner
ENV PATH=$HOME/.local/bin:$PATH
#COPY requirements.txt /app/
WORKDIR /app
#RUN pip install --user -r requirements.txt


COPY . /app/
RUN pip install --user .

ENV LOG_LEVEL=WARNING
ENV ENV=PROD

EXPOSE 9000
ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:9000", "nivo_api.app:app"]
