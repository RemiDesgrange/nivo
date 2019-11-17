import json
from contextlib import contextmanager
from datetime import datetime

import click
import geojson
import requests
from pkg_resources import resource_stream
from sqlalchemy import func, select

from nivo_api.cli.bra_record_helper.miscellaneous import (
    get_last_bra_date,
    get_bra_xml,
    get_bra_date,
    check_bra_record_exist,
)
from nivo_api.cli.bra_record_helper.persist import persist_bra, persist_massif
from nivo_api.cli.bra_record_helper.process import process_xml
from nivo_api.cli.database import create_schema_and_table

import logging
import logging.config
from sqlalchemy.dialects.postgresql import insert

from nivo_api.cli.flowcapt_record_helper import persist_flowcapt_station
from nivo_api.cli.nivo_record_helper import (
    import_nivo,
    download_nivo,
    check_nivo_doesnt_exist,
    get_last_nivo_date,
    get_all_nivo_date,
)
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.sql.nivo import SensorStationTable
from nivo_api.settings import Config

log = logging.getLogger(__name__)


@contextmanager
def time_elapsed():
    """
    Utility to see the time a command took
    """
    t1 = datetime.now()
    yield
    t2 = datetime.now() - t1
    click.echo(f"The command took {t2.seconds}s to execute ")


@click.command()
def import_last_nivo_data():
    # setup
    # get http://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo/lastNivo.js
    # get last nivo data if needed
    # process it
    # import it.
    last_nivo = get_last_nivo_date()
    if check_nivo_doesnt_exist(last_nivo):
        downloaded_nivo = download_nivo(last_nivo)
        import_nivo(downloaded_nivo)


@click.command()
def import_all_nivo_data():
    # setup
    # go through the meteofrance ftp
    # download all file (via http, better)
    # process it
    # import it
    all_nivo_date = get_all_nivo_date()
    log.info(f"Need to process {len(all_nivo_date)}")
    for nivo_date in all_nivo_date:
        if check_nivo_doesnt_exist(nivo_date["nivo_date"]):
            try:
                downloaded_nivo = download_nivo(**nivo_date)
                import_nivo(downloaded_nivo)
            except Exception as e:
                click.echo("Something bad append : ", e)


@click.command()
def import_nivo_sensor_station():
    # this need refactor
    res = requests.get(f"{Config.METEO_FRANCE_NIVO_BASE_URL}/postesNivo.json")
    res.raise_for_status()
    with connection_scope() as con:
        with con.begin():
            for feature in res.json()["features"]:
                pointz = feature["geometry"]
                pointz["coordinates"].append(int(feature["properties"]["Altitude"]))
                mf_id = (
                    feature["properties"]["ID"]
                    if feature["properties"]["ID"] != ""
                    else None
                )
                ins = (
                    insert(SensorStationTable)
                    .values(
                        **{
                            "nss_name": feature["properties"]["Nom"],
                            "nss_meteofrance_id": mf_id,
                            "the_geom": func.ST_SetSRID(
                                func.ST_GeomFromGeoJSON(json.dumps(pointz)), 4326
                            ),
                        }
                    )
                    .on_conflict_do_nothing(index_elements=["nss_name"])
                )
                con.execute(ins)
        inserted = (
            con.execute(
                select([func.count(SensorStationTable.c.nss_id).label("count")])
            )
            .first()
            .count
        )
        click.echo(f"{inserted} sensor station imported")


@click.command()
def import_last_bra():
    # setup,
    # get https://donneespubliques.meteofrance.fr/donnees_libres/Pdf/BRA/bra.%Y%m%d.json
    # if not 302 (302 means 404 at meteofrance 😭)
    # for all the date, get the xml
    # process
    # import
    bra_dates = get_last_bra_date()
    with connection_scope() as con:
        for massif, date in bra_dates.items():
            try:
                xml = get_bra_xml(massif, date)
                processed_bra = process_xml(con, xml)
                persist_bra(con, processed_bra)
            except Exception as e:
                log.critical(
                    f"an error occured when processing massif {massif} for date {date}"
                )


@click.command()
@click.argument("date", type=click.DateTime(["%Y-%m-%d"]))  # type: ignore
@time_elapsed()
def import_bra(date):
    bra_dates = get_bra_date(date)
    with connection_scope() as con:
        for massif, date in bra_dates.items():
            try:
                if not check_bra_record_exist(con, massif, date):
                    xml = get_bra_xml(massif, date)
                    processed_bra = process_xml(con, xml)
                    persist_bra(con, processed_bra)
                    click.echo(f"Persist {massif.capitalize()}")
            except Exception as e:
                log.debug(e)
                log.critical(
                    f"an error occured when processing massif {massif} for date {date}"
                )


@click.command()
def import_all_bra():
    # setup
    # request https://donneespubliques.meteofrance.fr/donnees_libres/Pdf/BRA/bra.%Y%m%d.json with all the date from december 2016 to today
    # if not 302 (302 means 404 at meteofrance 😭)
    # for all the date in all the json, download the xml of bra
    # process (download + post process)
    # import
    pass


@click.command()
def import_massifs():
    massif_json = requests.get(Config.BRA_BASE_URL + "/massifs.json").json()
    with connection_scope() as con:
        # the 4th element of the massif is useless, and there are no BRA for it.
        for zone in massif_json[:4]:
            for dept in zone["departements"]:
                for massif in dept["massifs"]:
                    click.echo(f"Importing {massif}")
                    try:
                        persist_massif(
                            con,
                            massif,
                            {"name": dept["nom_dep"], "number": dept["num_dep"]},
                            zone["zone"],
                        )
                    except ValueError:
                        log.warning(f"Do no import massif: {massif}")


@click.command()
def import_flowcapt_station():
    with connection_scope() as con:
        with resource_stream("nivo_api", "cli/data/flowcapt.geojson") as fp:
            gj = geojson.load(fp)
            for station in gj:
                persist_flowcapt_station(con, station)


@click.command()
@click.option("--drop", is_flag=True, help="Drop db before creating the schema")
def init_db(drop):
    # create the table if not exist. Assume the db is already here.
    # the command is idem potent
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    if drop:
        click.echo(
            "/!\\ Warning /!\\ you specify drop. Your db will be erased before creation"
        )
    create_schema_and_table(drop)
