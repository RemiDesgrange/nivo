# import data from meteofrance from cli.
import click

@click.command()
def import_last_nivo_data():
    # setup
    # get http://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo/lastNivo.js
    # get last nivo data if needed
    # process it
    # import it.
    pass

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