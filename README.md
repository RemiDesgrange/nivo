# nivo

*!! WIP !!*

A portal to share and display meteofrance opendata.

## Idea

The idea of this portal is to share meteo france opendata because :

* We are skier, and checking the meteofrance web site _every_ day during winter is a PITA
* nivo data is not display bit it is still useful
* having history of the snow is super important.

We aim to display three type of data


# API

openapi, powered by python(3). Tested on python3.7. Normally should run on python3.6

## Dev

* clone
* `cd api`
* make a virtualenv (`pew`, `mkvirtualenv` or `virtualenv .venv && .venv/bin/activate`
* run `python app.py` it listen on http://localhost:5000
* you can `pip install -e .` if you want to use cli directly.
* To init the database, you can use the `init_db` cmd that comes if you run `pip install -e .`
* follow README.md in `api` folder for more


# Frontend

We are not web dev, PR appreciated if you are master of the css, lord of the js.

## Dev

* `cd frontend`
* `npm i`
* `npm run serve`


# Prod ?

Docker
