# Nivo API

Nivo api consist of a little wrapper to serve OpenData from meteo france with an api. 
There is not limiter, no auth, no restriction whatsoever.

## Start with the api

You'll need data from meteo france. Be aware that downloading the whole dataset is quite long, 
both for nivo data and for BRA. So grab the last one if you develop (or a particular one).


### Start the db with docker (+ the app)

This command will start the app and the db with port exposed. the app is started but we 
won't use it. You can kill it if you want.
```bash
docker-compose up -f docker-compose.dev.yml -f docker-compose.yml -d
```

### Setup dev env

*  Create a venv, via virtualenv or pew or whatever the tool you like
*  `cd api`
*  `pip install -r requirements.txt -r dev-requirements.txt`
*  `pip install -e .` 

### Import script

Now that the app and the db is up, you'll need data from meteofrance

```bash
# start with massif. Normaly with the standard conf it must work.
init_db
import_massifs 
import_last_bra
import_nivo_sensor_station
import_last_nivo_data
```

You can now start the app. Via `flask` cli or `gunicorn`

```bash
FLASK_APP=nivo_api.app:app flask run
# OR
gunicorn nivo_api.app:app
``` 

Be aware that flask web server is for local dev only, not for production use. Gunicorn is commonly used in production environment, but you can use Waitress, uwsgi, etc...

## Test

```bash
#launch the db. Ex:
docker-compose up -f docker-compose.dev.yml -f docker-compose.yml -d db
pytest
```

Tests use [pspec](https://pypi.org/project/pytest-pspec/). So you can see "rspec like" unit test. `pspec` config is in the `setup.cfg` file.

## Mypy

`Mypy` is a static type checker. It helps you detect inconsistencies in 
types.

```bash
mypy nivo_api
```

Configuration is also in `setup.cfg` file.
