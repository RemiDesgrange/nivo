#!/bin/sh

init_db --drop
import_massifs
import_nivo_sensor_station
if [[ $ENV== "DEV" ]]; then
    import_last_nivo_data
    import_bra 2019-01-01
fi
