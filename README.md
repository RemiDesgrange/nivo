# Nivo

*!! WIP !!*

A portal to share and display meteofrance opendata.

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FRemiDesgrange%2Fnivo%2Fbadge&style=flat)](https://actions-badge.atrox.dev/RemiDesgrange/nivo/goto)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0d05d913551f4ecab75cc042cdb4ae9f)](https://www.codacy.com/app/RemiDesgrange/nivo)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/0d05d913551f4ecab75cc042cdb4ae9f)](https://www.codacy.com/app/RemiDesgrange/nivo)
[![Requirements Status](https://requires.io/github/RemiDesgrange/nivo/requirements.svg?branch=master)](https://requires.io/github/RemiDesgrange/nivo/requirements/?branch=master)
[![black](https://badgen.net/badge/code%20style/black/000)](https://github.com/psf/black)

## Idea

The idea of this portal is to share meteo france opendata because :

*  We are skier, and checking the meteofrance web site *every* day during winter is a PITA
*  nivo data is not display bit it is still useful
*  having history of the snow is super important.

We aim to display three type of data.

## Run it locally

Make an entry in `/etc/hosts`
```
127.0.1.1 nivo.test api.nivo.test
```

```
docker-compose up -d
```

Go to `http://nivo.test` in your browser

## API

openapi, powered by python(3). Tested on python3.7 and 3.8 and 3.9.

### Dev

See [README.md](api) in api folder

*  Clone
*  `cd api`
*  Make a virtualenv (`pew`, `mkvirtualenv` or `virtualenv .venv && .venv/bin/activate`
* `pip install -r requirements.txt -r dev-requirements.txt`
*  Run `python app.py` it listen on `http://localhost:5000`
*  You can `pip install -e .` if you want to use cli directly.
*  To init the database, you can use the `init_db` cmd that comes if you run `pip install -e .`

If you just want to run it for frontend dev :
```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

in the `api/` folder

## Frontend

We are not web dev, PR appreciated if you are master of the css, lord of the js.

### Dev

See [README.md](frontend) in frontend folder

*  `cd frontend`
*  `npm i`
*  `npm run serve`

## Prod

Docker. But it's quite standard python. So you can run it with anything that can run WSGI server
(Apache, gunicorn, uwsgi, waitress, etc...).

