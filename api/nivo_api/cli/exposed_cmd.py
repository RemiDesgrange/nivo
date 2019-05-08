import json

import click
import requests
from sqlalchemy import func

from nivo_api.cli.database import create_schema_and_table, NivoSensorStation

import logging
from sqlalchemy.dialects.postgresql import insert

from nivo_api.cli.nivo_record_helper import import_nivo, download_nivo, check_last_nivo_doesnt_exist, get_last_nivo
from nivo_api.cli.setup import cli_setup
from nivo_api.core.db.connection import connection_scope
from nivo_api.settings import Config


@click.command()
def import_last_nivo_data():
    # setup
    # get http://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo/lastNivo.js
    # get last nivo data if needed
    # process it
    # import it.
    cli_setup()
    last_nivo = get_last_nivo()
    if check_last_nivo_doesnt_exist(last_nivo):
        downloaded_nivo = download_nivo(last_nivo)
        import_nivo(downloaded_nivo)


@click.command()
def import_nivo_sensor_station():
    cli_setup()
    res = requests.get(f'{Config.METEO_FRANCE_NIVO_BASE_URL}/postesNivo.json')
    assert res.status_code == 200
    res.json()
    with connection_scope() as con:
        with con.begin():
            for feature in res.json()['features']:
                pointz = feature['geometry']
                pointz['coordinates'].append(int(feature['properties']['Altitude']))
                mf_id = feature['properties']['ID'] if feature['properties']['ID'] != '' else None
                ins = insert(NivoSensorStation).values(**{
                    'nss_name': feature['properties']['Nom'],
                    'nss_meteofrance_id': mf_id,
                    'the_geom': func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(pointz)), 4326)
                }).on_conflict_do_nothing(index_elements=['nss_name'])
                con.execute(ins)


@click.command()
def import_all_nivo_data():
    # setup
    # go through the meteofrance ftp
    # download all file (via http, better)
    # process it
    # import it
    pass


@click.command()
def import_last_bra():
    # setup, check if we have the massifs here : ftp://ftp.meteo.fr/FDPMSP/Pdf/BRA/massifs.json
    # list all folder from the FTP. get the last date
    # from the last date, get xml file for each of the region
    # process
    # import
    pass


@click.command()
def import_all_bra():
    # setup
    # list all xml files in ftp
    # process (download + post process)
    # import
    pass


@click.command()
def init_db():
    # create the table if not exist. Assume the db is already here.
    # the command is idem potent
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    create_schema_and_table()
