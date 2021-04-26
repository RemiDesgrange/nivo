import json
from contextlib import contextmanager
from datetime import datetime, date, timedelta

import click
import geojson
import requests
from pkg_resources import resource_stream
from requests import HTTPError
from sqlalchemy import func, select

from nivo_api.cli.bra_record_helper.miscellaneous import (
    get_bra_xml,
    get_bra_date,
    check_bra_record_exist,
    get_bra_by_dept_from_mf_rpc_api,
    format_xml_from_mf_rpc,
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
from nivo_api.core.db.connection import connection_scope, create_database_connections
from nivo_api.core.db.models.sql.bra import DepartmentTable
from nivo_api.core.db.models.sql.nivo import SensorStationTable
from nivo_api.settings import Config

logging.basicConfig(level=Config.LOG_LEVEL)
log = logging.getLogger(__name__)
log.setLevel(Config.LOG_LEVEL)


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
    db = create_database_connections().engine
    with connection_scope(db) as con:
        last_nivo = get_last_nivo_date()
        if check_nivo_doesnt_exist(con, last_nivo.nivo_date):
            downloaded_nivo = download_nivo(last_nivo, con)
            import_nivo(con, downloaded_nivo)


@click.command()
def import_all_nivo_data():
    # setup
    # download from 2010 to now
    # download all file (via http, better)
    # process it
    # import it
    all_nivo_date = get_all_nivo_date()
    log.info(f"Need to process {len(all_nivo_date)}")
    db = create_database_connections().engine
    with connection_scope(db) as con:
        for nivo_date in all_nivo_date:
            if check_nivo_doesnt_exist(con, nivo_date.nivo_date):
                try:
                    log.info(
                        f"Processing for {nivo_date.nivo_date.strftime('%d-%m-%Y')}"
                    )
                    downloaded_nivo = download_nivo(nivo_date, con)
                    import_nivo(con, downloaded_nivo)
                except Exception as e:
                    click.echo("Something bad append")
                    log.debug(e)


@click.command()
def import_nivo_sensor_station():
    # this need refactor
    res = requests.get(f"{Config.METEO_FRANCE_NIVO_BASE_URL}/postesNivo.json")
    res.raise_for_status()
    db = create_database_connections().engine
    with connection_scope(db) as con:
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
    # This is obsolete.
    db = create_database_connections().engine
    with connection_scope(db) as con:
        for dept in DepartmentTable.get(con):
            try:
                dept = get_bra_by_dept_from_mf_rpc_api(dept.d_number)
                for massif in dept:
                    xml = format_xml_from_mf_rpc(massif["corpsBulletin"])
                    processed_bra = process_xml(con, xml)
                    persist_bra(con, processed_bra)
            except HTTPError as e:
                log.critical(f"dept {dept.d_name} cannot be fetch no BRA")
                log.debug(e)
                continue
            except Exception as e:
                log.critical(
                    f"an error occured when processing dept {dept.d_name} for today"
                )
                log.debug(e)


@click.command()
@click.argument("bra_date", type=click.DateTime(["%Y-%m-%d"]))  # type: ignore
@time_elapsed()
def import_bra(bra_date):
    """
    * setup
    * request https://donneespubliques.meteofrance.fr/donnees_libres/Pdf/BRA/bra.%Y%m%d.json with all the date from december 2016 to today
    * if not 302 (302 means 404 at meteofrance 😭)
    * for all the date in all the json, download the xml of bra
    * process (download + post process)
    * import
    """
    db = create_database_connections().engine
    bra_dates = get_bra_date(bra_date)
    with connection_scope(db) as con:
        for massif, m_date in bra_dates.items():
            try:
                if not check_bra_record_exist(con, massif, m_date):
                    xml = get_bra_xml(massif, m_date)
                    processed_bra = process_xml(con, xml)
                    persist_bra(con, processed_bra)
                    click.echo(f"Persist {massif.capitalize()}")
            except Exception as e:
                log.debug(e)
                log.critical(
                    f"an error occured when processing massif {massif} for date {m_date}"
                )


@click.command()
@time_elapsed()
def import_all_bra():
    """
    Same as `import_bra` but we request from March 2016 to now.
    """
    db = create_database_connections().engine
    start_date = date(year=2016, month=3, day=10)
    date_range = [
        date.today() - timedelta(days=x)
        for x in range((date.today() - start_date).days + 1)
    ]

    for d in date_range:
        massif = ""
        try:
            bra_dates = get_bra_date(d)
            with connection_scope(db) as con:
                for massif, m_date in bra_dates.items():
                    if not check_bra_record_exist(con, massif, m_date):
                        xml = get_bra_xml(massif, m_date)
                        processed_bra = process_xml(con, xml)
                        persist_bra(con, processed_bra)
                        click.echo(f"Persist {massif.capitalize()}")
        except Exception as e:
            log.debug(e)
            log.critical(
                f"an error occured when processing massif {massif} for date {d}"
            )


@click.command()
def import_massifs():
    massif_json = requests.get(Config.BRA_BASE_URL + "/massifs.json").json()
    db = create_database_connections().engine
    with connection_scope(db) as con:
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
    db = create_database_connections().engine
    with connection_scope(db) as con:
        with resource_stream("nivo_api", "cli/data/flowcapt.geojson") as fp:
            gj = geojson.load(fp)
            for station in gj.features:
                persist_flowcapt_station(con, station)


@click.command()
@click.option("--drop", is_flag=True, help="Drop db before creating the schema")
def init_db(drop):
    # create the table if not exist. Assume the db is already here.
    # the command is idem potent
    if drop:
        click.echo(
            "/!\\ Warning /!\\ you specify drop. Your db will be erased before creation"
        )
    create_schema_and_table(drop)
